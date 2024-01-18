import cv2
import numpy as np


# here we simply create n number of masks and then OR(add) them together use the symbol '|'


def onTrack1(val):
    global hueLow
    hueLow = val
    print("hue low of mask 1: ", hueLow)


def onTrack2(val):
    global hueHigh
    hueHigh = val
    print("hue high of mask 1: ", hueHigh)


def onTrack3(val):
    global satLow
    satLow = val
    print("saturation low of mask 1: ", satLow)


def onTrack4(val):
    global satHigh
    satHigh = val
    print("saturation high of mask 1: ", satHigh)


def onTrack5(val):
    global valLow
    valLow = val
    print("value low of mask 1: ", valLow)


def onTrack6(val):
    global valHigh
    valHigh = val
    print("value high of mask 1: ", valHigh)


def onTrack7(val):
    global HueLow2
    HueLow2 = val
    print("hue low of 2nd mask :", HueLow2)


def onTrack8(val):
    global HueHigh2
    HueHigh2 = val
    print("hue High of 2nd mask :", HueHigh2)


def onTrack9(val):
    global satLow2
    satLow2 = val
    print("saturation low of 2nd mask: ", satLow2)


def onTrack10(val):
    global satHigh2
    satHigh2 = val
    print("saturation low of 2nd mask: ", satHigh2)


def onTrack11(val):
    global valLow2
    valLow2 = val
    print("value low of 2nd mask: ", valLow2)


def onTrack12(val):
    global valHigh2
    valHigh2 = val
    print("value low of 2nd mask: ", valHigh2)


frame_width = 640
frame_height = 480
cam = cv2.VideoCapture(1)


cv2.namedWindow("mask Parameters")
cv2.moveWindow("mask Parameters", frame_width, 0)
cv2.resizeWindow("mask Parameters", int(frame_width / 2), frame_height)

cv2.createTrackbar("Hue low 1", "mask Parameters", 10, 179, onTrack1)
cv2.createTrackbar("Hue high 1", "mask Parameters", 20, 179, onTrack2)
cv2.createTrackbar("Hue low 2", "mask Parameters", 10, 179, onTrack7)
cv2.createTrackbar("Hue high 2", "mask Parameters", 20, 179, onTrack8)

cv2.createTrackbar("Sat low 1", "mask Parameters", 10, 255, onTrack3)
cv2.createTrackbar("Sat high 1", "mask Parameters", 250, 255, onTrack4)
cv2.createTrackbar("Sat low 2", "mask Parameters", 10, 255, onTrack9)
cv2.createTrackbar("Sat high 2", "mask Parameters", 250, 255, onTrack10)

cv2.createTrackbar("val low 1", "mask Parameters", 10, 255, onTrack5)
cv2.createTrackbar("val high 1", "mask Parameters", 250, 255, onTrack6)
cv2.createTrackbar("val low 2", "mask Parameters", 10, 255, onTrack11)
cv2.createTrackbar("val high 2", "mask Parameters", 250, 255, onTrack12)

myCam = cv2.VideoCapture(1)

while True:
    _, frame = cam.read()
    resizedFrame = cv2.resize(frame, (int(frame_width / 3), int(frame_height / 3)))
    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ####### creating mask 1
    lowerBound1 = np.array([hueLow, satLow, valLow])
    upperBound1 = np.array([hueHigh, satHigh, valHigh])
    mask1 = cv2.inRange(HSVframe, lowerBound1, upperBound1)
    resizedMask1 = cv2.resize(mask1, (int(frame_width / 3), int(frame_height / 3)))
    myObject1 = cv2.bitwise_and(frame, frame, mask=mask1)
    myObject1_resized = cv2.resize(
        myObject1, (int(frame_width / 3), int(frame_height / 3))
    )
    cv2.imshow("mask 1", myObject1_resized)
    cv2.moveWindow("mask 1", int(frame_width / 3), int(frame_height))
    ########
    ########### creating mask 2
    lowerBound2 = np.array([HueLow2, satLow2, valLow2])
    upperBound2 = np.array([HueHigh2, satHigh2, valHigh2])
    mask2 = cv2.inRange(HSVframe, lowerBound2, upperBound2)
    resizedMask2 = cv2.resize(mask2, (int(frame_width / 3), int(frame_height / 3)))
    myObject2 = cv2.bitwise_and(frame, frame, mask=mask2)
    myObject2_resized = cv2.resize(
        myObject2, (int(frame_width / 3), int(frame_height / 3))
    )
    cv2.imshow("mask 2", myObject2_resized)
    cv2.moveWindow("mask 2", 2 * int(frame_width / 3), int(frame_height))
    ###########
    cv2.imshow("main capture", resizedFrame)
    cv2.moveWindow("main capture", 0, frame_height)

    ##### final detection frame
    finalFrame = myObject1 | myObject2
    # OR both the frames to get both the frames in one single frame
    cv2.imshow("final detection frame", finalFrame)
    cv2.moveWindow("final detection frame", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
