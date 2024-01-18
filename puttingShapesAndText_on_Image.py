import cv2
import time as t
import numpy as np

frame_height = 0
frame_width = 0
myText = "hello everyone, i am a bird"
myCam = cv2.VideoCapture(1)
if not myCam.isOpened():
    print("Error: Could not open video file.")
else:
    # Get the frame width and height
    frame_width = int(myCam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(myCam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print("Frame Size:", frame_width, "x", frame_height)
tLast = t.time()
FPS_filtered = 30
while True:
    _, frame = myCam.read()
    dt = t.time() - tLast
    FPS = int(np.floor(1 / dt))
    FPS_filtered = int(FPS_filtered * 0.9 + FPS * 0.1)
    print(FPS_filtered)
    tLast = t.time()
    cv2.rectangle(
        frame,
        (int(frame_width / 2), int(frame_height / 2)),
        (int(frame_width / 2 + 50), int(frame_height / 2 + 100)),
        (0, 255, 0),
        4,
    )  # 2nd parameter is the upper left corner, 3rd is the bottom right corner
    frame[  # we can do it this way too
        int(frame_height / 2) : int(frame_height / 2 + 100),
        int(frame_width / 2) : int(frame_width / 2 + 50),
    ] = [255, 0, 0]
    # frame.circle(frame, "center"(x, y), radius, color, thickness) drawing a circle
    cv2.putText(
        frame,
        myText,
        (int(frame_width / 4), int(frame_height - 100)),
        cv2.FONT_HERSHEY_COMPLEX,
        1,  # font size
        (255, 255, 0),
        1,  # text size
    )
    mytext2 = "FPS: {}".format(FPS_filtered)
    cv2.putText(frame, mytext2, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("turning on ur webCam", frame)
    cv2.moveWindow("turning on ur webCam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
