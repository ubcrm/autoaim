from assets.module import Module
from pathlib import Path
import os


class Transmit(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self, target):
        """
        Send target coordinates to embedded.
        # TODO: Insert description of transmitted message format
        :param target: For robot mode, see target_map output. For rune mode,
        see rune_aim output.
        """
        # TODO: Implement
        pass
