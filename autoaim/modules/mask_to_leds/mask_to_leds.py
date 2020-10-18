from autoaim_config import DO_DEBUG
from mask_to_leds_config import *
import cv2
import numpy as np


def mask_to_leds(capture):
    contours, _ = cv2.findContours(capture.frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    leds = []

    for i, contour in enumerate(contours):
        bounding_rect = BoundingRect(cv2.minAreaRect(contour), i + 1, capture)
        if bounding_rect.is_led:
            leds.append(bounding_rect)
        if DO_DEBUG:
            bounding_rect.draw(capture)
    return leds


class BoundingRect:
    def __init__(self, rect, label, capture):
        self.label = str(label)
        self.center = (round(rect[0][0]), round(rect[0][1]))
        self.width = round(min(rect[1]))
        self.height = round(max(rect[1]))
        self.angle = round(rect[2])
        if rect[1][1] < rect[1][0]:  # after the following adjustments -90 <= angle < 90
            self.angle += 90
            if self.angle >= 90:
                self.angle -= 180
        self.distance = 1 / max(EPSILON, self.height * capture.scale_factor / HEIGHT_1M_REL + DISTANCE_OFFSET)
        self.is_led = self._check_led()
        self._corners = None

    def _check_led(self):
        dims_ratio = self.height / max(EPSILON, self.width)
        is_led = all([self.is_between(self.distance, CRITERIA.DISTANCE),
                      self.is_between(self.angle, CRITERIA.ANGLE),
                      self.is_between(dims_ratio, CRITERIA.DIMS_RATIO)])
        return is_led

    def draw(self, capture):
        corners = np.array([capture.point_to_debug(p) for p in self.get_corners()])
        color = DRAW.COLOR_LED if self.is_led else DRAW.COLOR_NOT_LED
        label_position = tuple([sum(p) for p in zip(capture.point_to_debug(self.center), DRAW.LABEL_OFFSET)])

        cv2.polylines(capture.debug_frame, [corners], True, color, DRAW.THICKNESS)
        cv2.putText(capture.debug_frame, self.label, label_position, DRAW.FONT, DRAW.FONT_SIZE, color)

    def get_corners(self):
        if self._corners is None:
            (x, y), hw, hh, a = self.center, self.width / 2, self.height / 2, self.angle
            sina, cosa = np.sin(np.deg2rad(a)), np.cos(np.deg2rad(a))
            top_left = (round(x - hw * cosa + hh * sina), round(y - hh * cosa - hw * sina))
            top_right = (round(x + hw * cosa + hh * sina), round(y - hh * cosa + hw * sina))
            bottom_right = (round(x + hw * cosa - hh * sina), round(y + hh * cosa + hw * sina))
            bottom_left = (round(x - hw * cosa - hh * sina), round(y + hh * cosa - hw * sina))
            self._corners = np.array([top_left, top_right, bottom_right, bottom_left])
        return self._corners

    @staticmethod
    def is_between(value, range_):
        return range_[0] <= value <= range_[1]
