from module import Module
from pathlib import Path
import os


class Sender(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, aim_angles):
        # todo: send aim coordinate angles to embedded
        pass
