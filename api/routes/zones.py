# api/routes/zones.py  (add the heatmap endpoint here)
import cv2, numpy as np, sqlite3, os, base64
from fastapi import APIRouter

router = APIRouter()
DB = os.environ.get("DB_PATH", "data/events.db")

@router.get("/zones")
def get_zones():
    if not os.path.exists(DB):
        return {"zones":[]}
    conn = sqlite3.connect(DB)
    rows = conn.execute("""
        SELECT zone, COUNT(DISTINCT track_id) as visitors,
               AVG(dwell_seconds) as avg_dwell, MAX(dwell_seconds) as max_dwell
        FROM events WHERE zone IS NOT NULL AND event_type='dwell_update'
        GROUP BY zone ORDER BY avg_dwell DESC
    """).fetchall()
    conn.close()
    return {"zones": [{"zone_id":r[0],"visitors":r[1],
                       "avg_dwell_s":round(r[2] or 0,1),"max_dwell_s":round(r[3] or 0,1)}
                      for r in rows]}

@router.get("/zones/{zone_id}/heatmap")
def get_heatmap(zone_id: str):
    """
    Returns a base64 PNG heatmap of where people spent time in this zone.
    Generated from bbox positions stored in events.
    """
    if not os.path.exists(DB):
        return {"error": "no data"}

    conn = sqlite3.connect(DB)
    # Get all bounding box positions for this zone
    rows = conn.execute("""
        SELECT metadata FROM events
        WHERE zone=? AND event_type='dwell_update' AND metadata IS NOT NULL
    """, (zone_id,)).fetchall()
    conn.close()

    # Create accumulation grid (1920x1080 scaled to 192x108)
    W, H   = 192, 108
    grid   = np.zeros((H, W), dtype=np.float32)

    import json
    for (meta_str,) in rows:
        try:
            meta = json.loads(meta_str)
            if "cx" in meta and "cy" in meta:
                x = int(meta["cx"] / 1920 * W)
                y = int(meta["cy"] / 1080 * H)
                x = max(0, min(W-1, x))
                y = max(0, min(H-1, y))
                grid[y, x] += 1
        except:
            pass

    if grid.max() == 0:
        return {"zone_id": zone_id, "heatmap_b64": None,
                "note": "no position data yet — add cx/cy to dwell_update events"}

    # Gaussian blur to spread heat naturally
    grid = cv2.GaussianBlur(grid, (15, 15), 0)
    grid = (grid / grid.max() * 255).astype(np.uint8)
    colored = cv2.applyColorMap(grid, cv2.COLORMAP_JET)

    _, buf = cv2.imencode(".png", colored)
    b64 = base64.b64encode(buf).decode()
    return {"zone_id": zone_id, "heatmap_b64": b64,
            "format": "PNG, base64 encoded, 192x108px"}