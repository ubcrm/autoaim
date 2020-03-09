from module import Module
from pathlib import Path
import os
import cv2
from .led_finder.led_finder import LedFinder
from .led_matcher.led_matcher import LedMatcher
from .visualizer.visualizer import Visualizer
from .masker.masker import Masker
from .robot_cropper.robot_cropper import RobotCropper
from .panel_selector.panel_selector import PanelSelector


class PanelFinder(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        self.config['view']['dims'] = [round(dim * self.config['view']['scale'])
                                       for dim in self.parent.config['feed_dims']]

        self.robot_cropper = RobotCropper(self)
        self.masker = Masker(self)
        self.led_finder = LedFinder(self)
        self.led_matcher = LedMatcher(self)
        self.panel_selector = PanelSelector(self)
        if self.parent.config['mode'] != 'compete':
            self.visualizer = Visualizer(self)

        self.frame_count = 0

    def process(self, frame):
        """
        :param frame: frame of the feed
        :return: target panel
        """
        roi = self.robot_cropper.process(frame)
        mask = self.masker.process(roi)

        leds, not_leds = self.led_finder.process(mask)
        panels, not_panels = self.led_matcher.process(leds)
        target_panel = self.panel_selector.process(panels)

        self.frame_count += 1
        if self.parent.config['mode'] != 'compete':
            self.visualizer.process(frame, roi, leds, not_leds, panels, not_panels, target_panel)
            if self.parent.config['mode'] == 'debug':
                cv2.imshow(self.config['title_roi'], roi)
                cv2.imshow(self.config['title_mask'], mask)
            cv2.imshow(self.config['title_frame'], frame)

        return target_panel


