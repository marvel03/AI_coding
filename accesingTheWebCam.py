import cv2


myCam = cv2.VideoCapture(1)
# myCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)# incase of error
while True:
    _, frame = myCam.read()  # a single frame is read
    ###### do ur analysis part in here , things u gotta analyze in a frame

    # for now im gonna change a default BGR frame to grayscale
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ######
    cv2.imshow("turning on ur webCam", grayFrame)
    # display the frame u just read(note:the stuff written in quotes is ur window name)
    cv2.moveWindow("turning on ur webCam", 0, 0)
    # the window name should be the same(the stuff in the quotes)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        # 0xFF is just adding a mask so that this line executes with no trouble
        break
myCam.release()
