import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

SCALE_FRAME = 3
ROI_PERIOD = 15


class CROP:
    MARGIN_SMALL = 50
    MARGIN_LARGE = 200


class DEBUG:
    COLOUR = (0, 255, 0)
    THICKNESS = 2
