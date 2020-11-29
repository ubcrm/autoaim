from pathlib import Path
import os

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIRECTORY = DIR / f'{os.path.basename(DIR)}_assets'


def template():
    pass
