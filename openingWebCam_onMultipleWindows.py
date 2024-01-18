import cv2

myCam = cv2.VideoCapture(1)
while True:
    ignore, frame = myCam.read()
    ######################
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ######################
    cv2.imshow("window1(BGR)", frame)
    cv2.imshow("window2(GRAYSCALE)", grayFrame)
    cv2.imshow("window3(HSV)", hsvFrame)
    cv2.resizeWindow("window1(BGR)", 480, 480)
    cv2.moveWindow("window1(BGR)", 0, 0)
    cv2.resizeWindow("window2(GRAYSCALE)", 480, 480)
    cv2.moveWindow("window2(GRAYSCALE)", 480, 0)
    cv2.resizeWindow("window3(HSV)", 480, 480)
    cv2.moveWindow("window3(HSV)", 2 * 480, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
