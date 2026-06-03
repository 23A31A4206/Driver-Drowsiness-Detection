import cv2
import mediapipe as mp
import time
import winsound
import pyttsx3

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

engine = pyttsx3.init()

eye_closed_start = None
drowsy_count = 0
drowsiness_detected = False
safety_score = 100

warning_alert_given = False
critical_alert_given = False

while True:
    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            x_min, y_min = w, h
            x_max, y_max = 0, 0

            for landmark in face_landmarks.landmark:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

            cv2.rectangle(
                frame,
                (x_min, y_min),
                (x_max, y_max),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Driver Detected",
                (x_min, y_min - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            left_top = face_landmarks.landmark[159]
            left_bottom = face_landmarks.landmark[145]

            eye_distance = abs(left_top.y - left_bottom.y)

            if eye_distance < 0.01:

                if eye_closed_start is None:
                    eye_closed_start = time.time()

                elapsed = time.time() - eye_closed_start

                if elapsed > 2:

                    cv2.putText(
                        frame,
                        "DROWSINESS ALERT!",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                    winsound.Beep(1000, 500)

                    if not drowsiness_detected:
                        drowsy_count += 1
                        safety_score = max(0, safety_score - 5)
                        drowsiness_detected = True

            else:
                eye_closed_start = None
                drowsiness_detected = False

    cv2.rectangle(frame, (10, 10), (330, 60), (255, 255, 255), -1)

    cv2.putText(
        frame,
        f"Drowsiness Events: {drowsy_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2
    )

    cv2.rectangle(frame, (10, 70), (280, 120), (255, 255, 255), -1)

    cv2.putText(
        frame,
        f"Safety Score: {safety_score}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2
    )

    if safety_score <= 60:

        cv2.putText(
            frame,
            "TAKE A BREAK",
            (50, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        if not warning_alert_given:
            engine.say("Attention Driver! Please take a break immediately.")
            engine.runAndWait()
            warning_alert_given = True

    if safety_score <= 40:

        cv2.putText(
            frame,
            "CRITICAL FATIGUE DETECTED",
            (50, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            3
        )

        if not critical_alert_given:
            engine.stop()

            engine.say(
                "Critical fatigue detected. Attention driver. Please take a break immediately."
            )

            engine.runAndWait()

            critical_alert_given = True

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()