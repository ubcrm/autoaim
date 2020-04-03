import numpy as np
from math import sin, cos, radians


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
        self.angle = round(rect[2])
        if min(rect[1]) != rect[1][0]:
            self.angle += 90
            if self.angle >= 90:
                self.angle -= 180  # after this adjustment -90 <= self.angle < 90
        self.distance = 1 / max(1e-3, self.height / config['distance']['height_1m'] + config['distance']['offset'])

        # TODO: Can replace this with some library function
        (x, y), hw, hh, a = self.center, self.width / 2, self.height / 2, radians(self.angle)
        sina, cosa = sin(a), cos(a)
        topleft = (round(x - hw * cosa + hh * sina), round(y - hh * cosa - hw * sina))
        topright = (round(x + hw * cosa + hh * sina), round(y - hh * cosa + hw * sina))
        bottomright = (round(x + hw * cosa - hh * sina), round(y + hh * cosa + hw * sina))
        bottomleft = (round(x - hw * cosa - hh * sina), round(y + hh * cosa - hw * sina))
        self.corners = [topleft, topright, bottomright, bottomleft]

        self.confidences = {
            'distance': linear_bump(self.distance, *config['criteria']['distance']),
            'ratio_dims': linear_bump(self.height / max(1e-3, self.width), *config['criteria']['ratio_dims']),
            'angle': linear_bump(self.angle, *config['criteria']['angle'])
        }
        self.is_led = np.prod(list(self.confidences.values())) >= config['criteria']['led']

    def log(self):
        attributes = [
            'center%s' % str(self.center),
            'width=%d' % self.width,
            'height=%d' % self.height,
            'angle=%d' % self.angle,
            'distance=%.2f' % self.distance,
            'is_led=%s' % str(self.is_led)
        ]
        confidences = [(criterion + '=%.2f' % value) for criterion, value in self.confidences.items()]
        print('Led %s: %s | %s' % (self.label, ' '.join(attributes), ' '.join(confidences)))


def linear_bump(x, x_left_zero, x_left_one, x_right_zero, x_right_one):
    if x_left_zero <= x < x_left_one:
        return (x - x_left_zero) / (x_left_one - x_left_zero)
    elif x_left_one <= x <= x_right_one:
        return 1.0
    elif x_right_one < x <= x_right_one:
        return (x - x_right_zero) / (x_right_one - x_right_zero)
    else:
        return 0.0
