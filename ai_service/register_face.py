import cv2
import face_recognition
import numpy as np
import os
import time
import requests

ENCODINGS_DIR = "encodings"
TOLERANCE = 0.5   # lower = stricter
MODEL = "hog"     # cpu-friendly

def load_known_faces():
    known_encodings = []
    known_ids = []

    for file in os.listdir(ENCODINGS_DIR):
        if file.endswith(".npy"):
            student_id = file.replace(".npy", "")
            encoding = np.load(os.path.join(ENCODINGS_DIR, file))
            known_encodings.append(encoding)
            known_ids.append(student_id)

    return known_encodings, known_ids


def send_attendance(student_id):
    url = "http://127.0.0.1:8000/api/attendance/mark/"
    payload = {
        "student": int(student_id),
        "subject": 1,   # TEMP (later dynamic)
        "hour": 1       # TEMP (later dynamic)
    }

    try:
        res = requests.post(url, json=payload, timeout=3)
        try:
            print("📡 Backend response:", res.json())
        except Exception:
            print("📡 Backend response:", res.status_code)
    except Exception as e:
        print("❌ Failed to send attendance:", e)


def recognize_faces():
    print("🔍 Loading known face encodings...")
    known_encodings, known_ids = load_known_faces()

    if not known_encodings:
        print("❌ No registered faces found")
        return

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        print("❌ Camera not accessible")
        return

    window_name = "AI Attendance - Face Recognition"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 900, 600)

    print("\n📸 Camera ON")
    print("👉 Press Q to quit\n")

    last_seen = {}

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(
            rgb, number_of_times_to_upsample=0, model=MODEL
        )
        face_encodings = face_recognition.face_encodings(
            rgb, face_locations
        )

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            distances = face_recognition.face_distance(
                known_encodings, face_encoding
            )

            best_match_index = np.argmin(distances)

            name = "Unknown"

            if distances[best_match_index] < TOLERANCE:
                student_id = known_ids[best_match_index]
                name = f"ID: {student_id}"

                # 🔔 Attendance trigger (temporary)
                if student_id not in last_seen:
                    print(f"✅ Student recognized: {student_id}")
                    send_attendance(student_id)
                    last_seen[student_id] = time.time()

            # Draw box + label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognize_faces()
