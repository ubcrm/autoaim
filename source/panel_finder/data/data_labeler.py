import cv2, os
import numpy as np
from pathlib import Path

from source.common.instance import get_json_from_file
from source.common.bit_mask import over_exposed_threshold, under_exposed_threshold
from source.common.detect_shape import find_rectangles, find_contours, find_quad_centers
from source.panel_finder.data.leds import Led, LedCombs


class DataLabeler:
    def __init__(self, settings, state=None):
        if state is None:
            state = {}
        self.properties = settings
        self.properties.update(state)

    def show_feed(self, labels, rects, image):
        for label in labels.values():
            x1, y1 = label.get('x1'), label.get('y1')
            x2, y2 = label.get('x2'), label.get('y2')
            label_points = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
            cv2.drawContours(image, [label_points], 0, (0, 255, 0), 2)

        for rect_index, rect in enumerate(rects):
            color = (0, 0, 255)
            if any((pair[0] == str(rect_index) or pair[1] == str(rect_index)) for pair in self.panel_pairs):
                color = (255, 0, 0)
            box = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(image, [box], 0, color, 2)

        cv2.imshow('Feed', image)
        cv2.waitKey(self.properties["delay"])

    def find_panel_pairs(self, leds, labels):
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

    def process(self, json):
        labels = get_json_from_file(self.properties["labels_in"])
        pair_data = {}
        pair_cnt = 0
        c = self.properties["image_count"]
        should_log = self.properties["logging"]

        for image_index in range(0, c):
            if should_log:
                print('Processing %d of %d' % (image_index + 1, c))

            image = cv2.imread(Path(self.properties["image_in"]) % image_index)
            mask = over_exposed_threshold(image)
            rects = find_rectangles(mask)
            labels = labels['%d.jpg' % image_index]

            leds = [Led(rect_index, *rect) for rect_index, rect in enumerate(rects)]
            panel_pairs = self.find_panel_pairs(leds, labels)

            if self.properties["show_feed"]:
                self.show_feed(labels, rects, image)

            combs = LedCombs(image_index, leds, panel_pairs)
            for pair_info in combs.to_dict().values():
                pair_data[str(pair_cnt)] = pair_info
                pair_cnt += 1

        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + self.properties["data_out"], 'w') as f:
            json.dump(pair_data, f, indent=4)

        if self.properties["logging"]:
            print('Pair training data saved.')
