from pathlib import Path
from .module import Module
import os
import cv2


def under_exposed_threshold(image):
    blurred = cv2.blur(image, (round(image.shape[1] / 500), round(image.shape[0] / 54)))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    bright = cv2.inRange(hsv, (150, 0, 200), (200, 255, 250))
    return bright


class Bitmask(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)

    def process(self, frame):
        under_exposed_threshold(frame)

