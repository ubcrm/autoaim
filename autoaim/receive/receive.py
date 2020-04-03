from assets.module import Module
from pathlib import Path
import os
import serial


class Receive(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

    def process(self):
        """
        Receive communication from embedded.
        TODO: Insert description of received message format
        :return: Mode identifier if mode change is requested by embedded,
        None otherwise. Mode identifiers are defined in autoaim config.

        """
        # TODO: Implement
        pass
