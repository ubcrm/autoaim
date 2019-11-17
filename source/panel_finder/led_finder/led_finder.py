from source.common.shape_finder import ShapeFinder
from source.common.bit_mask import Bitmask
from source.common.module import Module
from pathlib import Path
import os


class LEDFinder(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.bitmasker = Bitmask()
        self.shape_finder = ShapeFinder()

    def process(self, frame):
        mask = self.bitmasker.process(frame)
        return self.shape_finder.process(mask)
