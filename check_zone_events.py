import sqlite3

conn = sqlite3.connect("data/events.db")

print("\nLast 20 Events:\n")

for row in conn.execute("""
SELECT event_type, camera_id, zone, track_id, dwell_seconds
FROM events
ORDER BY rowid DESC
LIMIT 20
"""):
    print(row)

conn.close()