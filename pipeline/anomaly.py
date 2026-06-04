# pipeline/anomaly.py
import sqlite3, uuid
from pipeline.db import get_conn

LOITER_SECONDS = 60     # stationary for 1min = loitering
QUEUE_THRESHOLD = 3     # 3+ people in checkout at once = queue buildup

def run_anomaly_detection(db_path):
    conn = get_conn(db_path)

    # 1. Loitering: single person dwell > threshold in one zone
    rows = conn.execute("""
        SELECT camera_id, track_id, zone, dwell_seconds, timestamp
        FROM events WHERE event_type='dwell_update' AND dwell_seconds > ?
    """, (LOITER_SECONDS,)).fetchall()

    for row in rows:
        conn.execute("""
            INSERT OR IGNORE INTO anomalies
            (event_id,anomaly_type,severity,camera_id,track_id,zone,timestamp,description)
            VALUES (?,?,?,?,?,?,?,?)
        """, (str(uuid.uuid4()), "loitering",
              "high" if row["dwell_seconds"] > 180 else "medium",
              row["camera_id"], row["track_id"], row["zone"], row["timestamp"],
              f"Person {row['track_id']} stayed {row['dwell_seconds']:.0f}s in {row['zone']}"))

    # 2. Queue buildup: multiple people in checkout in the same minute
    rows2 = conn.execute("""
        SELECT substr(timestamp,1,5) as minute,
               COUNT(DISTINCT track_id) as count
        FROM events WHERE zone='checkout'
        GROUP BY minute HAVING count >= ?
    """, (QUEUE_THRESHOLD,)).fetchall()

    for row in rows2:
        conn.execute("""
            INSERT OR IGNORE INTO anomalies
            (event_id,anomaly_type,severity,camera_id,zone,timestamp,description)
            VALUES (?,?,?,?,?,?,?)
        """, (str(uuid.uuid4()), "queue_buildup", "medium",
              "CAM_5", "checkout", row["minute"],
              f"Queue buildup: {row['count']} people at checkout at {row['minute']}"))

    conn.commit()
    conn.close()
    print("Anomaly detection complete")