from fastapi import APIRouter
import sqlite3, os

router = APIRouter()

DB = os.environ.get("DB_PATH", "data/events.db")


@router.get("/footfall/current")
def current_footfall():

    if not os.path.exists(DB):
        return {
            "entries": 0,
            "exits": 0,
            "occupancy": 0
        }

    conn = sqlite3.connect(DB)

    entries = conn.execute(
        """
        SELECT COUNT(*)
        FROM events
        WHERE event_type='person_entered'
        """
    ).fetchone()[0]

    exits = conn.execute(
        """
        SELECT COUNT(*)
        FROM events
        WHERE event_type='person_exited'
        """
    ).fetchone()[0]

    conn.close()

    return {
        "entries": entries,
        "exits": exits,
        "occupancy": max(0, entries - exits)
    }