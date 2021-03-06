import cv2 as cv
import numpy as np
from time import sleep

video = cv.VideoCapture('./record/videos/glitch1.h264')

purple_glitch_bottom = np.array([149, 216, 56])
purple_glitch_top = np.array([166, 255, 221])

x, y = 0, 0

while True:
    ret, frame = video.read()

    if not ret:
        break

    key = cv.waitKey(1)
    if key & 0xff == ord('q'):
        break

    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    glitch_mask = cv.inRange(
        hsv_frame, purple_glitch_bottom, purple_glitch_top)

    size = 0
    for row in glitch_mask:
        for point in row:
            if point:
                size += 1

    if size:
        print('y')
        x += 1
    else:
        print('n')
        y += 1

    result = cv.bitwise_and(frame, frame, mask=glitch_mask)

    # cv.imshow('frame', frame)
    # cv.imshow('result', result)
    # sleep(0.02)

video.release()
cv.destroyAllWindows()

print(x, y)
