import cv2

# here we r just traning it to detect a face ,not recognition
facesCascade = cv2.CascadeClassifier(
    r"C:\myCodes\AI_coding\AIvenv_3.11\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
)  # u have to use this file in order to use face detection available in openCV ,just copy it from the openCV dierctory
myCam = cv2.VideoCapture(1)
while True:
    _, frame = myCam.read()
    frame = cv2.flip(frame, 1)
    grayFrame = cv2.cvtColor(
        frame, cv2.COLOR_BGR2GRAY
    )  # detection is done on a gray frame
    faces = facesCascade.detectMultiScale(
        grayFrame,
        1.3,
        5,  # just use these number they r optimal values (these are assurance parameters)
    )  # THIS FUNCTION IS USED TO DETECT MULTIPLE FACES IN ONE FRAME

    # note: the data structure for 'faces' is : [[face1_coordinates],[face2_coordinates],[face3_coordinates],.....]
    # and "face_coordinates" is : [x,y,w,h] ,(x,y) is coordinate of the boundong rectangle on the frame,(w,h) is the width and height of the rectangle
    for face in faces:  # "face" is same as 'face_coordinates' ok
        print(face)
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("turning on ur webCam", frame)
    cv2.moveWindow("turning on ur webCam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myCam.release()
# note: this is not a very strong model ok
