import cv2
import numpy as np

evt = -1  # done coz initially there will be no value and program will crash


def mouseClick(event, mouseX, mouseY, flags, params):
    # mouseClick takes 5 parameters, only first three are useful for now
    # use the "event" to define the event u want to capture
    # mouseX,mouseY is position of mouse on ur frame
    global evt
    global mousePos  # defing global variables, so we can use them
    # in the frame loop
    # evt = event

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Mouse Event Was: ", event)
        print("at Position: ", mouseX, mouseY)
        mousePos = (mouseX, mouseY)
        evt = event
    if event == cv2.EVENT_LBUTTONUP:
        print("Mouse Event was: ", event)
        print("at position: ", mouseX, mouseY)
        mousePos = (mouseX, mouseY)
        evt = event
    if event == cv2.EVENT_RBUTTONUP:
        print("u released the right button: ", event)
        mousePos = (mouseX, mouseY)
        evt = event  # now clicking the right button will erase the circle


myCam = cv2.VideoCapture(1)
cv2.namedWindow("webCam")
# u must use this so as to create a window of name,"webCam".or elseu get an error coz "webCam" isnt created yet
cv2.setMouseCallback("webCam", mouseClick)
# this is the listener function ,everytime the mouse is on the frame,
# this event listener will listen to it and call the function mouseClick()
# note this is always listening ,it doesnt have to be inside ur frame loop to work
state = False
while True:
    _, frame = myCam.read()
    # print(evt)

    if evt == 1 or evt == 4:
        cv2.circle(frame, mousePos, 20, (255, 0, 0))
    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

myCam.release()
