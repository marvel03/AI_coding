import cv2
import mediapipe as mp
import time
import numpy as np

frame_width = 640
frame_height = 480
cam = cv2.VideoCapture(1)

# myHands = mp.solutions.hands.Hands(
#     False,  # if its static image then "true",as we r dealing with video then 'false'
#     2,  # detect 2 hands (use even no. only)
#     0.5,  # these 2 are confidence parameters
#     0.5,
# )
myHands = mp.solutions.hands.Hands(False, 2)
mpDraw = mp.solutions.drawing_utils
lTime = time.time()
fpsFiltered = 30
while True:
    _, frame = cam.read()
    dt = time.time() - lTime
    fps = int(np.floor(1 / dt))
    fpsFiltered = int(np.floor(fpsFiltered * 0.9 + 0.1 * fps))
    lTime = time.time()

    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(
        frame, cv2.COLOR_BGR2RGB
    )  # coz by opencv uses BGR, but mediapipe uses RBG
    results = myHands.process(
        frameRGB
    )  # collect all data regarding hands from the frame
    ## note: this "results" is a very complex data structure
    ## so we gotta break it down, inorder to use it ,there are predefined function for this
    if results.multi_hand_landmarks != None:
        ##check if any data is present bout hand landmarks in "results"
        for hand_landmarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(
                frame,  # frame on which u wanna draw on
                hand_landmarks,  # joint points
                mp.solutions.hands.HAND_CONNECTIONS,  # CREATES connections between each joint
            )
    cv2.putText(
        frame,
        "fps: {}".format(fpsFiltered),
        (20, 20),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 0, 0),
        1,
    )
    cv2.imshow("cam feed", frame)
    cv2.moveWindow("cam feed", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()

####### analysing the data structure from 'results'
# while True:
#     _, frame = cam.read()
#     frame = cv2.flip(frame, 1)
#     frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = myHands.process(frame)
#     # print(results)
#     if results.multi_hand_landmarks != None:
#         for hand_landmarks in results.multi_hand_landmarks:
#             print(hand_landmarks)
#             # on printing u will see this is an array 21 tuples(subarrays),each representing a joint coordinate on the frame
#             # each tuple is called landmark(predefind)
#             # it looks like this-> [landmark{x:,y:,z:},landmark{..},...],print it and check
#             # u can also acess each landmark individually
#             for landmarks in hand_landmarks.landmark:
#                 print("x: ", landmarks.x, "y: ", landmarks.y)
#                 # now note all these are normalized values, so they lie between 0 and 1 ,u gotta scale it based on window resolution ok
#     cv2.imshow("cam feed", frame)
#     cv2.moveWindow("cam feed", 0, 0)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# cam.release()
