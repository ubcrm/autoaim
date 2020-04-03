from assets.module import Module
from pathlib import Path
import os


class TargetMap(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, target):
        """
        Map target coordinates on frame to real-world cylindrical coordinates.
        :param target: See robot_aim output.
        :return: Real-world cylindrical coordinates of target (r, phi, z) in units
        meters for lengths and radians for angles. The origin of the coordinates
        is the intersection of the pitch and yaw axis of the gimbal, with z pointing up.
        """
        # todo ...
        pass
