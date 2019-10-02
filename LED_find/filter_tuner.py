import cv2
import numpy as np
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def set_h_min(x):
    global h_min
    h_min = x
def set_s_min(x):
    global s_min
    s_min = x
def set_v_min(x):
    global v_min
    v_min = x
def set_h_max(x):
    global h_max
    h_max = x
def set_s_max(x):
    global s_max
    s_max = x
def set_v_max(x):
    global v_max
    v_max = x

h_min, s_min, v_min = (0, 0, 0)
h_max, s_max, v_max = (179, 255, 255)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("h_min", "Trackbars", h_min, 179, set_h_min)
cv2.createTrackbar("s_min", "Trackbars", s_min, 255, set_s_min)
cv2.createTrackbar("v_min", "Trackbars", v_min, 255, set_v_min)
cv2.createTrackbar("h_max", "Trackbars", h_max, 179, set_h_max)
cv2.createTrackbar("s_max", "Trackbars", s_max, 255, set_s_max)
cv2.createTrackbar("v_max", "Trackbars", v_max, 255, set_v_max)

cap = cv2.VideoCapture(DIR + '/videos/2.mov')
ret, fm = cap.read()

while ret:
    fm = cv2.resize(fm, (480, 270))
    fm_hsv = cv2.cvtColor(fm, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([h_min, s_min, v_min])
    hsv_max = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(fm_hsv, hsv_min, hsv_max)
    result = cv2.bitwise_and(fm, fm, mask=mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(25) == 27:
        break

    ret, fm = cap.read()

cap.release()
cv2.destroyAllWindows()
