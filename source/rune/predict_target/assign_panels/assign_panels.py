from source.common.module import Module
from pathlib import Path
import os


class AssignPanels(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.theta = 0

    def process(self, image, state=False):
        self.theta -= 0.015
        return {self.theta: "target"}
