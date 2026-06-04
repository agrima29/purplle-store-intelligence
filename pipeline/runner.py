# pipeline/runner.py
import os, json
from pipeline.db import init_db

VIDEO_DIR  = os.environ.get("VIDEO_DIR",  "data/videos")
DB_PATH    = os.environ.get("DB_PATH",    "data/events.db")
MODEL_PATH = os.environ.get("MODEL_PATH", "yolov8n.pt")

CAM_CONFIGS = {
    "CAM_1": {"role": "zone",     "start": "20:10:29"},
    "CAM_2": {"role": "zone",     "start": "20:10:07"},
    "CAM_3": {"role": "entrance", "start": "20:09:50"},
    "CAM_4": {"role": "skip",     "start": "20:09:50"},
    "CAM_5": {"role": "checkout", "start": "20:09:52"},
}

def main():
    print("=== Purplle Store Intelligence Pipeline ===")

    # 1. Create DB tables
    init_db(DB_PATH)
    print("Database initialised")

    # 2. Process CAM_3 first (entry/exit — most critical)
    cam3 = f"{VIDEO_DIR}/CAM_3.mp4"
    if os.path.exists(cam3):
        from pipeline.entry_counter import process_cam3
        entries, exits = process_cam3(cam3, DB_PATH, MODEL_PATH,
                                      start_wall="20:09:50")
        print(f"Entry count: {entries}, Exit count: {exits}")
    else:
        print("WARNING: CAM_3.mp4 not found")

    # 3. Process zone cameras
    from pipeline.zone_tracker import process_zone_camera
    for cam_id, cfg in CAM_CONFIGS.items():
        if cfg["role"] in ("zone", "checkout"):
            path = f"{VIDEO_DIR}/{cam_id}.mp4"
            if os.path.exists(path):
                process_zone_camera(cam_id, path, DB_PATH, MODEL_PATH, cfg["start"])
            else:
                print(f"WARNING: {path} not found")

    # 4. Run anomaly detection on saved events
    from pipeline.anomaly import run_anomaly_detection
    run_anomaly_detection(DB_PATH)

    print("=== Pipeline complete ===")

if __name__ == "__main__":
    main()