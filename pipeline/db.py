# pipeline/db.py
import sqlite3, os

DB_PATH = os.environ.get("DB_PATH", "data/events.db")

def get_conn(path=None):
    p = path or DB_PATH
    os.makedirs(os.path.dirname(p), exist_ok=True)
    conn = sqlite3.connect(p, check_same_thread=False)
    conn.row_factory = sqlite3.Row   # lets you do row["column_name"] instead of row[0]
    return conn

def init_db(path=None):
    conn = get_conn(path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            event_id      TEXT PRIMARY KEY,
            event_type    TEXT NOT NULL,
            camera_id     TEXT NOT NULL,
            track_id      INTEGER,
            zone          TEXT,
            timestamp     TEXT,
            frame         INTEGER,
            dwell_seconds REAL,
            metadata      TEXT
        );
        CREATE TABLE IF NOT EXISTS anomalies (
            event_id     TEXT PRIMARY KEY,
            anomaly_type TEXT,
            severity     TEXT,
            camera_id    TEXT,
            track_id     INTEGER,
            zone         TEXT,
            timestamp    TEXT,
            description  TEXT,
            resolved     INTEGER DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_event_type   ON events(event_type);
        CREATE INDEX IF NOT EXISTS idx_event_camera ON events(camera_id);
        CREATE INDEX IF NOT EXISTS idx_event_zone   ON events(zone);
        CREATE INDEX IF NOT EXISTS idx_track_id ON events(track_id);
    """)
    conn.commit()
    conn.close()