import cv2

frame_width = 640
frame_height = 540


def myCallBack(val):  # single parameter that has the value from the trackbar
    print(val)
    global radius
    radius = val


def someOtherCallBack(val):
    print("2nd trackbar value: ", val)


radius = 5
myCam = cv2.VideoCapture(1)
cv2.namedWindow("trackbar")
cv2.moveWindow("trackbar", frame_width, 0)
cv2.createTrackbar("radius:", "trackbar", 0, 50, myCallBack)
# parameters(name of the trackbar,name of the window to be displayed in, intial point of the trackbar(note: trackbar will always start
# 0),max limit of the trackbar,function to be called when event is captured)
# note: u can have multiple trackbars on a single window
cv2.createTrackbar("2nd bar:", "trackbar", 34, 100, someOtherCallBack)
# see it automatically queue's the new trackbar in the window

while True:
    _, frame = myCam.read()
    cv2.circle(
        frame, (int(frame_width / 2), int(frame_height / 2)), radius, (255, 0, 0), 3
    )
    cv2.imshow("webCam", frame)
    cv2.moveWindow("webCam", 0, 0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
