from source.module import Module
from pathlib import Path
import os
import math


class GimbalAngleFinder(Module):
    def __init__(self, parent=None, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)

    # Processes screen coords and frame and converts them to a set of angles
    def process(self, x, y, frame_dims):
        adj_x = x - (frame_dims[0] / 2)
        adj_y = y - (frame_dims[1] / 2)
        horiz_angle = math.radians((adj_x / (frame_dims[0] / 2)) * self.properties["horiz_fov"])
        vert_angle = math.radians((adj_y / (frame_dims[1] / 2)) * self.properties["vert_fov"])
        return horiz_angle, vert_angle



