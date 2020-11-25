import cv2
import numpy as np

HEIGHT_1M_REL = 0.12

CRITERIA_DISTANCE = (0.3, 4)
CRITERIA_DIMS_RATIO = (2, 15)
CRITERIA_ANGLE = (-30, 30)  # change to (-15, 15) on proper footage

COLOR_LED = (255, 180, 0)
COLOR_NOT_LED = (0, 180, 255)
THICKNESS = 1
FONT = 0
FONT_SIZE = 0.46
LABEL_OFFSET = (7, 4)


def mask_to_leds(mask, com):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    leds = []

    for i, contour in enumerate(contours):
        bounding_rect = BoundingRect(cv2.minAreaRect(contour), i + 1, com)
        if bounding_rect.is_led:
            leds.append(bounding_rect)
        if com.debug:
            bounding_rect.draw(com)
    if com.debug:
        print(f'Leds detected: {len(leds)}')
    return leds


class BoundingRect:
    def __init__(self, rect, label, com):
        self.label = str(label)
        self.center = com.frame_to_orig(rect[0])
        self.width = min(rect[1]) * com.frame_scale
        self.height = max(rect[1]) * com.frame_scale
        self.angle = rect[2]
        if rect[1][1] < rect[1][0]:  # after the following adjustments, -90 <= angle < 90
            self.angle += 90
            if self.angle >= 90:
                self.angle -= 180
        self.distance = HEIGHT_1M_REL / (self.height / com.orig_dims[1])
        self.is_led = self._check_led()
        self._corners = None

    def _check_led(self):
        dims_ratio = self.height / max(1E-3, self.width)
        is_led = all([self.is_between(self.distance, CRITERIA_DISTANCE),
                      self.is_between(self.angle, CRITERIA_ANGLE),
                      self.is_between(dims_ratio, CRITERIA_DIMS_RATIO)])
        return is_led

    def draw(self, com):
        corners = np.array([com.orig_to_debug(p) for p in self.get_corners()])
        color = COLOR_LED if self.is_led else COLOR_NOT_LED
        label_position = tuple([sum(p) for p in zip(com.orig_to_debug(self.center), LABEL_OFFSET)])
        cv2.polylines(com.debug_frame, [corners], True, color, THICKNESS)
        cv2.putText(com.debug_frame, self.label, label_position, FONT, FONT_SIZE, color)

    def get_corners(self):
        if self._corners is None:
            (x, y), hw, hh, a = self.center, self.width / 2, self.height / 2, self.angle
            sina, cosa = np.sin(np.deg2rad(a)), np.cos(np.deg2rad(a))
            tl = (x - hw * cosa + hh * sina, y - hh * cosa - hw * sina)
            tr = (x + hw * cosa + hh * sina, y - hh * cosa + hw * sina)
            br = (x + hw * cosa - hh * sina, y + hh * cosa + hw * sina)
            bl = (x - hw * cosa - hh * sina, y + hh * cosa - hw * sina)
            self._corners = np.array([tl, tr, br, bl])
        return self._corners

    @staticmethod
    def is_between(value, range_):
        return range_[0] <= value <= range_[1]
