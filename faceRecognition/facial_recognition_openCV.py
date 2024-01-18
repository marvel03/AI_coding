import cv2
import face_recognition as FR

### its incomplete ,coz the library didnt install properly

font = cv2.FONT_HERSHEY_COMPLEX
peta = FR.load_image_file(r"C:\myCodes\AI_coding\faceRecognition\known\peta jensen.jpg")
######## traing ur model using one picture
faceLoc_peta = FR.face_locations(peta)
# 'faceLoc': [[],[],[],.....],its an array of array
# no. of subarrays will depend on the no. of faces
faceLoc_peta = faceLoc_peta[0]
# we r taking the first sub array, or the first face info
##next encode ur image
encodedImage_peta = FR.face_encodings(peta)
## even this is an array of array ,coz its possible to get more than one face
##so we must extract the first sub array from this(coz we have only face)
encodedImage_peta = encodedImage_peta[0]
top, right, bottom, left = faceLoc_peta
# MARKING THE FACE OF THE PERSON IN THE IMAGE
# cv2.rectangle(peta, (left, top), (right, bottom), (255, 0, 0), 3)
knownEncodings = [encodedImage_peta]
names = ["peta jensen"]
######## end of training one image

## now testing the image using another image
unknownFace = FR.load(r"C:\myCodes\AI_coding\faceRecognition\unknown\unknown1.jpeg")
unknownFaceBGR = cv2.cvtColor(unknownFace, cv2.COLOR_RGB2BGR)
faceLocations = FR.face_locations(unknownFace)
unknownEncodings = FR.face_encodings(unknownFace, faceLocations)

for faceLocation, unknownEncoding in faceLocations, unknownEncodings:
    top, right, bottom, left = faceLocation
    print(faceLocation)
    cv2.rectangle()

petaBGR = cv2.cvtColor(peta, cv2.COLOR_RGB2BGR)
cv2.imshow("my window", petaBGR)
cv2.waitKey(5000)  # program waits for 5 seconds
