import cv2

# this code may not work properly, coz my webCam is broken , so its for future applications
width = 640
height = 360
# use standard resolutions only, to avoid error
myCam = cv2.VideoCapture(1)
# myCam = cv2.VideoCapture(1, cv2.CAP_DSHOW)# this line doesnt work for me, but its there of the future
# telling windows explicitly, that its for displaying purpose
myCam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
myCam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
myCam.set(cv2.CAP_PROP_FPS, 30)
# u can also set the video encoding manually to improve speed, but google how to do that

while True:
    _, frame = myCam.read()
    # Create a named window if it doesn't exist
    if not cv2.getWindowProperty("turning on ur webCam", cv2.WND_PROP_VISIBLE):
        cv2.namedWindow("turning on ur webCam", cv2.WINDOW_NORMAL)
    cv2.imshow("turning on ur webCam", frame)
    cv2.moveWindow("turning on ur webCam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
