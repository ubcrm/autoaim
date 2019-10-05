import numpy as np
import cv2


def findRectangles(filtered, frame):
    # puts rectangles on blobs
    contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        if min(rect[1]) > 10:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 3)
    return frame


def findLEDFromImage(frame):
    # layer 1: Only high hue pixels using hsv color format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    layer1 = cv2.inRange(hsv, (179 * 0, 0, 250), (179 * 0.5, 60, 255))
    kernel = np.ones((2, 2), np.uint8)
    layer1 = cv2.dilate(layer1, kernel, iterations=7)

    # layer 2: Everything near bright red
    layer2 = cv2.inRange(frame, (0, 0, 250), (150, 150, 255))
    kernel = np.ones((4, 4), np.uint8)
    layer2 = cv2.dilate(layer2, kernel, iterations=10)

    # layer 3: only bright pixels
    layer3 = cv2.inRange(frame, (200, 200, 253), (255, 255, 255))
    kernel = np.ones((3, 3), np.uint8)
    layer3 = cv2.dilate(layer3, kernel, iterations=2)

    # final image: only the overlap of all 3 layers
    result = cv2.bitwise_and(layer1, layer2)
    result = cv2.bitwise_and(result, layer3)
    return result

    # runs at 30 fps during testing


# some reference videos
vidA = "videos/robot1.MOV"
vidB = "videos/robot2.mp4"
vidC = "videos/robot3.MOV"  # no robot, just ceiling lights
vidD = "videos/robot4.MOV"
vidE = "videos/robot5.mp4"

# load video
cap = cv2.VideoCapture(vidA)

# Capture frame-by-frame
ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red

# loop through frames in video
while ret:
    # get only the areas with an LED
    thresh = findLEDFromImage(frame)

    # adds boxes around LEDs, while watching they blur to look round, but each frame is a normal rectangle
    result = findRectangles(thresh, frame)

    # Display the resulting image
    cv2.imshow('Press q to quit', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break

    # get next frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
