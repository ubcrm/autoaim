import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

SCALE_FRAME = 2
ROI_PERIOD = 20


class CROP:
    MARGIN_SMALL = 150
    MARGIN_LARGE = 400


class DEBUG:
    COLOUR = (0, 255, 0)
    THICKNESS = 2
