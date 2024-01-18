import cv2
import numpy as np

# u can use this for making gesture based tracking games


def onTrack1(val):
    global hueLow
    hueLow = val
    print("hue low: ", hueLow)


def onTrack2(val):
    global hueHigh
    hueHigh = val
    print("hue high: ", hueHigh)


def onTrack3(val):
    global satLow
    satLow = val
    print("saturation low: ", satLow)


def onTrack4(val):
    global satHigh
    satHigh = val
    print("saturation high: ", satHigh)


def onTrack5(val):
    global valLow
    valLow = val
    print("value low: ", valLow)


def onTrack6(val):
    global valHigh
    valHigh = val
    print("value high: ", valHigh)


frame_width = 640
frame_height = 480
cam = cv2.VideoCapture(1)

cv2.namedWindow("my Trackbars")
cv2.moveWindow("my Trackbars", frame_width, 0)
cv2.createTrackbar("Hue low", "my Trackbars", 137, 179, onTrack1)
cv2.createTrackbar("Hue high", "my Trackbars", 179, 179, onTrack2)
cv2.createTrackbar("Sat low", "my Trackbars", 57, 255, onTrack3)
cv2.createTrackbar("Sat high", "my Trackbars", 250, 255, onTrack4)
cv2.createTrackbar("val low", "my Trackbars", 43, 255, onTrack5)
cv2.createTrackbar("val high", "my Trackbars", 219, 255, onTrack6)
xPos = 0
yPos = 0
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ################ creating the mask
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    resizedMaskFrame = cv2.resize(myMask, (int(frame_width / 4), int(frame_height / 4)))
    cv2.namedWindow("my mask")
    cv2.moveWindow("my mask", int(frame_width / 4), frame_height)
    cv2.imshow("my mask", resizedMaskFrame)
    contours, ignore = cv2.findContours(
        myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    # cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            xPos = x
            yPos = y
            xPos = xPos / frame_width
            yPos = yPos / frame_height
            # by doing this u create a relative scaling for the position of the object in the frame
            xPos = int((1920 * xPos) / 2)
            yPos = int((1080 * yPos) / 2)  # scaling it based on ur screen resolution
    ################

    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", xPos, yPos)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
