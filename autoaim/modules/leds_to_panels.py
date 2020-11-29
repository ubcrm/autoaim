import itertools
import numpy as np
import cv2

DRAW_NOT_PANELS = False

CRITERIA_ANGLE_DIFF = (0, 5)
CRITERIA_ASPECT_RATIO = (1.25, 2.7)
CRITERIA_RATIO_LEDS = (0.75, 1.25)

COLOR_PANEL = (0, 0, 255)
COLOR_NOT_PANEL = (0, 220, 255)
THICKNESS = 1
FONT = 0
FONT_SIZE = 0.45
LABEL_OFFSET = (-15, 4)


def leds_to_panels(leds, com):
    panels = []
    for led1, led2 in itertools.combinations(leds, 2):
        led_pair = LedPair(led1, led2)
        if led_pair.is_panel:
            panels.append(led_pair)
        if com.debug:
            led_pair.draw(com)
    if com.debug:
        print(f'Panels detected: {len(panels)}')
    return panels


class LedPair:
    def __init__(self, led1, led2):
        if led1.center[0] > led2.center[0]:
            led2, led1 = led1, led2
        self.led_left, self.led_right = led1, led2
        self.label = f'{led1.label}-{led2.label}'

        delta_x = led2.center[0] - led1.center[0]
        delta_y = np.abs(led1.center[1] - led2.center[1])
        self.width = np.sqrt(delta_x ** 2 + delta_y ** 2)
        self.height = (led1.height + led2.height) / 2
        self.center = np.array([sum(p) / 2 for p in zip(led1.center, led2.center)])
        self.distance = (led1.distance + led2.distance) / 2
        self.is_panel = self._check_panel()
        self._corners = None

    def _check_panel(self):
        angle_diff = abs(self.led_left.angle - self.led_right.angle)
        aspect_ratio = self.width / self.height
        ratio_leds = self.led_left.height / self.led_right.height
        is_panel = all([self.is_between(angle_diff, CRITERIA_ANGLE_DIFF),
                        self.is_between(aspect_ratio, CRITERIA_ASPECT_RATIO),
                        self.is_between(ratio_leds, CRITERIA_RATIO_LEDS)])
        return is_panel

    def draw(self, com):
        if not (self.is_panel or DRAW_NOT_PANELS):
            return
        corners = np.array([com.orig_to_debug(p) for p in self.get_corners()])
        color = COLOR_PANEL if self.is_panel else COLOR_NOT_PANEL
        label_position = tuple([sum(p) for p in zip(com.orig_to_debug(self.center), LABEL_OFFSET)])
        cv2.polylines(com.debug_frame, [corners], True, color, THICKNESS)
        cv2.putText(com.debug_frame, self.label, label_position, FONT, FONT_SIZE, color)

    def get_corners(self):
        if self._corners is None:
            tl, _, _, bl = self.led_left.get_corners()
            _, tr, br, _ = self.led_right.get_corners()
            self._corners = np.array([tl, tr, br, bl])
        return self._corners

    @staticmethod
    def is_between(value, range_):
        return range_[0] <= value <= range_[1]
