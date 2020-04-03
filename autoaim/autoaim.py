from assets.module import Module
from pathlib import Path
import os
import cv2
from receive.receive import Receive
from robot_aim import RobotAim
from rune_aim.rune_aim import RuneAim
from target_map.target_map import TargetMap
from transmit.transmit import Transmit


class Autoaim(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.receive = Receive(self)
        self.robot_aim = RobotAim(self)
        self.rune_aim = RuneAim(self)
        self.target_map = TargetMap(self)
        self.transmit = Transmit(self)

        self.mode = self.config['mode_robot']
        self.count_frame = 0

    def process(self):
        """
        Run vision autoaim in different modes.
        """
        feed = cv2.VideoCapture(self.config['feed'])

        while True:
            if self.mode is self.config['mode_robot']:
                _, frame = feed.read()
                self.count_frame += 1
                target_coords = self.target_map.process(self.robot_aim.process(frame))
                self.transmit.process(target_coords)

            elif self.mode is self.config['mode_rune']:
                _, frame = feed.read()
                self.count_frame += 1
                self.transmit.process(self.rune_aim.process(frame))

            elif self.mode is self.config['mode_sleep']:
                cv2.waitKey(self.config['delay'])

            received_mode = self.receive.process()
            if received_mode is not None:  # change mode if embedded requested it
                self.mode = received_mode
