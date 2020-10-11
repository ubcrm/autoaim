from leds_to_panels_config import *
import itertools
import numpy as np
import cv2


def leds_to_panels(leds, debug=None):
    panels = []

    for led1, led2 in itertools.combinations(leds, 2):
        led_pair = LedPair(led1, led2)
        if led_pair.is_panel:
            panels.append(led_pair)
        if debug is not None:
            led_pair.draw(debug.frame.image)
    return panels


class LedPair:
    def __init__(self, led1, led2):
        switch_leds = led1.center[0] < led2.center[0]
        self.led_left = led1 if switch_leds else led2
        self.led_right = led2 if switch_leds else led1
        self.label = LABEL_FORMAT.format(self.led_left.label, self.led_right.label)

        delta_x = self.led_right.center[0] - self.led_left.center[0]
        delta_y = self.led_right.center[1] - self.led_left.center[1]
        self.width = np.sqrt(delta_x ** 2 + delta_y ** 2) + (led1.width + led2.width) / 2
        self.height = (led1.height + led2.height) / 2
        self.center = tuple([round(sum(p) / 2) for p in zip(led1.center, led2.center)])
        self.distance = (led1.distance + led2.distance) / 2
        self.is_panel = self._check_panel()
        self._corners = None

    def _check_panel(self):
        angle_diff = abs(self.led_left.angle - self.led_right.angle)
        aspect_ratio = self.width / max(EPSILON, self.height)
        ratio_leds = self.led_left.height / self.led_right.height
        is_panel = all([self.is_between(angle_diff, CRITERIA.ANGLE_DIFF),
                        self.is_between(aspect_ratio, CRITERIA.ASPECT_RATIO),
                        self.is_between(ratio_leds, CRITERIA.RATIO_LEDS)])
        return is_panel

    def draw(self, frame):
        should_draw = self.is_panel or DRAW_NOT_PANELS
        if not should_draw:
            return

        color = DRAW.COLOR_PANEL if self.is_panel else DRAW.COLOR_NOT_PANEL
        label_position = tuple([sum(p) for p in zip(self.center, DRAW.LABEL_OFFSET)])
        cv2.polylines(frame, [self.get_corners()], True, color, DRAW.THICKNESS)
        cv2.putText(frame, self.label, label_position, DRAW.FONT, DRAW.FONT_SIZE, color)

    def get_corners(self):
        if self._corners is None:
            topleft, _, _, bottomleft = self.led_left.get_corners()
            _, topright, bottomright, _ = self.led_right.get_corners()
            self._corners = np.array([topleft, topright, bottomright, bottomleft])
        return self._corners

    @staticmethod
    def is_between(value, range_):
        return range_[0] <= value <= range_[1]
