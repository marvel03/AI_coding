import cv2
import numpy as np
import time as t

frame_height = 0
frame_width = 0

myCam = cv2.VideoCapture(1)
# to get frame height and width
if not myCam.isOpened():
    print("Error: Could not open video file.")
else:
    frame_width = int(myCam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(myCam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frame_height)
print(frame_width)
tLast = t.time()
FPS_filtered = 30
while True:
    _, frame = myCam.read()
    dt = t.time() - tLast
    FPS = int(np.floor(1 / dt))
    FPS_filtered = int(FPS_filtered * 0.9 + FPS * 0.1)
    tLast = t.time()
    #############defining a ROI
    frameGrayROI = frame[250:400, 200:360]
    frameGrayROI = cv2.cvtColor(
        frameGrayROI, cv2.COLOR_BGR2GRAY
    )  # converting the ROI TO gray
    # noe inorder attach this ROI BACK TO THE MAIN FRAME
    # U MUST CONVERT IT TO BGR, but note: ur ROI will not get its color info back,it only \
    # changes its shape
    frameGray2BGR_ROI = cv2.cvtColor(frameGrayROI, cv2.COLOR_GRAY2BGR)
    # attaching it back to the main frame
    frame[250:400, 200:360] = frameGray2BGR_ROI
    # or else u can attach somewhere else on ur main frame
    frame[0 : 400 - 250, 0 : 360 - 200] = frameGray2BGR_ROI
    # make sure the shape matches else u get a shape mismatch error
    cv2.imshow("my gray ROI", frameGrayROI)
    cv2.moveWindow("my gray ROI", 640, 0)

    ############################
    mytext2 = "FPS: {}".format(FPS_filtered)
    cv2.putText(frame, mytext2, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("actual Frame", frame)
    cv2.moveWindow("actual Frame", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
