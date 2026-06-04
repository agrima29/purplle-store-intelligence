# api/routes/metrics.py
import os, sqlite3
from fastapi import APIRouter
from pipeline.sales_loader import load_sales

router = APIRouter()
DB = os.environ.get("DB_PATH", "data/events.db")
CSV = os.environ.get("SALES_CSV", "data/sales/Brigade_Bangalore_10_April_26.csv")

def _video_stats():
    if not os.path.exists(DB):
        return {"status":"pipeline_not_run","entries":0,"exits":0,
                "checkout_visitors":0,"avg_dwell":0}
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    entries  = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='person_entered'").fetchone()[0]
    exits    = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='person_exited'").fetchone()[0]
    checkout = conn.execute("SELECT COUNT(DISTINCT track_id) FROM events WHERE zone='checkout'").fetchone()[0]
    avg_dwell = conn.execute("SELECT AVG(dwell_seconds) FROM events WHERE event_type='dwell_update'").fetchone()[0] or 0
    conn.close()
    return {"status":"ok","entries":entries,"exits":exits,
            "checkout_visitors":checkout,"avg_dwell":round(avg_dwell,1)}

@router.get("/metrics")
def get_metrics():
    v = _video_stats()
    sales = load_sales(CSV)    # reads CSV dynamically every call
    entries = max(v["entries"], 1)
    conversion = min(
            100.0,
            round(v["checkout_visitors"] / entries * 100, 1)
    )

    kpi_summary = {
        "gmv_per_customer": round(
            sales.get("total_gmv_inr", 0) /
            max(sales.get("unique_customers", 1), 1),
            2
        ),
        "gmv_per_transaction": round(
            sales.get("total_gmv_inr", 0) /
            max(sales.get("total_transactions", 1), 1),
            2
        )
    }
    return {
        "pipeline_status": v["status"],
        "store": sales.get("store", "Unknown Store"),
        "video_clip": {
            "window": "derived_from_video_processing",
            "cameras": ["CAM_1","CAM_2","CAM_3","CAM_5"],
            "staff_excluded": "CAM_4",
            "entries": v["entries"],
            "exits": v["exits"],
            "in_store": max(0, v["entries"]-v["exits"]),
            "checkout_visitors": v["checkout_visitors"],
            "conversion_pct": conversion,
            "avg_dwell_seconds": v["avg_dwell"],
        },
        "full_day": sales,   # 100% dynamic from CSV
        "kpis": kpi_summary,
        "intelligence": {
            "top_zone_by_revenue": max(sales.get("revenue_by_zone",{"?":0}), key=sales.get("revenue_by_zone",{"?":0}).get),
            "top_salesperson": sales.get("top_salesperson"),
            "peak_hour": sales.get("peak_sales_hour"),
            "department_revenue": 
                sales.get("department_revenue", {}),
        }
    }