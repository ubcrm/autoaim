from assets.module import Module
from pathlib import Path
import os


class PanelSelect(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, panels):
        """
        :return: The panel to target which is an LedPair instance.
        """
        # TODO: Implement
        return panels[0]
