import cv2
import numpy as np
import os

# current directory, video file and defaults file paths
DIR = os.path.dirname(os.path.abspath(__file__))
FILE_VIDEO = '/videos/5.mov'
FILE_DEFAULTS = '/data/default_filters.txt'

DIMS_CROP = (480, 270)  # frame crop dimensions
DELAY = 50  # ms delay between frames

# funcions to update filter limits
def set_h_min(x):
    global mins
    mins[0] = x
def set_s_min(x):
    global mins
    mins[1] = x
def set_v_min(x):
    global mins
    mins[2] = x
def set_h_max(x):
    global maxs
    maxs[0] = x
def set_s_max(x):
    global maxs
    maxs[1] = x
def set_v_max(x):
    global maxs
    maxs[2] = x

# initialize filter limits to defaults
with open(DIR + FILE_DEFAULTS, 'r') as f:
    mins = eval(f.readline())
    maxs = eval(f.readline())

# setup trackbar window GUI
cv2.namedWindow("Trackbars")
cv2.createTrackbar("h_min", "Trackbars", mins[0], 179, set_h_min)
cv2.createTrackbar("s_min", "Trackbars", mins[1], 255, set_s_min)
cv2.createTrackbar("v_min", "Trackbars", mins[2], 255, set_v_min)
cv2.createTrackbar("h_max", "Trackbars", maxs[0], 179, set_h_max)
cv2.createTrackbar("s_max", "Trackbars", maxs[1], 255, set_s_max)
cv2.createTrackbar("v_max", "Trackbars", maxs[2], 255, set_v_max)

# setup video capture and read first frame
cap = cv2.VideoCapture(DIR + FILE_VIDEO)
ret, fm = cap.read()

while ret:
    # resize frame and convert to HSV colorspace
    fm = cv2.resize(fm, DIMS_CROP)
    fm_hsv = cv2.cvtColor(fm, cv2.COLOR_BGR2HSV)

    # generate mask and apply it to frame
    mask = cv2.inRange(fm_hsv, np.array(mins), np.array(maxs))
    result = cv2.bitwise_and(fm, fm, mask=mask)

    # display mask and masked frame
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # terminate if ESC key is pressed
    if cv2.waitKey(DELAY) == 27:
        break

    # read the next frame
    ret, fm = cap.read()

# save default filter values
with open(DIR + FILE_DEFAULTS, 'w') as f:
    f.write(str(mins) + '\n' + str(maxs))

# end the capture and close all windows
cap.release()
cv2.destroyAllWindows()
