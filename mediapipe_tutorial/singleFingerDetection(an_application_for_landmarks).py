import cv2
import mediapipe as mp

frame_width = 640
frame_height = 480

cam = cv2.VideoCapture(1)
mp_draw = mp.solutions.drawing_utils
myHands = mp.solutions.hands.Hands(False, 2)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = myHands.process(frame)
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            # print(handLandmarks)  # this is a set of tuples called "landmarks"
            # accesing each landmark,s x,y coordinates(even z if u want)
            scaledLandmarkValues = []
            for landmark in handLandmarks.landmark:
                # print("x: ", landmark.x, "y: ", landmark.y, "z: ", landmark.z)
                # these values are normalized
                # on scaling them we get
                # print("x: ", landmark.x * frame_width, "y: ", frame_height * landmark.y)
                scaledLandmarkValues.append(
                    (int(landmark.x * frame_width), int(frame_height * landmark.y))
                )
            print(scaledLandmarkValues)
            # now as u can see i have converted the hand landmark coordinates((x,y) only) into an array of tuple
            # each tuple representing a landmark
            # now u can plot any one point for single finger detection,
            # say u want only pinky finger (joint no. 20)
            cv2.circle(frame, scaledLandmarkValues[20], 5, (255, 0, 0), -1)

    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", 0, 0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
