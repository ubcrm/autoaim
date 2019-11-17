from source.common.module import Module
from pathlib import Path
import os


class Preprocess(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)

    def process(self, frame):
        frame = frame.copy()
        dims = frame.shape[:2]
        top = round((dims[0] * (1 - self.properties["y_scaling"])) / 2)
        bottom = dims[0] - top
        left = round((dims[1] * (1 - self.properties["x_scaling"])) / 2)
        right = dims[1] - left
        print(dims)
        print(top, bottom, left, right)
        crop_img = frame[top:bottom, left:right]
        return crop_img
