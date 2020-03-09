from module import Module
from pathlib import Path
import os
import cv2
import numpy as np


class Masker(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        frame_height = parent.robot_cropper.config['dims'][1]
        self.config['dilation'] = round(self.config['dilation_rel'] * frame_height)
        self.config['morph']['abs'] = [round(val * frame_height) for val in self.config['morph']['rel']]

    def process(self, roi):
        """
        :param roi: to be masked
        :return: led mask of roi
        """
        mask = cv2.inRange(roi, tuple(self.config['range'][0]), tuple(self.config['range'][1]))
        # mask = cv2.dilate(mask, np.ones((self.config['dilation'], self.config['dilation'])))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, tuple(self.config['morph']['abs']))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        return mask
