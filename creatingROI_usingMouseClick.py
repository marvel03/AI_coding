import cv2
import numpy as np

evt = -1


def mouseClick(event, mouseX, mouseY, flags, params):
    global evt
    global mousePos
    mousePos = (mouseX, mouseY)
    print(mousePos)
    if event == cv2.EVENT_LBUTTONDOWN:
        evt = event
        print("u clicked the lbutton at ", (mouseX, mouseY))
        mousePos = (mouseX, mouseY)
    if event == cv2.EVENT_LBUTTONUP:
        evt = event
        print("u released the lbutton at :", (mouseX, mouseY))
        mousePos = (mouseX, mouseY)
    if event == cv2.EVENT_RBUTTONUP:
        evt = event
        print("u released the rbutton")


myCam = cv2.VideoCapture(1)
cv2.namedWindow("webCam")
cv2.setMouseCallback("webCam", mouseClick)
state = False

while True:
    _, frame = myCam.read()
    if evt == 1 and state == False:
        state = True
        initialPos = mousePos

    if state == True and evt == 1:
        cv2.rectangle(frame, initialPos, mousePos, (0, 255, 0), 3)

    if state == True and evt == 4:
        finalPos = mousePos
        state = False
    if evt == 4 and state == False:
        cv2.rectangle(frame, initialPos, finalPos, (0, 255, 0), 3)
        frameROI = frame[initialPos[1] : finalPos[1], initialPos[0] : finalPos[0]]

        cv2.imshow("ROI", frameROI)
        cv2.resizeWindow(
            "ROI", finalPos[0] - initialPos[0], finalPos[1] - initialPos[1]
        )  # the width of the window has limited minimum value, so may get a problem while cropping extremly widths
        cv2.moveWindow("ROI", 640, 0)
    if evt == 5 and state == False:
        # now on releasing the right click u can freeze ur ROI
        cv2.imshow("ROI", frameROI)
        cv2.resizeWindow(
            "ROI", finalPos[0] - initialPos[0], finalPos[1] - initialPos[1]
        )  # the width of the window has limited minimum value, so may get a problem while cropping extremly widths
        cv2.moveWindow("ROI", 640, 0)

    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", 0, 0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
