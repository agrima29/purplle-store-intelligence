from pipeline.entry_counter import process_cam3

entries, exits = process_cam3(
    video_path="data/videos/CAM_3.mp4",
    db_path="data/events.db"
)

print("Entries:", entries)
print("Exits:", exits)