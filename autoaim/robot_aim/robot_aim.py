from assets.module import Module
from pathlib import Path
import os
import cv2
from robot_crop.robot_crop import RobotCrop
from led_mask.led_mask import LedMask
from led_find.led_find import LedFind
from led_match.led_match import LedMatch
from panel_select.panel_select import PanelSelect
from panel_predict.panel_predict import PanelPredict
from robot_visualize.robot_visualize import RobotVisualize


class RobotAim(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.robot_crop = RobotCrop(self)
        self.led_mask = LedMask(self)
        self.led_find = LedFind(self)
        self.led_match = LedMatch(self)
        self.panel_select = PanelSelect(self)
        self.panel_predict = PanelPredict(self)
        if self.config['mode'] != 'compete':
            self.robot_visualize = RobotVisualize(self)

    def process(self, frame):
        """
        :param frame: BGR feed frame. Dimensions are defined in autoaim config.
        :return: Target coordinates on original frame (x, y) in units pixels.
        The origin of coordinates is top-left corner of frame with y pointing down.
        """
        roi = self.robot_crop.process(frame)
        mask = self.led_mask.process(roi)
        leds, not_leds = self.led_find.process(mask)
        panels, not_panels = self.led_match.process(leds)
        panel = self.panel_select.process(panels)
        target = self.panel_predict.process(panel)

        if self.config['mode'] != 'compete':
            self.robot_visualize.process(frame, roi, leds, not_leds, panels, not_panels, panel, target)
            if self.config['mode'] == 'debug':
                cv2.imshow(self.config['title_roi'], roi)
                cv2.imshow(self.config['title_mask'], mask)
            cv2.imshow(self.config['title_frame'], frame)

        return target
