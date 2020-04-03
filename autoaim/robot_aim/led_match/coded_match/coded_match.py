from assets.module import Module
from pathlib import Path
import os
import numpy as np
from ...led_find.assets.bounding_rect import linear_bump


class CodedMatch(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, led_pair):
        """
        Assign confidences and determine whether an led pair is a target
        :param led_pair: an LedPair object
        :return: True if led pair is a target, False otherwise
        """
        led_pair.confidences = {
            'angle_delta': linear_bump(abs(led_pair.led_left.angle - led_pair.led_right.angle),
                                       *self.config['criteria']['angle_delta']),
            'ratio_dims': linear_bump(led_pair.width / max(1e-3, led_pair.height),
                                      *self.config['criteria']['ratio_dims']),
            # skew property was obtained by trial and error - we should work out the theory behind it
            'skew': linear_bump(led_pair.width / max(1e-3, led_pair.height) - 12 /
                                max(1e-3, abs(led_pair.angle_mid - led_pair.angle)), *self.config['criteria']['skew'])
        }
        led_pair.is_panel = float(np.prod(list(led_pair.confidences.values()))) >= self.config['criteria']['target']
