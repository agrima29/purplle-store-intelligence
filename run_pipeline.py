from pipeline.entry_counter import process_cam3
from pipeline.zone_tracker import process_zone_camera

DB_PATH = "data/events.db"

print("Starting pipeline...")

# CAM 3 - Entry / Exit
process_cam3(
    video_path="data/videos/CAM_3.mp4",
    db_path=DB_PATH
)

# CAM 1
process_zone_camera(
    cam_id="CAM_1",
    video_path="data/videos/CAM_1.mp4",
    db_path=DB_PATH
)

# CAM 2
process_zone_camera(
    cam_id="CAM_2",
    video_path="data/videos/CAM_2.mp4",
    db_path=DB_PATH
)

# CAM 5
process_zone_camera(
    cam_id="CAM_5",
    video_path="data/videos/CAM_5.mp4",
    db_path=DB_PATH
)

print("Pipeline Complete")