from module import Module
from pathlib import Path
import os
import cv2
from .panel_finder.panel_finder import PanelFinder
from .panel_aimer.panel_aimer import PanelAimer


class RobotAimer(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.panel_finder = PanelFinder(self)
        self.panel_aimer = PanelAimer(self)

    def process(self, frame):
        """
        :param frame: of the opponent robot
        """
        aim_angles = self.panel_aimer.process(self.panel_finder.process(frame))
        return aim_angles
