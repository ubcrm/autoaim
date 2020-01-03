from source.module import Module
from pathlib import Path
import os
import cv2
import numpy as np
from math import sin, cos, radians


class LedFinder(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        # not sure if this is the best way to pass dimensions through
        self.config['distance']['height_1m'] = self.config['distance']['height_1m_rel'] * \
                                               self.parent.config['view']['dims'][1]

    def process(self, mask):
        """
        Find leds from a mask of the frame
        :param mask: led mask of the frame
        :return: tuple of two lists of BoundingRect objects that are leds, not leds
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        leds = []
        not_leds = []
        for i, contour in enumerate(contours):
            bounding_rect = BoundingRect(i + 1, cv2.minAreaRect(contour), self.config)
            if bounding_rect.is_led:
                leds.append(bounding_rect)
            else:
                not_leds.append(bounding_rect)

        return leds, not_leds


class BoundingRect:
    def __init__(self, label, rect, config):
        """
        Represent a bounding rectangle (possibly an led)
        :param label: label to identify the bounding rectangle
        :param rect: cv2.rectangle object representing the bounding rectangle
        :param config: dictionary of led criteria and other settings
        """
        self.label = str(label)
        self.center = (round(rect[0][0]), round(rect[0][1]))
        self.width = round(min(rect[1]))
        self.height = round(max(rect[1]))
        self.distance = 1 / max(1e-3, self.height / config['distance']['height_1m'] + config['distance']['offset'])

        # this angle adjustment part was a little tricky to figure out
        # after adjustment -90 <= self.angle < 90 always
        self.angle = round(rect[2])
        if min(rect[1]) != rect[1][0]:
            self.angle += 90
            if self.angle >= 90:
                self.angle -= 180

        (x, y), hw, hh, a = self.center, self.width / 2, self.height / 2, radians(self.angle)
        top_left = (round(x - hw * cos(a) + hh * sin(a)), round(y - hh * cos(a) - hw * sin(a)))
        top_right = (round(x + hw * cos(a) + hh * sin(a)), round(y - hh * cos(a) + hw * sin(a)))
        bottom_right = (round(x + hw * cos(a) - hh * sin(a)), round(y + hh * cos(a) + hw * sin(a)))
        bottom_left = (round(x - hw * cos(a) - hh * sin(a)), round(y + hh * cos(a) - hw * sin(a)))
        self.corners = [top_left, top_right, bottom_right, bottom_left]

        self.confidences = [
            bump_func(self.distance, *config['criteria']['distance']),
            bump_func(self.height / max(1e-3, self.width), *config['criteria']['ratio_dims']),
            bump_func(self.angle, *config['criteria']['angle'])
        ]
        self.confidence = float(np.prod(self.confidences))
        self.is_led = self.confidence >= config['criteria']['led']

    def log(self):
        attributes = [
            'width=%d' % self.width,
            'height=%d' % self.height,
            'angle=%d' % self.angle,
            'center%s' % str(self.center),
            'distance=%.2f' % self.distance,
            'is_led=%s' % str(self.is_led)
        ]
        confidences = [
            'distance=%.2f' % self.confidences[0],
            'ratio_dims=%.2f' % self.confidences[1],
            'angle=%.2f' % self.confidences[2]
        ]
        print('Led %s: %s | %s' % (self.label, ' '.join(attributes), ' '.join(confidences)))


def bump_func(x, x_left_zero, x_left_one, x_right_zero, x_right_one):
    if x_left_zero <= x < x_left_one:
        return (x - x_left_zero) / (x_left_one - x_left_zero)
    elif x_left_one <= x <= x_right_one:
        return 1.0
    elif x_right_one < x <= x_right_one:
        return (x - x_right_zero) / (x_right_one - x_right_zero)
    else:
        return 0.0
