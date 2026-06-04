from fastapi import APIRouter
from pipeline.sales_loader import load_sales
import sqlite3, os

router = APIRouter()
DB = os.environ.get("DB_PATH", "data/events.db")
CSV = os.environ.get("SALES_CSV", "data/sales/Brigade_Bangalore_10_April_26.csv")


@router.get("/funnel")
def get_funnel():
    try:
        sales = load_sales()
        converted = sales.get("total_transactions", 0)
        conn = sqlite3.connect(DB) if os.path.exists(DB) else None

        entered = conn.execute(
            "SELECT COUNT(DISTINCT track_id) FROM events WHERE event_type='person_entered'"
        ).fetchone()[0] if conn else 0

        browsed = conn.execute("""
            SELECT COUNT(DISTINCT track_id) FROM events
            WHERE camera_id IN ('CAM_1','CAM_2')
              AND event_type IN ('zone_enter','dwell_update')
        """).fetchone()[0] if conn else 0

        checkout = conn.execute(
            "SELECT COUNT(DISTINCT track_id) FROM events WHERE zone='checkout'"
        ).fetchone()[0] if conn else 0

        if conn:
            conn.close()

        

        def pct(n, d):
            return round(n / max(d, 1) * 100, 1)
        
        # Purchase data comes from full-day POS data,
        # so it cannot be directly compared to video entries.
        overall_conversion = None

        return {
            "funnel_type": "session_based",

            "note":
                "Each unique track_id represents one visitor session.",

            "purchase_note":
                "Purchase data is full-day POS data and not directly linked to video sessions.",

            "overall_conversion_pct": overall_conversion,

            "stages": [
                {
                    "stage": "entry",
                    "label": "Entered Store",
                    "count": entered,
                    "pct_of_entry": 100.0,
                    "source": "CAM_3 tripwire"
                },

                {
                    "stage": "browse",
                    "label": "Browsed Aisles",
                    "count": browsed,
                    "pct_of_entry": pct(browsed, entered) if entered > 0 else None,
                    "dropoff": pct(entered - browsed, entered) if browsed > 0 and entered >= browsed else None,
                    "source": "CAM_1 + CAM_2"
                },

                {
                    "stage": "checkout",
                    "label": "Reached Checkout",
                    "count": checkout,
                    "pct_of_entry": pct(checkout, entered) if entered > 0 else None,
                    "dropoff": pct(browsed - checkout, browsed) if browsed > 0 else None,
                    "source": "CAM_5"
                },

                {
                    "stage": "purchase",
                    "label": "Completed Purchase",
                    "count": converted,
                    "pct_of_entry": None,
                    "source": "POS CSV"
                }
            ],

            "summary": {
                "entered_store": entered,
                "browsed": browsed,
                "checkout_visitors": checkout,
                "purchases": converted,
                "overall_conversion_pct": overall_conversion
            }
        }
    
    except Exception as e:
        return {"error": str(e), "stages": []}
    
