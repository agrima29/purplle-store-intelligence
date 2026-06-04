# pipeline/sales_loader.py
import pandas as pd, os

CSV_PATH = os.environ.get("Brigade_Bangalore_10_April_26.csv", "data/sales/Brigade_Bangalore_10_April_26.csv")

# Department name in CSV → camera zone (from dep_name column)
DEPT_TO_ZONE = {
    "makeup":        "makeup-aisle",
    "skin":          "skincare-aisle",
    "hair":          "hair-section",
    "bath-and-body": "skincare-aisle",
    "personal-care": "skincare-aisle",
    "fragrance":     "other",
}

def load_sales(path=None):
    """Read CSV and compute all metrics dynamically. Zero hardcoding."""
    p = path or CSV_PATH
    if not os.path.exists(p):
        return {"error": "CSV not found", "path": p}

    df = pd.read_csv(p)

    # Core metrics — computed from data
    total_gmv        = int(df["GMV"].sum())
    total_nmv        = round(float(df["NMV"].sum()), 2)
    total_orders     = int(df["order_id"].nunique())
    unique_customers = int(df["customer_number"].nunique())
    avg_basket = round(total_gmv / total_orders, 2) if total_orders else 0

    # Peak hour — computed from data
    df["hour"] = df["order_time"].astype(str).str[:2]
    hourly = df.groupby("hour")["order_id"].nunique()
    peak_hour = hourly.idxmax() + ":00"
    peak_count = int(hourly.max())

    # Revenue by zone — uses dep_name column, no brand names
    df["zone"] = df["dep_name"].map(DEPT_TO_ZONE).fillna("other")
    zone_rev = df.groupby("zone")["GMV"].sum().to_dict()
    zone_rev = {k: int(v) for k, v in zone_rev.items()}
    department_revenue = (
    df.groupby("dep_name")["GMV"]
      .sum()
      .astype(int)
      .to_dict()
    )

    # Salesperson performance — computed from data
    staff = (df.groupby("salesperson_name")
               .agg(orders=("order_id","nunique"), gmv=("GMV","sum"), items=("qty","sum"))
               .sort_values("gmv", ascending=False)
               .reset_index())
    staff_perf = {
        row["salesperson_name"]: {
            "orders": int(row["orders"]),
            "gmv": int(row["gmv"]),
            "items": int(row["items"])
        }
        for _, row in staff.iterrows()
    }

    # Hourly order breakdown
    orders_by_hour = {h: int(c) for h, c in hourly.items()}

    top_salesperson = (
        staff.iloc[0]["salesperson_name"]
        if not staff.empty
        else "unknown"
   )

    return {
        "date": str(df["order_date"].iloc[0]) if "order_date" in df.columns else "unknown",
        "store": str(df["store_name"].iloc[0]) if "store_name" in df.columns else "unknown",
        "total_transactions": total_orders,
        "unique_customers": unique_customers,
        "total_gmv_inr": total_gmv,
        "total_nmv_inr": total_nmv,
        "avg_basket_gmv_inr": avg_basket,
        "peak_sales_hour": peak_hour,
        "peak_hour_transactions": peak_count,
        "orders_by_hour": orders_by_hour,
        "revenue_by_zone": zone_rev,
        "department_revenue": department_revenue,
        "salesperson_performance": staff_perf,
        "top_salesperson": top_salesperson
    }