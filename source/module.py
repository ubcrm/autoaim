from pathlib import Path
import os
import yaml


class Module:
    def __init__(self, wd, parent, config):
        self.parent = parent
        try:

            self.config = yaml.full_load(Path(wd / ('%s.yml' % os.path.basename(wd))).read_text())
        except FileNotFoundError:
            self.config = {}
        # merge default configuration and passed configuration, the latter overrides
        self.config.update(config)
