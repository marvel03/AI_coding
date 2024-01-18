import cv2
import numpy as np

myCam = cv2.VideoCapture(1)
frame_width = 640
frame_hieght = 540

while True:
    frame = np.zeros([frame_hieght, frame_width, 3], dtype=np.uint8)
    for x in range(0, frame_width):
        for y in range(0, frame_hieght):
            hue = np.interp(x, [0, frame_width], [0, 180])
            saturation = np.interp(y, [0, frame_hieght], [0, 255])
            frame[y, x] = (hue, saturation, 255)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    cv2.imshow("hue chart", frame)
    cv2.moveWindow("hue chart", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
