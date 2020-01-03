from source.module import Module
from pathlib import Path
import os
from itertools import combinations
from math import sqrt, degrees, atan


class LedMatcher(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        if self.config['mode'] == 'coded':
            from .coded_matcher.coded_matcher import CodedMatcher
            self.led_matcher = CodedMatcher(self)
        elif self.config['mode'] == 'opencv':
            from .opencv_matcher.opencv_matcher import OpencvMatcher
            self.led_matcher = OpencvMatcher(self)
        elif self.config['mode'] == 'tensorflow':
            from .tensorflow_matcher.tensorflow_matcher import TensorflowMatcher
            self.led_matcher = TensorflowMatcher(self)

    def process(self, leds):
        panels = []
        not_panels = []
        # we can sort by angle and/or x of center first and pair neighbors
        for led1, led2 in combinations(leds, 2):
            led_pair = LedPair(led1, led2)
            self.led_matcher.process(led_pair)

            if led_pair.is_panel:
                panels.append(led_pair)
            else:
                not_panels.append(led_pair)
        return panels, not_panels


class LedPair:
    def __init__(self, led1, led2):
        """
        Represent an led pair (possibly a panel)
        :param led1, led2: pair of BoundingRect objects that are leds
        """
        self.led_left = led1 if led1.center[0] < led2.center[0] else led2
        self.led_right = led2 if led1.center[0] < led2.center[0] else led1
        self.label = self.led_left.label + '-' + self.led_right.label

        delta_x = self.led_right.center[0] - self.led_left.center[0]
        delta_y = self.led_right.center[1] - self.led_left.center[1]
        top_left, _, _, bottom_left = self.led_left.corners
        _, top_right, bottom_right, _ = self.led_right.corners

        self.width = round(sqrt(delta_x ** 2 + delta_y ** 2) + (led1.width + led2.width) / 2)
        self.height = round((led1.height + led2.height) / 2)
        self.angle = round((led1.angle + led2.angle) / 2)
        self.angle_mid = round(degrees(atan(delta_y / max(1e-3, delta_x))))

        self.center = (round((led1.center[0] + led2.center[0]) / 2), round((led1.center[1] + led2.center[1]) / 2))
        self.corners = [top_left, top_right, bottom_right, bottom_left]
        self.distance = (led1.distance + led2.distance) / 2

        self.confidences = None
        self.is_panel = None

    def log(self):
        attributes = [
            'width=%d' % self.width,
            'height=%d' % self.height,
            'angle=%d' % self.angle,
            'center=%s' % str(self.center),
            'distance=%.2f' % self.distance,
            'is_panel=%s' % str(self.is_panel)
        ]
        confidences = [(criterion + '=%.2f' % value) for criterion, value in self.confidences.items()]
        print('Panel %s: %s | %s' % (self.label, ' '.join(attributes), ' '.join(confidences)))
