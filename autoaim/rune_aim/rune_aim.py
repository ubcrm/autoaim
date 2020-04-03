from assets.module import Module
from pathlib import Path
import os
from .leaf_find.leaf_find import LeafFind
from .leaf_aim.leaf_aim import LeafAim


class RuneAim(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.leaf_find = LeafFind(self)
        self.leaf_aim = LeafAim(self)

    def process(self, frame):
        # todo: return gimbal angles to aim at rune
        pass
