from module import Module
from pathlib import Path
import os


class PanelSelector(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, panels):
        """
        :param panels: list of potential target panels
        :return: target panel
        """
        # todo: implement
        return panels[0]
