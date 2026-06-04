from ultralytics import YOLO
import cv2
import os

VIDEO_PATH = "data/videos/CAM_3.mp4"

print("Loading YOLO model...")

model = YOLO("yolov8n.pt")

print("Opening video...")

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"Could not open video: {VIDEO_PATH}")
    exit()

success, frame = cap.read()

print("Frame read:", success)

if not success:
    print("Could not read frame")
    exit()

print("Running detection...")

results = model(frame, classes=[0])

count = len(results[0].boxes)

print(f"People detected: {count}")

for box in results[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0,255,0),
        2
    )

os.makedirs("data/output", exist_ok=True)

output_path = "data/output/cam3_detection.jpg"

cv2.imwrite(output_path, frame)

print(f"Saved image: {output_path}")