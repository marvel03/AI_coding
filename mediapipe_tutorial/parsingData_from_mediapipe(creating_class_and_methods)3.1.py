import cv2
import mediapipe as mp

cam = cv2.VideoCapture(1)
frame_width = 640
frame_height = 480
myHands = mp.solutions.hands.Hands(False, 2)
mp_draw = mp.solutions.drawing_utils


def parseLandmarks(frame):
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    both_hand_landmarks = []
    # im doing for more control ok, u can do it, how i did it before too
    results = myHands.process(frameRGB)
    if results.multi_hand_landmarks != None:
        for hand_landmarks in results.multi_hand_landmarks:
            scaled_hand_landmark = []
            for landmark in hand_landmarks.landmark:
                # print("x: ", landmark.x, "y: ", landmark.y, "z: ", landmark.z)
                scaled_hand_landmark.append(
                    (int(landmark.x * frame_width), int(landmark.y * frame_height))
                )  # note this is a array of tuples
            both_hand_landmarks.append(scaled_hand_landmark)

    return both_hand_landmarks


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    hands_landmarks = parseLandmarks(frame)
    # notice that "hands_landmarks" is in the form : [[(),(),(),(),..],[(),(),.....]]
    print(hands_landmarks)
    for single_hand in hands_landmarks:
        # to only mark the finger tips
        for tip in [8, 12, 16, 20]:  # these are finger tip no.s
            cv2.circle(frame, single_hand[tip], 10, (255, 0, 0), 2)
        cv2.circle(frame, single_hand[20], 10, (255, 0, 0), 3)
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
