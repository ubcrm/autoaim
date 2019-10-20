import numpy as np
import cv2
from source.resource import bit_mask, detect_shape
from source.tensorflow_pipeline import tensorflow_pipeline
import time


def draw_rectangles(frame, rectangles):
    for rect in rectangles:
        draw_rectangle(frame, rect)


def draw_rectangle(frame, rect, color=(255, 0, 0)):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box], 0, color, 3)


def main():
    vidA = "robot2.mp4"  # change to path of downloaded video

    # load video
    cap = cv2.VideoCapture(vidA)

    # Capture frame-by-frame
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    avg_time = []
    # loop through frames in video
    while ret:

        # frame = cv2.pyrDown(frame) # enable this line to see lower resolution

        # get only the areas with an LED
        start = time.time()
        thresh = bit_mask.under_exposed_threshold(frame)
        # frame = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        rects = detect_shape.find_rectangles(thresh)

        avg_time.append(time.time() - start)

        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        draw_rectangles(frame, rects)

        # Display the resulting image
        cv2.imshow('Press q to quit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break

        # get next frame
        ret, frame = cap.read()
    else:
        print("last frame reached")

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print(1 / (sum(avg_time) / len(avg_time)), "fps")


if __name__ == "__main__":
    main()
