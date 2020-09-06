import find_leds_config as CONFIG
import cv2


class FindLeds:
    def __init__(self):
        pass

    def run(self, mask):
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
