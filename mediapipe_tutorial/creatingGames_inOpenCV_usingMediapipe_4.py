import cv2
import numpy as np
import time

# we are creating a ping pong game

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
myHands = parseMediapipe(1)  # can put no. of hands , but default i defined is 2
###
lTime = time.time()
fpsFiltered = 30

### seting the paddle dimensions
paddleWidth = 50
paddleHeight = 10
paddleColor = (0, 0, 255)

###
xPos = int(frame_width / 2)
yPos = int(frame_height / 2)
radius = 20
deltaPosX = 5
deltaPosY = 5
score = 0
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    dt = time.time() - lTime
    fps = int(np.floor(1 / dt))
    fpsFiltered = int(np.floor(0.9 * fpsFiltered + 0.1 * fps))
    lTime = time.time()
    ##################################
    cv2.putText(
        frame,
        str(score),
        (25, int(6 * paddleHeight)),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        paddleColor,
        1,
    )

    handData = myHands.getLandmarks(frame)
    for hand in handData:
        # remember this will be an array of size = no. of hands being proccessed
        cv2.rectangle(
            frame,
            (hand[8][0] - int(paddleWidth / 2), 0),
            (hand[8][0] + int(paddleWidth / 2), paddleHeight),
            paddleColor,
            -1,
        )
        cv2.circle(frame, hand[8], 10, (255, 0, 0), -1)
        # follow the 8th joint, y coordinates

    cv2.circle(frame, (xPos, yPos), radius, (0, 255, 0), -1)
    if xPos + radius >= frame_width or xPos - radius <= 0:
        deltaPosX = deltaPosX * (-1)

    if yPos + radius >= frame_height:
        deltaPosY = deltaPosY * (-1)

    # if yPos - radius <= 0:
    #     score = score - 1
    #     deltaPosY = deltaPosY * (-1)

    if yPos - radius <= paddleHeight:
        if xPos >= int(hand[8][0] - paddleWidth / 2 - radius) and xPos <= int(
            hand[8][0] + paddleWidth / 2 + radius
        ):
            deltaPosY = deltaPosY * (-1)
            score = score + 1
        else:
            # xPos = int(frame_width / 2)
            # yPos = int(frame_height / 2)
            deltaPosY = deltaPosY * (-1)
            score = score - 1

    xPos += deltaPosX
    yPos += deltaPosY
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
