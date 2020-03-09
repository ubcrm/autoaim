from module import Module
from pathlib import Path
import os
import cv2
from receiver.receiver import Receiver
from sender.sender import Sender
from robot_aimer.robot_aimer import RobotAimer
from rune_aimer.rune_aimer import RuneAimer


class Source(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.sender = Sender(self)
        self.receiver = Receiver(self)
        self.robot_aimer = RobotAimer(self)
        self.rune_aimer = RuneAimer(self)

    def process(self):
        feed = cv2.VideoCapture(self.config['feed'])
        while True:
            state = self.receiver.process()

            if state == self.receiver.config['state']['quit']:
                cv2.waitKey(self.config['delay'])
            elif state == self.receiver.config['state']['robot']:
                for i in range(self.config['focus_span']):
                    _, frame = feed.read()
                    self.sender.process(self.robot_aimer.process(frame))
            elif state == self.receiver.config['state']['rune']:
                for i in range(self.config['focus_span']):
                    _, frame = feed.read()
                    self.sender.process(self.rune_aimer.process(frame))
