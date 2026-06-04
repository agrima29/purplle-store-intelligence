# api/routes/journey.py
import os, sqlite3
from fastapi import APIRouter

router = APIRouter()
DB = os.environ.get("DB_PATH", "data/events.db")

@router.get("/journey/{track_id}")
def get_journey(track_id: int):
    """Returns the complete path of a single customer through the store."""
    if not os.path.exists(DB):
        return {"track_id": track_id, "path": []}

    conn = sqlite3.connect(DB)
    rows = conn.execute("""
        SELECT event_type, camera_id, zone, timestamp, dwell_seconds
        FROM events WHERE track_id=?
        ORDER BY timestamp ASC
    """, (track_id,)).fetchall()
    conn.close()

    path = []
    for etype, cam, zone, ts, dwell in rows:
        step = {"event": etype, "camera": cam, "timestamp": ts}
        if zone:
            step["zone"] = zone
        if dwell:
            step["dwell_seconds"] = round(dwell, 1)
        path.append(step)

    # Build a simple readable journey string
    zones_visited = [r[2] for r in rows if r[2] is not None]
    # Deduplicate consecutive same zones
    journey_str = []
    prev = None
    for z in zones_visited:
        if z != prev:
            journey_str.append(z)
            prev = z

    return {
        "track_id": track_id,
        "journey": journey_str or ["no zone data"],
        "total_events": len(rows),
        "detailed_path": path
    }