from module import Module
from pathlib import Path
import os


class LeafFinder(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, frame):
        # todo: return target leaf object
        pass
