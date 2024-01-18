import cv2
import mediapipe as mp
import time
import numpy as np

frame_width = 640
frame_height = 480
myFace = mp.solutions.face_detection.FaceDetection()
drawFace = mp.solutions.drawing_utils
myCam = cv2.VideoCapture(0)
while True:
    _, frame = myCam.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = myFace.process(frameRGB)

    # print(results.detections)
    # now if u look at the data structure generated from this
    # and scroll to the top ,we need to extract 'location_data' and from that 'relative_bounding_box'
    if results.detections != None:
        for face in results.detections:  # extracting data of one face at a time
            # drawFace.draw_detection(frame, face)
            ### this is the regular general method
            # print(face)
            box = face.location_data.relative_bounding_box
            # print the "box" variable and check out its data structure
            x = int(box.xmin * frame_width)
            y = int(box.ymin * frame_height)
            bottomCorner = (
                int((box.xmin + box.width) * frame_width),
                int((box.ymin + box.height) * frame_height),
            )
            cv2.rectangle(frame, (x, y), bottomCorner, (255, 0, 0), 2)
    #         if x <= 0:
    #             x = 10
    #         if y <= 0:
    #             y = 10
    #         frameROI = frame[y : bottomCorner[1], x : bottomCorner[0]]
    # cv2.namedWindow("roi")
    # cv2.imshow("roi", frameROI)
    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", 0, 0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
