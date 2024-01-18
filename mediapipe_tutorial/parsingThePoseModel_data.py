import numpy as np
import time
import cv2


frame_width = 640
frame_height = 480


class parsePoseModel:
    import mediapipe as mp

    def __init__(self):
        self.myPose = self.mp.solutions.pose.Pose(False, False, True)

    def get_body_landmarks(self, frame):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myPose.process(frameRGB)
        full_body_landmarks = []
        if results.pose_landmarks != None:
            for lm in results.pose_landmarks.landmark:
                landmarks = (int(lm.x * frame_width), int(lm.y * frame_height))
                full_body_landmarks.append(landmarks)
        return full_body_landmarks


cam = cv2.VideoCapture(1)
poseModel = parsePoseModel()
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    full_body_landmarks = poseModel.get_body_landmarks(frame)
    # print(full_body_landmarks)
    if full_body_landmarks:
        cv2.circle(frame, full_body_landmarks[0], 10, (0, 0, 0), -1)
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
