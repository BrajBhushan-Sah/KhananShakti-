from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO(r"c:\Users\Brajbhushan Sah\runs\detect\train-12\weights\best.pt")  # Replace with your model path

# Open laptop webcam
cap = cv2.VideoCapture(0)

# Optional: Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to access camera.")
        break

    # Run inference
    results = model(frame, conf=0.25)

    # Draw detections
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("YOLO Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()