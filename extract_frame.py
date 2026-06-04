import cv2

cap = cv2.VideoCapture("data/videos/CAM_3.mp4")

success, frame = cap.read()

if success:
    cv2.imwrite("cam3_first_frame.jpg", frame)
    print("Saved cam3_first_frame.jpg")
else:
    print("Could not read frame")

cap.release()