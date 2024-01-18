import cv2
import numpy as np

frame = np.zeros([5, 5], dtype=np.uint8)
# basic black n white image matrix
print(frame)
print()
frame[3, 2] = 255  # applying 255 at index(3,2)
print(frame)
frame[1:3, 0:5] = 100
print()
# apply 100 to indexes from 1 row to 3-1 th row, and from columns 0 to 5-1
print(frame)
print()
frame[:, 0:2] = 2  # ':' means traverse through all the rows or columns
print(frame)
frame[:, :] = 0
frame[:, 3:] = 4  # its from column 3 to the last possible column
print(frame)

## now to create a BGR MATRIX ie; a color image
print("color image matrix")
frameBGR = np.zeros([5, 5, 3], dtype=np.uint8)
# the first parameter says that create a 5x5 matrix(image),and every pixel must have 3
#  values associated with it
print(frameBGR)
print("assigning color to a pixel")
# now to assign color to it
frameBGR[0, 0] = [255, 0, 255]  # Assigning the pixel at 0,0 (255,0,255)
print(frameBGR)
