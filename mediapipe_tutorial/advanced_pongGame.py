import numpy as np
import cv2
import time

frame_width = 640
frame_height = 480


class parseMediaPipeData:
    import mediapipe as mp

    def __init__(self, maxHands=2):
        self.myHands = self.mp.solutions.hands.Hands(False, maxHands)

    def getHandData(self, frame):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myHands.process(frame)
        both_hand_landmarks = []
        if results.multi_hand_landmarks != None:
            for hand_landmarks in results.multi_hand_landmarks:
                # print(hand_landmarks)
                single_hand_landmark = []
                for hand_landmark in hand_landmarks.landmark:
                    single_hand_landmark.append(
                        (
                            int(hand_landmark.x * frame_width),
                            int(hand_landmark.y * frame_height),
                        )
                    )
                both_hand_landmarks.append(single_hand_landmark)
        # print(both_hand_landmarks)
        return both_hand_landmarks


deltaPosY = 10
deltaPosX = 10


def checkBounce(x, dx, y, dy, r):
    if y + r >= frame_height or y - r <= 0:
        dy = dy * (-1)
    if x + r >= frame_width or x - r <= 0:
        dx = dx * (-1)
    return dx, dy


cam = cv2.VideoCapture(1)
myHands = parseMediaPipeData(2)
xPos = int(frame_width / 2)
yPos = int(frame_height / 2)

lTime = time.time()
fpsFiltered = 30
while True:
    _, frame = cam.read()
    dt = time.time() - lTime
    fps = int(np.floor(1 / dt))
    lTime = time.time()
    fpsFiltered = np.floor(0.9 * fpsFiltered + 0.1 * fps)
    frame = cv2.flip(frame, 1)
    handData = myHands.getHandData(frame)
    for hand in handData:
        cv2.circle(frame, (hand[8]), 20, (255, 255, 0, 2), 3)
    cv2.circle(frame, (xPos, yPos), 20, (255, 0, 255), -1)
    deltaPosX, deltaPosY = checkBounce(xPos, deltaPosX, yPos, deltaPosY, 20)
    xPos += deltaPosX
    yPos += deltaPosY
    cv2.putText(
        frame,
        "fps: {}".format(fpsFiltered),
        (25, 25),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        1,
    )
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
