# pipeline/entry_counter.py
import cv2, supervision as sv, uuid, json
from ultralytics import YOLO
from pipeline.db import get_conn

RE_ENTRY_COOLDOWN = 30   # seconds — same track can't enter twice within 30s

def wall_time(frame_num, fps, start_str):
    """Convert frame number to HH:MM:SS using video start time."""
    h, m, s = map(int, start_str.split(":"))
    total = h*3600 + m*60 + s + frame_num/fps
    return f"{int(total//3600):02d}:{int(total%3600//60):02d}:{int(total%60):02d}"

def process_cam3(video_path, db_path, model_path="yolov8n.pt",
                start_wall="20:09:50",
                line_start=(1180, 250), line_end=(1180, 850)):

    model   = YOLO(model_path)
    tracker = sv.ByteTrack()
    conn    = get_conn(db_path)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 29.97
    frame_num  = 0
    entries    = 0
    exits      = 0

    previous_x = {}
    ENTRY_X = 1500

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Skip every other frame on slow machines (halves processing time)
        # Comment this out if you have time — more frames = more accurate
        if frame_num % 5 != 0:
            frame_num += 1
            continue

        ts = wall_time(frame_num, fps, start_wall)

        results = model(frame, conf=0.4, classes=[0], verbose=False)[0]
        dets    = sv.Detections.from_ultralytics(results)
        dets = tracker.update_with_detections(dets)

        if dets.tracker_id is None or len(dets) == 0:
            frame_num += 1
            continue

        if dets.tracker_id is not None:
            for i, tid in enumerate(dets.tracker_id):
                x1, y1, x2, y2 = dets.xyxy[i]

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                

        for i, tid in enumerate(dets.tracker_id):
            tid = int(tid)

            x1, y1, x2, y2 = dets.xyxy[i]
            cx = int((x1 + x2) / 2)

            prev_x = previous_x.get(tid)

            if prev_x is not None:

                # Entering store
                if prev_x > ENTRY_X and cx <= ENTRY_X:
                    entries += 1
                    _save(
                        conn,
                        "person_entered",
                        "CAM_3",
                        tid,
                        None,
                        ts,
                        frame_num
                    )

                # Exiting store
                elif prev_x <= ENTRY_X and cx > ENTRY_X:
                    exits += 1
                    _save(
                        conn,
                        "person_exited",
                        "CAM_3",
                        tid,
                        None,
                        ts,
                        frame_num
                    )

            previous_x[tid] = cx

        frame_num += 1

    cap.release()
    conn.close()
    print(f"CAM_3: {entries} entries, {exits} exits")
    return entries, exits

def _save(conn, etype, cam, tid, zone, ts, frame):
    conn.execute("""
        INSERT OR IGNORE INTO events
        (event_id, event_type, camera_id, track_id, zone, timestamp, frame)
        VALUES (?,?,?,?,?,?,?)
    """, (str(uuid.uuid4()), etype, cam, tid, zone, ts, frame))
    conn.commit()