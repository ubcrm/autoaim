from source.module import Module
from pathlib import Path
import os
import cv2
from .led_finder.led_finder import LedFinder
from .led_matcher.led_matcher import LedMatcher
from .visualizer.visualizer import Visualizer
import numpy as np


class PanelFinder(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        self.config['view']['dims'] = [round(dim * self.config['view']['scale'])
                                       for dim in self.parent.config['feed_dims']]
        self.config['mask']['dilation'] = round(self.config['mask']['dilation_rel'] * self.config['view']['dims'][1])

        self.led_finder = LedFinder(self)
        self.led_matcher = LedMatcher(self)
        self.frame_count = 0
        if self.parent.config['mode']:
            self.visualizer = Visualizer(self, )

    def process(self, frame):
        """
        Find panels in the frame
        :param frame: frame of the feed
        :return: list of LedPair objects that are panels
        """
        if self.config['view']['scale'] != 1:
            frame = cv2.resize(frame, tuple(self.config['view']['dims']))
        mask = cv2.inRange(frame, tuple(self.config['mask']['range'][0]), tuple(self.config['mask']['range'][1]))
        mask = cv2.dilate(mask, np.ones((self.config['mask']['dilation'], self.config['mask']['dilation'])))
        leds, not_leds = self.led_finder.process(mask)
        panels, not_panels = self.led_matcher.process(leds)

        self.frame_count += 1
        if self.parent.config['mode'] != 'compete':
            self.visualizer.process(frame, self.frame_count, leds, not_leds, panels, not_panels)
            if self.parent.config['mode'] == 'debug':
                cv2.imshow(self.config['view']['title_mask'], mask)
            cv2.imshow(self.config['view']['title_frame'], frame)

        return panels


