import numpy as np
import cv2

from source.resource.bit_mask import find_led_from_image
from source.resource.detect_shape import find_rectangles

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
    # runs at 30 fps during testing

    # get only the areas with an LED
    thresh = find_led_from_image(frame)

    # adds boxes around LEDs, while watching they blur to look round, but each frame is a normal rectangle
    result = find_rectangles(thresh, frame)

    # Display the resulting image
    cv2.imshow('Press q to quit', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break

    # get next frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
