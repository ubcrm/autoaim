import os
from pathlib import Path

from source.common.bit_mask import under_exposed_threshold
from source.common.detect_shape import find_rectangles, reformat_cv_rectangle
from source.common.module import Module


class LEDFinder(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)

    def process(self, frame):
        mask = under_exposed_threshold(frame)
        rectangles = find_rectangles(mask)

        leds = []
        for r in rectangles:
            reformat = reformat_cv_rectangle(r)
            leds.append(reformat)
        return leds
