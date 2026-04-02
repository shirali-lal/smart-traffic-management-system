import cv2
from ultralytics import YOLO
import json
import time

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("traffic.mp4")

prev_positions = {}
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    lanes = [0, 0, 0, 0]
    speeds = []

    current_time = time.time()
    time_diff = current_time - prev_time
    prev_time = current_time

    for r in results:
        for i, box in enumerate(r.boxes):
            cls = int(box.cls[0])

            if cls in [2, 3, 5, 7]:  # vehicles
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Lane counting
                if cx < 320:
                    lanes[0] += 1
                elif cx < 640:
                    lanes[1] += 1
                elif cx < 960:
                    lanes[2] += 1
                else:
                    lanes[3] += 1

                # Speed tracking
                if i in prev_positions:
                    px, py = prev_positions[i]
                    distance = ((cx - px)**2 + (cy - py)**2) ** 0.5

                    speed = distance / (time_diff + 1e-5)
                    speeds.append(speed)

                    # Overspeed check
                    if speed > 50:  # threshold (adjust)
                        cv2.putText(frame, "OVERSPEED!", (cx, cy),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                prev_positions[i] = (cx, cy)

    avg_speed = sum(speeds)/len(speeds) if speeds else 0

    data = {
        "lane1": lanes[0],
        "lane2": lanes[1],
        "lane3": lanes[2],
        "lane4": lanes[3],
        "emergency": 0,
        "avg_speed": round(avg_speed, 2)
    }

    with open("data.json", "w") as f:
        json.dump(data, f)

    print(data)

    cv2.imshow("Traffic", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()