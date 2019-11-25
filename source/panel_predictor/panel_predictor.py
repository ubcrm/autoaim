from source.common.module import Module
from pathlib import Path
import os
from source.panel_predictor.panel_finder.panel_finder import PanelFinder


class PanelPredictor(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.panel = None
        self.panel_finder = PanelFinder(state=state)  # this panel finder needs no additional properties

    def process(self, frame):
        panel = self.panel_finder.process(frame)
        if panel is not None:
            return panel["x_center"], panel["y_center"]
