import cv2
import numpy as np
import mediapipe as mp

frame_width = 640
frame_height = 480

faceMesh = mp.solutions.face_mesh.FaceMesh(
    False, 4  # static image or not,  # max faces to be detected
)
mpDraw = mp.solutions.drawing_utils
####### controlling the drawing utility output
drawSpecCircle = mpDraw.DrawingSpec(thickness=1, circle_radius=0, color=(255, 0, 0))
drawSpecLine = mpDraw.DrawingSpec(thickness=1, circle_radius=0, color=(0, 0, 255))
#######
cam = cv2.VideoCapture(1)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)
    # print(results.multi_face_landmarks)
    if results.multi_face_landmarks != None:
        # note u have an array , containing info bout all the max faces
        # so u have to step through each face individually
        for face_landmarks in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                frame,
                face_landmarks,
                mp.solutions.face_mesh.FACEMESH_TESSELATION,
                drawSpecLine,  # these are the parameters u setup manually
                drawSpecCircle,  ## this too
            )
            index = 0
            for landmark in face_landmarks.landmark:
                # we put numbers on each landmark,just to check their index number
                cv2.putText(
                    frame,
                    str(index),
                    (int(landmark.x * frame_width), int(landmark.y * frame_height)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.2,
                    (0, 255, 0),
                    1,
                )
                index = index + 1

    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
