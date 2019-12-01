from source.common.shape_finder import ShapeFinder
from source.common.bit_mask import Bitmask
from source.common.module import Module
from pathlib import Path
import os


class LEDFinder(Module):
    def __init__(self, parent, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        self.bitmasker = Bitmask(self)
        self.shape_finder = ShapeFinder(self)

    def process(self, frame):
        """
        finds panel leds in an image
        :param frame: bgr image that may contain panel leds
        :return: [] list of rectangle dictionaries
        """
        mask = self.bitmasker.process(frame)
        return self.shape_finder.process(mask)
