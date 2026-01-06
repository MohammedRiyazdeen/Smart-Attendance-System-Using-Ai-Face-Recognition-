import cv2
import face_recognition
import numpy as np
import os
import time
import requests

ENCODINGS_DIR = "encodings"
TOLERANCE = 0.5
MODEL = "hog"

API_URL = "http://127.0.0.1:8000/api/attendance/mark/"
SESSION_ID = 1   # 🔥 set from teacher dashboard later


def load_known_faces():
    known_encodings = []
    known_ids = []

    for file in os.listdir(ENCODINGS_DIR):
        if file.endswith(".npy"):
            student_id = file.replace(".npy", "")
            known_ids.append(student_id)
            known_encodings.append(
                np.load(os.path.join(ENCODINGS_DIR, file))
            )

    return known_encodings, known_ids


def send_attendance(student_id):
    payload = {
        "student_id": int(student_id),
        "session_id": SESSION_ID
    }

    try:
        res = requests.post(API_URL, json=payload, timeout=3)
        print("📡", res.json())
    except Exception as e:
        print("❌ Failed:", e)


def recognize_faces():
    known_encodings, known_ids = load_known_faces()

    if not known_encodings:
        print("❌ No registered faces")
        return

    cam = cv2.VideoCapture(0)
    marked_students = set()

    print("📸 Camera ON | Press Q to quit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb, model=MODEL)
        encodings = face_recognition.face_encodings(rgb, locations)

        for (top, right, bottom, left), encoding in zip(locations, encodings):
            distances = face_recognition.face_distance(
                known_encodings, encoding
            )
            best_match = np.argmin(distances)

            label = "Unknown"

            if distances[best_match] < TOLERANCE:
                student_id = known_ids[best_match]
                label = f"ID: {student_id}"

                if student_id not in marked_students:
                    send_attendance(student_id)
                    marked_students.add(student_id)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame, label, (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )

        cv2.imshow("AI Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognize_faces()
