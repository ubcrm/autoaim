from assets.module import Module
from pathlib import Path
import os
from itertools import combinations
from .assets.led_pair import LedPair


class LedMatch(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        if self.config['mode'] == 'coded':
            from .coded_match.coded_match import CodedMatch
            self.matcher = CodedMatch(self)
        elif self.config['mode'] == 'opencv':
            from .opencv_match.opencv_match import OpencvMatch
            self.matcher = OpencvMatch(self)
        elif self.config['mode'] == 'tf':
            from .tf_match.tf_match import TfMatch
            self.matcher = TfMatch(self)

    def process(self, leds):
        panels = []
        not_panels = []
        # we can sort by angle and/or x of center first and pair neighbors
        for led1, led2 in combinations(leds, 2):
            led_pair = LedPair(led1, led2)
            self.matcher.process(led_pair)

            if led_pair.is_panel:
                panels.append(led_pair)
            else:
                not_panels.append(led_pair)
        return panels, not_panels
