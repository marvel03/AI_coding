import cv2
import numpy as np

height = 250
width = 250
# black and white image
# while True:
#     frame = np.zeros([250, 250], dtype=np.uint8)
#     ##### applying splicing
#     frame[10:100, :] = 255
#     #####
#     cv2.imshow("custom image", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
################################################

# color image
# while True:
#     frame = np.zeros([height, width, 3], dtype=np.uint8)
#     ##### applying splicing
#     frame[10:100, :] = (255, 0, 0)
#     frame[150:200, :] = (255, 0, 255)
#     #####
#     cv2.imshow("custom image", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#############################################
### homework problem_ create a checker board pattern
n = 10  # im making an nxn checker board
while True:
    frame = np.zeros([height, width], dtype=np.uint8)
    lw = int(width / n)
    lh = int(height / n)
    for i in range(0, n):
        for j in range(0, n):
            if j % 2 == 0:
                if i % 2 == 0:
                    frame[j * lh : (j + 1) * lh, i * lw : (i + 1) * lw] = 255
            else:
                if i % 2 != 0:
                    frame[j * lh : (j + 1) * lh, i * lw : (i + 1) * lw] = 255
    cv2.imshow("checker board", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
