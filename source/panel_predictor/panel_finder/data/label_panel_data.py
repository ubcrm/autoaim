import cv2
import json
import os
import time
import numpy as np
from source.panel_predictor.panel_finder.data.leds import Led, LedCombs
from source.common import bit_mask, shape_finder

leds = []
pairs = []
past_pairs = []
frame = None


def draw_rectangle(rectangle, color=(0, 255, 0)):
    global frame
    box = cv2.boxPoints(rectangle)
    box = np.int0(box)
    cv2.drawContours(frame, [box], 0, color, 3)


def draw_rectangles(rectangles, color=(255, 0, 0)):
    for rectangle in rectangles:
        draw_rectangle(rectangle, color)


def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        global leds, pairs, frame, past_pairs
        for led in leds:
            box = cv2.boxPoints(led)
            box = np.int0(box)
            if cv2.pointPolygonTest(box, (x, y), False) > 0:
                if led in pairs:
                    pairs.remove(led)
                    draw_rectangle(led, (255, 0, 0))
                else:
                    pairs.append(led)
                    past_pairs.append(led)
                    draw_rectangle(led, (0, 255 if len(pairs) < 3 else 0, 255 if 3 <= len(pairs) < 5 else 0))


def distance_squared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def guess_past(past, rectangles):
    global past_pairs, pairs
    best_guesses = []
    for led in past_pairs:
        for rect in rectangles:
            if distance_squared(led[0], rect[0]) < 1000:
                best_guesses.append(rect)
    if len(best_guesses) % 2 == 0:
        pairs += best_guesses
        past_pairs = best_guesses
        for led in best_guesses:
            draw_rectangle(led, (0, 255 if len(best_guesses) < 3 else 0, 255 if 3 <= len(best_guesses) < 5 else 0))


def main():
    global leds, frame, pairs

    pair_data = {}
    pair_cnt = 0
    image_index = 0

    DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_OUT = '/pair_training_data_old.json'

    vid = "videos/robot3.mp4"  # relative path of downloaded video

    # load video
    cap = cv2.VideoCapture(vid)
    cv2.namedWindow("Press q to quit")
    cv2.setMouseCallback("Press q to quit", click)
    ending = False

    # Capture frame-by-frame
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red

    # loop through frames in video
    while ret and not ending:
        start = time.time()

        mask = bit_mask.under_exposed_threshold(frame)
        leds = shape_finder.find_rectangles(mask)
        draw_rectangles(leds)
        guess_past(past_pairs, leds)

        # Display the resulting image
        while True:
            # display the image and wait for a keypress
            cv2.imshow("Press q to quit", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(" ") and len(pairs) % 2 == 0:
                break
            elif key == ord("q") and len(pairs) % 2 == 0:
                ending = True
                break

        leds_obj = []
        pair_indexes = []
        for rect_index, rect in enumerate(leds):
            leds_obj.append(Led(rect_index, *rect))
            if rect in past_pairs:
                pair_indexes.append(rect_index)
        pair_indexes = [(i, j) for i, j in zip(pair_indexes[::2], pair_indexes[1::2])]

        combs = LedCombs(image_index, leds_obj, [tuple(pair_indexes)])
        for pair_info in combs.to_dict().values():
            pair_data[str(pair_cnt)] = pair_info
            pair_cnt += 1
            print(pair_info["isPanel"])
        pairs = []
        image_index += 1

        # get next frame
        ret, frame = cap.read()
    else:
        print("Last frame reached")

    with open(DIR + DATA_OUT, 'w') as f:
        json.dump(pair_data, f, indent=4)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
