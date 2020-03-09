from module import Module
from pathlib import Path
import os
import cv2


class RobotCropper(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, frame):
        """
        :param frame: of robot
        :return: roi cropped around the robot
        """
        # todo: implement robot cropping
        if self.config['scale'] != 1:
            frame = cv2.resize(frame, tuple(self.config['dims']))
        return frame
