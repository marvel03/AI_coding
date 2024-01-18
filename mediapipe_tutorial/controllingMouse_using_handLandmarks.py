import pyautogui
import cv2
import mediapipe as mp
import time
import numpy as np


frame_width = 640
frame_height = 480


class parseMediapipe:
    import mediapipe as mp

    def __init__(self, maxHands=2):  # contructor
        self.myHands = self.mp.solutions.hands.Hands(False, maxHands)

    def getLandmarks(self, frame):
        # u r putting 'self' as a parameter,coz u r making this method non-static
        both_hand_landmarks = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.myHands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for hand_landmarks in results.multi_hand_landmarks:
                single_hand_landmark = []
                for hand_landmark in hand_landmarks.landmark:
                    single_hand_landmark.append(
                        (
                            int(frame_width * hand_landmark.x),
                            int(frame_height * hand_landmark.y),
                        )
                    )
                both_hand_landmarks.append(single_hand_landmark)
        return both_hand_landmarks


cam = cv2.VideoCapture(1)
###creating an object
myHands = parseMediapipe()  # can put no. of hands , but default i defined is 2
###
lTime = time.time()
fpsFiltered = 30

if not cam.isOpened():
    print("Error: Could not open video file.")
else:
    # Get the frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Frame Size:", frame_width, "x", frame_height)
xPos = frame_width
yPos = frame_height

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    dt = time.time() - lTime
    fps = int(np.floor(1 / dt))
    fpsFiltered = int(np.floor(0.9 * fpsFiltered + 0.1 * fps))
    lTime = time.time()
    ############
    handData = myHands.getLandmarks(frame)
    for hands in handData:
        cv2.circle(frame, hands[8], 10, (255, 0, 0), 2)
        xPos = hands[8][0]
        yPos = hands[8][1]
    # print(handData)
    pyautogui.moveTo(xPos, yPos, 0.0001)
    cv2.putText(
        frame,
        "fps: {}".format(fpsFiltered),
        (20, 20),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 0, 0),
        1,
    )
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
