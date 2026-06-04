# api/routes/insights.py
import os
import sqlite3
from fastapi import APIRouter
from pipeline.sales_loader import load_sales

router = APIRouter()
DB  = os.environ.get("DB_PATH",    "data/events.db")
CSV = os.environ.get("SALES_CSV",  "data/sales/Brigade_Bangalore_10_April_26.csv")

def _gather_context():
    """Pull key stats to give Claude context for insights."""
    stats = {}
    if os.path.exists(DB):
        conn = sqlite3.connect(DB)
        stats["entries"]   = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='person_entered'").fetchone()[0]
        stats["exits"]     = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='person_exited'").fetchone()[0]
        stats["anomalies"] = conn.execute("SELECT COUNT(*) FROM anomalies WHERE resolved=0").fetchone()[0]
        zone_rows = conn.execute("""
            SELECT zone, COUNT(DISTINCT track_id), AVG(dwell_seconds)
            FROM events WHERE zone IS NOT NULL AND event_type='dwell_update'
            GROUP BY zone ORDER BY AVG(dwell_seconds) DESC
        """).fetchall()
        stats["zones"] = [{"zone":r[0],"visitors":r[1],"avg_dwell":round(r[2] or 0,1)} for r in zone_rows]
        conn.close()

    if os.path.exists(CSV):
        from pipeline.sales_loader import load_sales
        sales = load_sales(CSV)
        stats["total_gmv"]      = sales.get("total_gmv_inr")
        stats["total_orders"]   = sales.get("total_transactions")
        stats["revenue_by_zone"]= sales.get("revenue_by_zone")
        stats["peak_hour"]      = sales.get("peak_sales_hour")
    return stats

@router.get("/insights")
def get_insights():

    sales = load_sales(CSV)

    revenue_by_zone = sales.get("revenue_by_zone", {})
    top_zone = max(revenue_by_zone, key=revenue_by_zone.get)

    top_salesperson = sales.get("top_salesperson")
    peak_hour = sales.get("peak_sales_hour")

    avg_dwell = 0

    if os.path.exists(DB):
        conn = sqlite3.connect(DB)

        row = conn.execute("""
            SELECT AVG(dwell_seconds)
            FROM events
            WHERE event_type='dwell_update'
        """).fetchone()

        avg_dwell = round(row[0] or 0, 1)

        conn.close()

    insights = [
        {
            "title": "Top Revenue Zone",
            "insight":
                f"{top_zone} generated the highest revenue and should receive priority merchandising."
        },

        {
            "title": "Peak Sales Window",
            "insight":
                f"Customer purchases peaked around {peak_hour}. Consider allocating additional staff during this period."
        },

        {
            "title": "Best Sales Performer",
            "insight":
                f"{top_salesperson} generated the highest GMV among all sales associates."
        },

        {
            "title": "Customer Engagement",
            "insight":
                f"Average observed dwell time was {avg_dwell} seconds."
        }
    ]

    return {
        "store": sales.get("store"),
        "date": sales.get("date"),
        "insights": insights
    }
