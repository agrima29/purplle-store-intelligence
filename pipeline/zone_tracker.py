# pipeline/zone_tracker.py
import cv2, supervision as sv, uuid, json
from ultralytics import YOLO
from pipeline.db import get_conn

# Three simple zones per camera — uses dep_name logic, not brand names
ZONES = {
    "CAM_1": [
        {"id": "skincare-aisle", "name": "Skincare Aisle",
         "bbox": [0, 250, 1350, 950]},
        {"id": "makeup-station", "name": "Makeup Station",
         "bbox": [1350, 300, 1920, 950]},
    ],
    "CAM_2": [
        {"id": "makeup-aisle", "name": "Makeup Aisle",
         "bbox": [0, 250, 1920, 950]},
    ],
    "CAM_5": [
        {"id": "checkout", "name": "Checkout Counter",
         "bbox": [0, 150, 1920, 950]},
    ],
}

STAFF_DARK_THRESHOLD = 0.50   # # >50% dark pixels → likely staff uniform
MIN_DWELL_SECONDS = 2

def is_staff(frame, bbox):
    """Staff wear all-black uniforms. Check crop darkness."""
    x1, y1, x2, y2 = map(int, bbox)
    x1, y1 = max(0,x1), max(0,y1)
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return False
    import cv2 as _cv2
    gray = _cv2.cvtColor(crop, _cv2.COLOR_BGR2GRAY)
    return float((gray < 60).mean()) > STAFF_DARK_THRESHOLD

def get_zone(x, y, zones):
    for z in zones:
        x1,y1,x2,y2 = z["bbox"]
        if x1 <= x <= x2 and y1 <= y <= y2:
            return z["id"]
    return None

def wall_time(frame_num, fps, start_str):
    h, m, s = map(int, start_str.split(":"))
    total = h*3600 + m*60 + s + frame_num/fps
    return f"{int(total//3600):02d}:{int(total%3600//60):02d}:{int(total%60):02d}"

def process_zone_camera(cam_id, video_path, db_path,
                        model_path="yolov8n.pt", start_wall="20:10:00"):

    if cam_id == "CAM_4":
        print("CAM_4 skipped — staff room")
        return

    model   = YOLO(model_path)
    tracker = sv.ByteTrack()
    conn    = get_conn(db_path)
    zones   = ZONES.get(cam_id, [])

    cap       = cv2.VideoCapture(video_path)
    fps       = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_num = 0
    track_state = {}   # tid → {zone, zone_entry_frame, is_staff}

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_num % 3 != 0:   # process every 3rd frame for zone cameras
            frame_num += 1
            continue

        ts      = wall_time(frame_num, fps, start_wall)
        results = model(frame, conf=0.4, classes=[0], verbose=False)[0]
        dets    = sv.Detections.from_ultralytics(results)
        dets    = tracker.update_with_detections(dets)

        if dets.tracker_id is None or len(dets) == 0:
            frame_num += 1
            continue

        active_ids = set()
        for i, (bbox, tid) in enumerate(zip(dets.xyxy, dets.tracker_id)):
            tid = int(tid)
            active_ids.add(tid)

            if tid not in track_state:
                track_state[tid] = {
                    "zone": None, "zone_entry_frame": frame_num,
                    "is_staff": is_staff(frame, bbox),
                    "last_zone_enter": None
                }

            state = track_state[tid]
            if state["is_staff"]:
                continue

            cx = (bbox[0] + bbox[2]) / 2
            cy = bbox[3]   # foot position = bottom of bounding box
            new_zone = get_zone(cx, cy, zones)

            if new_zone and new_zone != state["zone"]:
                old_zone = state["zone"]
                # Save dwell in old zone
                if old_zone:
                    dwell = (frame_num - state["zone_entry_frame"]) / fps
                    if dwell >= MIN_DWELL_SECONDS:
                        conn.execute("""
                            INSERT OR IGNORE INTO events
                            (event_id,event_type,camera_id,track_id,zone,timestamp,frame,dwell_seconds,metadata)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        """, (str(uuid.uuid4()), "dwell_update", cam_id, tid,
                          old_zone, ts, frame_num, round(dwell,2),
                          json.dumps({"from":old_zone,"to":new_zone})))
                    

                state["zone"] = new_zone
                state["zone_entry_frame"] = frame_num

                if new_zone and state["last_zone_enter"] != new_zone:
                    conn.execute("""
                        INSERT OR IGNORE INTO events
                        (event_id,event_type,camera_id,track_id,zone,timestamp,frame)
                        VALUES (?,?,?,?,?,?,?)
                    """, (
                        str(uuid.uuid4()),
                        "zone_enter",
                        cam_id,
                        tid,
                        new_zone,
                        ts,
                        frame_num
                    ))

                    state["last_zone_enter"] = new_zone

        # Finalize disappeared tracks
        for tid in list(track_state.keys()):
            if tid not in active_ids:
                state = track_state.pop(tid)
                if state["zone"] and not state["is_staff"]:
                    dwell = (frame_num - state["zone_entry_frame"]) / fps
                    
                    if dwell >= MIN_DWELL_SECONDS:
                        conn.execute("""
                            INSERT OR IGNORE INTO events
                            (event_id,event_type,camera_id,track_id,zone,timestamp,frame,dwell_seconds)
                            VALUES (?,?,?,?,?,?,?,?)
                        """, (str(uuid.uuid4()), "dwell_update", cam_id, tid,
                            state["zone"], ts, frame_num, round(dwell,2)))
                    

        frame_num += 1

    conn.commit()

    cap.release()
    conn.close()
    print(f"{cam_id}: zone tracking complete")