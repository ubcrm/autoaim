from assets.module import Module
from pathlib import Path
import os
import cv2
from .assets.bounding_rect import BoundingRect


class LedFind(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        # not sure if this is the best way to pass dimensions through
        self.config['distance']['height_1m'] = self.config['distance']['height_1m_rel'] * \
                                               self.parent.robot_crop.config['dims'][1]

    def process(self, mask):
        """
        Find leds from a mask of the ROI.
        :return: Two lists of leds, not_leds with BoundingRect objects
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
