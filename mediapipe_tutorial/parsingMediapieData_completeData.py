import cv2
import numpy as np
import time

frame_width = 640
frame_height = 480


class parseMediapipe:
    import mediapipe as mp

    def __init__(self, maxHands=2):
        self.myHands = self.mp.solutions.hands.Hands(False, maxHands)
        self.myPose = self.mp.solutions.pose.Pose(False, False, True)
        self.mp_Draw = self.mp.solutions.drawing_utils
        self.myFace = self.mp.solutions.face_detection.FaceDetection()

    def get_hand_landmarks(self, frame, draw=False):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myHands.process(frameRGB)
        both_hand_landmarks = []
        hand_name = []
        if results.multi_hand_landmarks != None:
            for handType in results.multi_handedness:
                for handlabel in handType.classification:
                    # print(handlabel.label)
                    hand_name.append(handlabel.label)

            for hand_landmarks in results.multi_hand_landmarks:
                if draw == True:
                    self.mp_Draw.draw_landmarks(
                        frame,  # frame on which u wanna draw on
                        hand_landmarks,  # joint points
                        self.mp.solutions.hands.HAND_CONNECTIONS,  # CREATES connections between each joint
                    )
                single_hand_landmark = []
                for hand in hand_landmarks.landmark:
                    single_hand_landmark.append(
                        (int(hand.x * frame_width), int(hand.y * frame_height))
                    )
                both_hand_landmarks.append(single_hand_landmark)

        return both_hand_landmarks, hand_name

    def get_pose_landmarks(self, frame, draw=False):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myPose.process(frameRGB)
        pose_landmarks = []
        if results.pose_landmarks != None:
            if draw == True:
                self.mp_Draw.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp.solutions.pose.POSE_CONNECTIONS,
                )
            for lm in results.pose_landmarks.landmark:
                pose_landmarks.append(
                    (int(lm.x * frame_width), int(lm.y * frame_height))
                )
        # print(pose_landmarks)
        return pose_landmarks

    def detect_face(self, frame):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myFace.process(frame)
        box = []
        if results.detections:
            for face in results.detections:
                faceBox = face.location_data.relative_bounding_box
                topCorner = (
                    int(faceBox.xmin * frame_width),
                    int(faceBox.ymin * frame_height),
                )
                bottomCorner = (
                    int((faceBox.xmin + faceBox.width) * frame_width),
                    int((faceBox.ymin + faceBox.height) * frame_height),
                )
                box.append((topCorner, bottomCorner))
            print(box)
        return box


cam = cv2.VideoCapture(1)
mp = parseMediapipe(2)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    both_hand_landmarks, hand_names = mp.get_hand_landmarks(frame, False)
    # pose_landmarks = mp.get_pose_landmarks(frame)
    face_box = mp.detect_face(frame)
    # for hand, hand_name in zip(both_hand_landmarks, hand_names):
    #     cv2.putText(
    #         frame, hand_name, hand[0], cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 0), 1
    #     )
    # if pose_landmarks:
    #     for pose_landmark in pose_landmarks:
    #         cv2.circle(frame, pose_landmark, 5, (255, 0, 0), -1)
    if face_box:
        for face in face_box:
            cv2.rectangle(frame, face[0], face[1], (0, 255, 0), 3)
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
