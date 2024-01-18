import cv2
import numpy as np

# so here we r tracking object based on color
# first u gotta convert the frames into HSV ,so that the computer can understand colors
# and this version the training will be done during the captures,
# rather than pre-training


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

# so we set 6 trackbars to train the model based on H,S,V values
# 2 for telling the max and min value of H
# next 2 for min and max value of S
# and finally min and max value of V

cv2.namedWindow("my Trackbars")
cv2.moveWindow("my Trackbars", frame_width, 0)
cv2.createTrackbar("Hue low", "my Trackbars", 10, 179, onTrack1)
cv2.createTrackbar("Hue high", "my Trackbars", 20, 179, onTrack2)
cv2.createTrackbar("Sat low", "my Trackbars", 10, 255, onTrack3)
cv2.createTrackbar("Sat high", "my Trackbars", 250, 255, onTrack4)
cv2.createTrackbar("val low", "my Trackbars", 10, 255, onTrack5)
cv2.createTrackbar("val high", "my Trackbars", 250, 255, onTrack6)

# while True:
#     _, frame = cam.read()
#     # now we gotta create a mask which will contain the upper and lower bound values  of H,S,V
#     # mask will basically check for all the pixels that have matching values with the
#     # upper and lower bound value stored with it
#     # if a pixel matches its description, it mark it white, everything else will be marked black
#     ## how to create a mask
#     frameHSV = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
#     lowerBound = np.array([hueLow, satLow, valLow])
#     upperBound = np.array([hueHigh, satHigh, valHigh])
#     myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
#     cv2.namedWindow("my mask")
#     frameResized = cv2.resize(frame, (int(frame_width / 4), int(frame_height / 4)))
#     # im just making it small
#     cv2.imshow("my mask", myMask)
#     cv2.moveWindow("my mask", 0, 0)
#     cv2.imshow("webCam", frameResized)
#     cv2.moveWindow("webCam", 0, frame_height)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# # u can use this program to check tracking particular colors
# # the tracking will depend on lighting too,so be carefull
# # first use the hue to get the color right
# # the saturation and value to tune it to the right brightness and darkness values
# cam.release()
###########################################################################################################
############ u can use this program to capture the object of interest completly
# as long as it matches the H,S,V parameters
while True:
    _, frame = cam.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    # after creating ur mask do an AND operation with the main frame so that u get the original color back
    # wherever the mask is applied succesfully ie; the white region in the mask
    myObject = cv2.bitwise_and(
        frame, frame, mask=myMask
    )  # yes u gotta put the first two opeators as ur main frame
    invertedObject = cv2.bitwise_not(
        frame, frame, mask=myMask
    )  # this will create an inverted mask everything except the object of interest is highlighted
    cv2.namedWindow("my mask")
    resizedMaskFrame = cv2.resize(myMask, (int(frame_width / 4), int(frame_height / 4)))
    frameResized = cv2.resize(frame, (int(frame_width / 4), int(frame_height / 4)))
    cv2.imshow("my Object of interest", invertedObject)
    cv2.moveWindow("my Object of interest", 0, 0)
    cv2.imshow("webCam", frameResized)
    cv2.moveWindow("webCam", 0, frame_height)
    cv2.moveWindow("my mask", int(frame_width / 4), frame_height)

    cv2.imshow("my mask", resizedMaskFrame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
