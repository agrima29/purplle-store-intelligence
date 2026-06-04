from fastapi import APIRouter
import sqlite3, os

router = APIRouter()

DB = os.environ.get("DB_PATH", "data/events.db")


@router.get("/anomalies")
def get_anomalies():

    if not os.path.exists(DB):
        return {"anomalies": []}

    conn = sqlite3.connect(DB)

    rows = conn.execute("""
        SELECT
            anomaly_type,
            severity,
            camera_id,
            timestamp,
            description
        FROM anomalies
        ORDER BY timestamp DESC
    """).fetchall()

    conn.close()

    return {
        "count": len(rows),
        "anomalies": [
            {
                "type": r[0],
                "severity": r[1],
                "camera": r[2],
                "timestamp": r[3],
                "description": r[4]
            }
            for r in rows
        ]
    }