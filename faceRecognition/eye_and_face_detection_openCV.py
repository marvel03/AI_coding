import cv2
import numpy as np
import time

faceCascade = cv2.CascadeClassifier(
    r"C:\myCodes\AI_coding\AIvenv_3.11\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
)
eyeCascade = cv2.CascadeClassifier(
    r"C:\myCodes\AI_coding\AIvenv_3.11\Lib\site-packages\cv2\data\haarcascade_eye.xml"
)
cam = cv2.VideoCapture(1)
frame_width = 640
frame_height = 480

Ltime = time.time()
fpsFiltered = 30
while True:
    _, frame = cam.read()
    dt = time.time() - Ltime
    fps = int(np.floor(1 / dt))
    Ltime = time.time()
    fpsFiltered = int(0.9 * fpsFiltered + 0.1 * fps)

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frame, 1.3, 5)
    # for face in faces:
    #     x, y, w, h = face
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    ####eye detection
    ##1st technique (computionally hectic)
    # eyes = eyeCascade.detectMultiScale(frame, 1.3, 5)
    # for eye in eyes:
    #     x, y, w, h = eye
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    ###2nd technique (computionally efficient, but its based on the fact that ur eyes are always on ur face)
    ## here instead of scanning the entire frame ,we create a ROI, and
    ## only scan that region
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        frameROI = frame[y : y + h, x : x + w]
        grayframeROI = cv2.cvtColor(frameROI, cv2.COLOR_BGR2GRAY)
        eyes = eyeCascade.detectMultiScale(
            grayframeROI, 1.3, 5
        )  # u can even use the default parameters, ie: no 2nd and 3rd paramater
        for eye in eyes:
            xeye, yeye, weye, heye = eye
            cv2.rectangle(
                frame[y : y + h, x : x + w],  # be careful bout where u draw it
                (xeye, yeye),
                (xeye + weye, yeye + heye),
                (0, 0, 255),
                2,
            )

    cv2.putText(
        frame,
        "fps:{}".format(fpsFiltered),
        (10, 30),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 0, 0),
        1,
    )
    cv2.rectangle(frame, (0, 0), (100, 40), (255, 0, 0), 2)
    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
### note : u can try the other haar files available, remember
### all them of them have similar outputs only
