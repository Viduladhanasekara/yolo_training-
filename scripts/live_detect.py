from ultralytics import YOLO
import cv2
import time

# Load trained model
model = YOLO(
    r"D:\Crack_defect_project\runs\detect\train-6\weights\best.pt"
)

# Webcam
cap = cv2.VideoCapture(3)

prev_time = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, conf=0.5)

    annotated = results[0].plot()

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(
        annotated,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Building Defect Detection", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()