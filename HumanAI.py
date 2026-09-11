import cv2
from ultralytics import YOLO

model = YOLO("yolo11n-pose.pt")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Camera could not be opened.")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break

    results = model.predict(
        source=frame,
        classes=[0],
        conf=0.5,
        verbose=False
    )

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO11 Human Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()