import cv2
import face_recognition
import numpy as np
import os
from pynput import keyboard
import threading
import time

ENCODINGS_DIR = "encodings"
os.makedirs(ENCODINGS_DIR, exist_ok=True)

def register_face(student_id):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        print("❌ Camera not accessible")
        return

    window_name = "Register Face"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)

    print("\n📸 Camera ON")
    print("👉 Press:")
    print(" S = Save face")
    print(" Q = Quit\n")

    key_pressed = {'value': None}
    lock = threading.Lock()

    def on_press(key):
        try:
            if key.char.lower() in ('s', 'q'):
                with lock:
                    key_pressed['value'] = key.char.lower()
        except:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    time.sleep(0.5)  # allow window to initialize

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("❌ Failed to read camera frame")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(
                rgb,
                number_of_times_to_upsample=0,
                model='hog'
            )

            for top, right, bottom, left in face_locations:
                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    (0, 255, 0),
                    2
                )

            cv2.imshow(window_name, frame)

            # IMPORTANT: this makes the window visible
            if cv2.waitKey(1) & 0xFF == 27:
                break

            with lock:
                pressed = key_pressed['value']
                key_pressed['value'] = None

            if pressed == 'q':
                print("❌ Quit without saving")
                break

            if pressed == 's':
                print("🔍 Processing face...")

                if len(face_locations) != 1:
                    print("⚠️ Ensure EXACTLY ONE face is visible")
                    continue

                print("⏳ Encoding face...")
                try:
                    encoding = face_recognition.face_encodings(
                        rgb, face_locations, num_jitters=1
                    )[0]
                except IndexError:
                    print("❌ Could not encode face. Try again.")
                    continue

                print("💾 Saving face...")
                path = os.path.join(ENCODINGS_DIR, f"{student_id}.npy")
                np.save(path, encoding)

                print(f"✅ Face registered successfully: {path}")
                break

    finally:
        listener.stop()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    student_id = input("Enter Student ID: ").strip()
    register_face(student_id)
