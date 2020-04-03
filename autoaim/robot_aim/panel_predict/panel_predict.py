from assets.module import Module
from pathlib import Path
import os


class PanelPredict(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, panel):
        """
        Predict the position of panel's center in future.
        """
        # TODO: Implement
        return panel.center
