import time
import cv2
import mediapipe as mp
from .angles import calculate_angle
from .counter import RepCounter
from . import db
import json

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def get_point(landmarks, side, joint, w, h):
    index = getattr(mp_pose.PoseLandmark, f'{side}_{joint}').value
    return (landmarks[index].x * w, landmarks[index].y * h)

def run(exercise, side='LEFT'):
    counter = RepCounter(exercise)
    cap = cv2.VideoCapture(0)
    started = time.time()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            h, w = frame.shape[:2]
            result = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if result.pose_landmarks:
                lms = result.pose_landmarks.landmark
                a, b, c = (get_point(lms, side, j, w, h) for j in counter.cfg['joints'])
                angle = calculate_angle(a, b, c)
                counter.update(angle)
                mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                cv2.putText(frame, f'Angle: {int(angle)}', (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f'{exercise.upper()}  Reps: {counter.reps}', (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'Press Q to finish and save', (20, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.imshow('Workout Rep Tracker', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    if counter.reps > 0:
        db.add_session(
            exercise, 
            counter.reps, 
            int(time.time() - started), 
            round(counter.total_tut, 1), 
            json.dumps(counter.rep_data)
        )
    return counter.reps