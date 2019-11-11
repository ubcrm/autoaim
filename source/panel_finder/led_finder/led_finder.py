from source.instance import get_json_from_file
from source.common.detect_shape import find_rectangles, reformat_cv_rectangle
from source.common.bit_mask import under_exposed_threshold
from pathlib import Path
import os


class LEDFinder:
    def __init__(self, state=None):
        if state is None:
            state = {}
        working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.properties = get_json_from_file(working_dir / "settings.json")
        self.properties.update(state)  # merges static settings and dynamically passed state. States override settings.

    def process(self, frame):
        mask = under_exposed_threshold(frame)
        rectangles = find_rectangles(mask)
        import cv2
        import numpy as np
        for rect in rectangles:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 3)

        leds = []
        for r in rectangles:
            reformat = reformat_cv_rectangle(r)
            leds.append(reformat)
        return leds
