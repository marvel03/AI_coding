import cv2
import numpy as np
import time

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
        handTypes = []
        if results.multi_hand_landmarks != None:
            ################# inorder for this to work u have to flip the frame that
            # print(results.multi_handedness) # [classification{...},classification{...}]
            ################# look here we will use to view the classifications
            for hand in results.multi_handedness:
                # print(hand)  #classification{...}
                # print(hand.classification)  # [label,index,score]
                # print(hand.classification[0])
                # notice there is only one element in this array
                print(hand.classification[0].label)  # to retrive the label
                handType = hand.classification[0].label
                handTypes.append(handType)

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
        return both_hand_landmarks, handTypes


cam = cv2.VideoCapture(1)
###creating an object
myHands = parseMediapipe(2)  # can put no. of hands , but default i defined is 2
###
lTime = time.time()
fpsFiltered = 30

while True:
    _, frame = cam.read()
    dt = time.time() - lTime
    fps = int(np.floor(1 / dt))
    fpsFiltered = int(np.floor(0.9 * fpsFiltered + 0.1 * fps))
    lTime = time.time()
    frame = cv2.flip(frame, 1)
    handData, handNames = myHands.getLandmarks(frame)
    for hand, handName in zip(handData, handNames):
        # notice in any particular frame the size of "handData" and 'handNames' is gonna be the same
        # and we use zip() to be able to traverse through 2 arrays simultaeneosly
        cv2.putText(
            frame, handName, hand[0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1
        )
        for finger in [4, 8, 12, 16, 20]:
            cv2.circle(frame, hand[finger], 20, (0, 235, 100), 1)
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
