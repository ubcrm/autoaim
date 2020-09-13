import leds_to_panels_config as CONFIG
import itertools
import numpy as np
import cv2


def leds_to_panels(leds, debug_frame=None):
    panels = []

    for led1, led2 in itertools.combinations(leds, 2):
        led_pair = LedPair(led1, led2)
        if led_pair.is_panel:
            panels.append(led_pair)
        if debug_frame is not None:
            led_pair.draw(debug_frame)
    return panels


class LedPair:
    def __init__(self, led1, led2):
        switch_leds = led1.center[0] < led2.center[0]
        self.led_left = led1 if switch_leds else led2
        self.led_right = led2 if switch_leds else led1
        self.label = CONFIG.LABEL_FORMAT.format(self.led_left.label, self.led_right.label)

        delta_x = self.led_right.center[0] - self.led_left.center[0]
        delta_y = self.led_right.center[1] - self.led_left.center[1]
        self.width = np.sqrt(delta_x ** 2 + delta_y ** 2) + (led1.width + led2.width) / 2
        self.height = (led1.height + led2.height) / 2
        self.center = tuple([round(sum(p) / 2) for p in zip(led1.center, led2.center)])
        self.distance = (led1.distance + led2.distance) / 2
        self.is_panel = self._check_panel()

    def _check_panel(self):
        angle_diff = abs(self.led_left.angle - self.led_right.angle)
        aspect_ratio = self.width / max(CONFIG.EPSILON, self.height)
        ratio_leds = self.led_left.height / self.led_right.height
        is_panel = all([self.is_between(angle_diff, CONFIG.CRITERIA.ANGLE_DIFF),
                        self.is_between(aspect_ratio, CONFIG.CRITERIA.ASPECT_RATIO),
                        self.is_between(ratio_leds, CONFIG.CRITERIA.RATIO_LEDS)])
        return is_panel

    def draw(self, frame):
        corners = self.find_corners()
        color = CONFIG.DRAW.COLOR_PANEL if self.is_panel else CONFIG.DRAW.COLOR_NOT_PANEL
        label_position = tuple([sum(p) for p in zip(self.center, CONFIG.DRAW.LABEL_OFFSET)])

        cv2.polylines(frame, [corners], True, color, CONFIG.DRAW.THICKNESS)
        cv2.putText(frame, self.label, label_position, CONFIG.DRAW.FONT, CONFIG.DRAW.FONT_SIZE, color)

    def find_corners(self):
        topleft, _, _, bottomleft = self.led_left.corners
        _, topright, bottomright, _ = self.led_right.corners
        return np.array([topleft, topright, bottomright, bottomleft])

    @staticmethod
    def is_between(value, range_):
        return range_[0] <= value <= range_[1]
