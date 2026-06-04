import sqlite3

conn = sqlite3.connect("data/events.db")

conn.execute("DELETE FROM events")
conn.commit()



conn.close()

print("Events cleared")