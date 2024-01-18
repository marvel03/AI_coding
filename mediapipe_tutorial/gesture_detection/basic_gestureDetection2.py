## what we do here calc the distance between certain keypoints on ur hand
## and train our model based on these distance values (euclidien distance )
## so when we do live feed , we will compare the distance between eac key point , and based on some tolerance value
## we classify it

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


def findDistances(handData):
    distances = []
    for hand in handData:
        dists = []
        for j in range(0, len(hand)):
            d = []
            for i in range(0, len(hand)):
                dist = round(
                    ((hand[j][0] - hand[i][0]) ** 2 + (hand[j][1] - hand[i][1]) ** 2)
                    ** 0.5
                )
                d.append(dist)
            dists.append(d)
        distances.append(dists)
        # print("next hand")
    # print(distances)
    # print("done")
    return distances


def distanceError(knownGestures, unknownGestures, keyPoints):
    error = 0
    for knownGesture, unknownGesture in zip(knownGestures, unknownGestures):
        for row in keyPoints:
            for col in keyPoints:
                error = error + abs(knownGesture[row][col] - unknownGesture[row][col])
    print(error)
    return error


def detectGestures(unknownGesture, saved_gestures, keyPoints, gesture_names, tolerance):
    err = 10000000000
    min_index = 0
    i = 0
    for saved_gesture in saved_gestures:
        temp = distanceError(unknownGesture, saved_gesture, keyPoints)
        if temp < err:
            err = temp
            min_index = i
        i = i + 1
    print(gesture_names[i])
    return gesture_names[i]


keyPoints = [4, 8, 12, 16, 20, 0, 5, 9, 13, 17, 1]
cam = cv2.VideoCapture(1)
mp = parseMediapipe(1)
train = False
gesture_names = ["one", "two", "three", "four"]
trainCounter = 0
saved_gestures = []
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    both_hand_landmarks, hand_names = mp.get_hand_landmarks(frame, False)
    for hand_landmarks in both_hand_landmarks:
        for tip in keyPoints:
            cv2.circle(frame, hand_landmarks[tip], 10, (0, 255, 0), 3)
    # gestureDistances = findDistances(both_hand_landmarks)
    if train == False:
        if both_hand_landmarks != []:
            print("press t to train for : " + gesture_names[trainCounter])
            if cv2.waitKey(1) & 0xFF == ord("t"):
                knownGestures = findDistances(both_hand_landmarks)
                saved_gestures.append(
                    knownGestures[0]
                )  # im doing only for one hand now
                trainCounter = trainCounter + 1
                if trainCounter == len(gesture_names):
                    train = True
    elif train == True:
        if both_hand_landmarks != []:
            name = detectGestures(
                findDistances(both_hand_landmarks)[0],
                saved_gestures,
                keyPoints,
                gesture_names,
                1500,
            )

    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
