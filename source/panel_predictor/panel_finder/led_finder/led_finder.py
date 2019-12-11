from source.module import Module
from pathlib import Path
import os
import cv2


class LEDFinder(Module):
    def __init__(self, parent, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)

    def process(self, frame):
        """
        finds panel leds in an image
        :param frame: bgr image that may contain panel leds
        :return: [] list of rectangle dictionaries
        """
        mask = self.under_exposed_threshold(frame)
        rectangles = self.find_rectangles(mask)

        leds = []
        for r in rectangles:
            reformat = self.reformat_cv_rectangle(r)
            leds.append(reformat)
        return leds

    @staticmethod
    def under_exposed_threshold(image):
        blurred = cv2.blur(image, (round(image.shape[1] / 500), round(image.shape[0] / 54)))
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        bright = cv2.inRange(hsv, (150, 0, 200), (200, 255, 250))
        return bright

    @staticmethod
    def reformat_cv_rectangle(rect):
        """
        converts from an openCV rectangle to a dict style rectangle
        :param rect: an openCV rectangle
        :return: a dictionary rectangle
        """
        rect_dict = {"width": rect[1][0], "height": rect[1][1],
                     "x_center": rect[0][0], "y_center": rect[0][1],
                     "angle": rect[2]}

        return rect_dict

    @staticmethod
    def find_rectangles(filtered):
        """
        finds rectangles around leds
        :param filtered: a binary image of suspected leds
        :return: a list of rectangles in the format ((centerX,centerY),(width,height),(rotation))
        """
        # puts rectangles on blobs
        contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rectangles = []
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            if max(rect[1]) > round(filtered.shape[0] / 35) and max(rect[1]) > 2 * min(rect[1]):
                if rect[1][0] > rect[1][1] and rect[2] > -45:
                    rect = ((rect[0][0], rect[0][1]), (rect[1][1], rect[1][0]), rect[2] - 90)
                rectangles.append(rect)
        return rectangles
