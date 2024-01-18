#### here we r creating a moving box on the main frame
#### that bounces of the walls of it
#### create a color box on a gray image

import cv2
import numpy as np
import time as t

cam = cv2.VideoCapture(1)
frame_height = 0
frame_width = 0
if not cam.isOpened():
    print("Error: Could not open video file.")
else:
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

snipH = 60
snipW = 60
boxCC = int(frame_width / 2)  # center of the column
boxCR = int(frame_height / 2)  # center of the row
deltaRow = 5
deltaCol = 5

while True:
    _, frame = cam.read()
    frameROI = frame[
        int(boxCR - snipH / 2) : int(boxCR + snipH / 2),
        int(boxCC - snipW / 2) : int(boxCC + snipW / 2),
    ]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    frame[
        int(boxCR - snipH / 2) : int(boxCR + snipH / 2),
        int(boxCC - snipW / 2) : int(boxCC + snipW / 2),
    ] = frameROI

    if boxCR - snipH / 2 <= 0 or boxCR + snipH / 2 >= frame_height:
        deltaRow = deltaRow * (-1)
    if boxCC - snipW / 2 <= 0 or boxCC + snipW / 2 >= frame_width:
        deltaCol = deltaCol * (-1)
    boxCC += deltaCol
    boxCR += deltaRow
    cv2.rectangle(
        frame,
        (int(boxCC - snipW / 2), int(boxCR - snipH / 2)),
        (int(boxCC + snipW / 2), int(boxCR + snipH / 2)),
        (0, 255, 0),
        2,
    )
    cv2.imshow("ROI", frameROI)
    cv2.moveWindow("ROI", frame_width, 0)
    cv2.imshow("my capture feed", frame)
    cv2.moveWindow("my capture feed", 0, 0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
