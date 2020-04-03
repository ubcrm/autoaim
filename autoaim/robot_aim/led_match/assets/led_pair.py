from math import sqrt, degrees, atan


class LedPair:
    def __init__(self, led1, led2):
        """
        Represent an led pair (possibly a target)
        :param led1, led2: pair of BoundingRect objects that are leds
        """
        self.led_left = led1 if led1.center[0] < led2.center[0] else led2
        self.led_right = led2 if led1.center[0] < led2.center[0] else led1
        self.label = self.led_left.label + '-' + self.led_right.label

        delta_x = self.led_right.center[0] - self.led_left.center[0]
        delta_y = self.led_right.center[1] - self.led_left.center[1]
        topleft, _, _, bottomleft = self.led_left.corners
        _, topright, bottomright, _ = self.led_right.corners
        self.corners = [topleft, topright, bottomright, bottomleft]

        self.center = (round((led1.center[0] + led2.center[0]) / 2), round((led1.center[1] + led2.center[1]) / 2))
        self.width = round(sqrt(delta_x ** 2 + delta_y ** 2) + (led1.width + led2.width) / 2)
        self.height = round((led1.height + led2.height) / 2)
        self.angle = round((led1.angle + led2.angle) / 2)
        self.angle_mid = round(degrees(atan(delta_y / max(1e-3, delta_x))))
        self.distance = (led1.distance + led2.distance) / 2

        self.confidences = None
        self.is_panel = None

    def log(self):
        attributes = [
            'center=%s' % str(self.center),
            'width=%d' % self.width,
            'height=%d' % self.height,
            'angle=%d' % self.angle,
            'angle_mid=%d' % self.angle_mid,
            'distance=%.2f' % self.distance,
            'is_panel=%s' % str(self.is_panel)
        ]
        confidences = [(criterion + '=%.2f' % value) for criterion, value in self.confidences.items()]
        print('Panel %s: %s | %s' % (self.label, ' '.join(attributes), ' '.join(confidences)))
