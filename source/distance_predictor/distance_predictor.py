from source.module import Module
from pathlib import Path
import os

class DistancePredictor(Module):
    def init(self, parent=None, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
