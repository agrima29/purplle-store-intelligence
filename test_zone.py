from pipeline.zone_tracker import process_zone_camera

process_zone_camera(
    cam_id="CAM_1",
    video_path="data/videos/CAM_1.mp4",
    db_path="data/events.db"
)