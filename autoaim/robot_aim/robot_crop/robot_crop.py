from assets.module import Module
from pathlib import Path
import os
import cv2


class RobotCrop(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.config['dims'] = [round(dim * self.config['scale'])
                               for dim in self.parent.parent.config['feed_dims']]

    def process(self, frame):
        """
        :return: Cropped region of interest (ROI) of the frame around the target robot.
        ROI dimensions may vary.
        """
        # TODO: Implement robot cropping
        if self.config['scale'] != 1:
            frame = cv2.resize(frame, tuple(self.config['dims']))
        return frame
