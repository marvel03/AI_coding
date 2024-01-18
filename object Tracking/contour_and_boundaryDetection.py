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

cv2.namedWindow("my Trackbars")
cv2.moveWindow("my Trackbars", frame_width, 0)
cv2.createTrackbar("Hue low", "my Trackbars", 137, 179, onTrack1)
cv2.createTrackbar("Hue high", "my Trackbars", 179, 179, onTrack2)
cv2.createTrackbar("Sat low", "my Trackbars", 57, 255, onTrack3)
cv2.createTrackbar("Sat high", "my Trackbars", 250, 255, onTrack4)
cv2.createTrackbar("val low", "my Trackbars", 43, 255, onTrack5)
cv2.createTrackbar("val high", "my Trackbars", 219, 255, onTrack6)

while True:
    _, frame = cam.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ################creating the mask
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    resizedMaskFrame = cv2.resize(myMask, (int(frame_width / 4), int(frame_height / 4)))
    cv2.namedWindow("my mask")
    cv2.moveWindow("my mask", int(frame_width / 4), frame_height)
    cv2.imshow("my mask", resizedMaskFrame)
    #######detecting the countours
    ### note: u gotta detect it on the mask not the masked image
    contours, ignore = cv2.findContours(
        myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    # parameters used above are->
    #    myMask: the mask u want to get ur contours from
    #    cv2.RETR_EXTERNAL: tells this function to return only the outermost boundary pixels of the object of interest
    #    cv2.CHAIN_APPROX_SIMPLE: tells the funtion to only return a limited set of pixel points rather than all the pixel points
    ##now draw the contours onto ur frame

    # cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)

    ## -1 -> draw all the contour sets from the countour array
    ## if u want a specific contour set to be drawn from the contour array, use 0,1,..or n,indicaticating the index of the contour set from the counter array

    ####noise correction for contours(u can manually adjust the mask parameters too if needed, but not possible real world applications )
    ## using the cv2.contourArea() function we will calculate the area associated with
    ## each contour set ,ie area bounded by those points in each contour set
    ## and then define a threshold ,so if the area is greater than a particular value, draw only that contour points

    for contour in contours:  # notice the shape of "counter" and "contours"
        # contour : [x,y],[x,y],[x,y],....
        # contours: [[contour],[contour],[contour],.....]
        area = cv2.contourArea(contour)
        if area >= 500:
            # cv2.drawContours(frame, [contour], 0, (255, 0, 0), 3)
            ## i did the [contour] coz this function expects an array of an array as its parameter
            ## u can use this same logic to draw a rectangle around the object ,rather than plot the entire boundary
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    ##object of interest
    myObject = cv2.bitwise_and(frame, frame, mask=myMask)
    resizedMyObject = cv2.resize(
        myObject, (int(frame_width / 4), int(frame_height / 4))
    )
    cv2.imshow("my Object of interest", resizedMyObject)
    cv2.moveWindow("my Object of interest", 0, frame_height)
    ###############

    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", 0, 0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
