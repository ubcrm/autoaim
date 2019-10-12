from manage_leds import Led, LedCombs
import cv2, os, json, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, DIR + '/../../source/resource')
from bit_mask import find_led_from_image
from detect_shape import find_rectangles

DATA_OUT = '/data/pair_data.json'
LABELS_IN = '/data/image_labels.json'
IMAGE_IN = '/data/images/%d.jpg'

IMAGE_CNT = 655
DELAY_MS = 0
SHOW_FEED = False
PRINT_TO_TERMINAL = True


def show_feed(labels, rects, image):
    for label in labels.values():
        x1, y1 = label.get('x1'), label.get('y1')
        x2, y2 = label.get('x2'), label.get('y2')
        label_points = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        cv2.drawContours(image, [label_points], 0, (0, 255, 0), 2)

    for rect_index, rect in enumerate(rects):
        color = (0, 0, 255)
        if any((pair[0] == str(rect_index) or pair[1] == str(rect_index)) for pair in panel_pairs):
            color = (255, 0, 0)
        box = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(image, [box], 0, color, 2)

    cv2.imshow('Feed', image)
    cv2.waitKey(DELAY_MS)


def find_panel_pairs(leds, labels):
    panel_pairs = []

    for label in labels.values():
        leds_inside = []
        for led in leds:
            x, y = led.center
            x1, y1 = label.get('x1'), label.get('y1')
            x2, y2 = label.get('x2'), label.get('y2')
            if (x1 < x < x2) and (y1 < y < y2):
                leds_inside += [led]

        if len(leds_inside) == 2:
            panel_pairs += [(leds_inside[0].id, leds_inside[1].id)]

    return panel_pairs


with open(DIR + LABELS_IN, 'r') as f:
    labels_dict = json.load(f)

pair_data = {}
pair_cnt = 0

for image_index in range(0, IMAGE_CNT):
    if PRINT_TO_TERMINAL:
        print('Processing %d.jpg/%d.jpg' % (image_index, IMAGE_CNT - 1))

    image = cv2.imread(DIR + IMAGE_IN % image_index)
    rects = find_rectangles(find_led_from_image(image))
    labels = labels_dict['%d.jpg' % image_index]

    leds = [Led(rect_index, *rect) for rect_index, rect in enumerate(rects)]
    panel_pairs = find_panel_pairs(leds, labels)

    if SHOW_FEED:
        show_feed(labels, rects, image)

    combs = LedCombs(image_index, leds, panel_pairs)
    for pair_info in combs.toDict().values():
        pair_data[str(pair_cnt)] = pair_info
        pair_cnt += 1


with open(DIR + DATA_OUT, 'w') as f:
    json.dump(pair_data, f, indent=4)

if PRINT_TO_TERMINAL:
    print('Pair data generated and saved successfully.')
