from module import Module
from pathlib import Path
import os


class Receiver(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self):
        # todo: return robot state received from embedded
        return self.config['state']['robot']
