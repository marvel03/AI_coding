import cv2
import mediapipe as mp
import time
import numpy as np

### now understand that the data structures we get here are all the same
### as the hand detection model , so learn and refer that first if u forgot how all this works
frame_width = 640
frame_height = 480

Pose = mp.solutions.pose.Pose(  ## create ur pose model instance
    False,  # is it static image or not
    False,  # do u want only upper body or not
    True,  # to smooth the values
)
mp_Draw = mp.solutions.drawing_utils
myCam = cv2.VideoCapture(1)
fpsFiltered = 30
lTime = time.time()
# while True:
#     _, frame = myCam.read()
#     frame = cv2.flip(frame, 1)
#     frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     results = Pose.process(frameRGB)
#     if results.pose_landmarks != None:
#         # mp_Draw.draw_landmarks(frame, results.pose_landmarks)# this will draw the dots
#         mp_Draw.draw_landmarks(
#             frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
#         )  # THIS WILL DRAW ALL THE CONNECTIONS TOO

#     cv2.imshow("webcam", frame)
#     cv2.moveWindow("webcam", 0, 0)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# myCam.release()


### analysis of the data structure
while True:
    _, frame = myCam.read()
    dt = time.time() - lTime
    fps = np.floor(1 / dt)
    fpsFiltered = np.floor(0.9 * fpsFiltered + 0.1 * fps)
    lTime = time.time()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = Pose.process(frameRGB)
    full_body_landmarks = []
    if results.pose_landmarks != None:
        ## note: unlike the hand model ,this model only analysis one body
        ## so it does not return an array of array of landmarks,just an array of landmarks
        # print(results.pose_landmarks)# u can see this here, this is just a list of values
        for lm in results.pose_landmarks.landmark:
            # landmarks = (lm.x, lm.y)
            # print(landmarks)  # all these are normalized values
            landmarks = (int(lm.x * frame_width), int(lm.y * frame_height))
            full_body_landmarks.append(landmarks)
        # say we want to plot the nose only
        cv2.circle(frame, full_body_landmarks[0], 10, (255, 0, 0), 2)
        # and for the eyes
        cv2.circle(frame, full_body_landmarks[5], 5, (0, 255, 0), -1)
        cv2.circle(frame, full_body_landmarks[2], 5, (0, 255, 0), -1)
    # print(full_body_landmarks)
    cv2.putText(
        frame,
        "FPS: {}".format(fpsFiltered),
        (25, 25),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 0, 0),
        1,
    )
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

myCam.release()
