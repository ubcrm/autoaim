import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

EPSILON = 1E-5
LABEL_FORMAT = '{}-{}'


class CRITERIA:
    ANGLE_DIFF = (0, 4)
    ASPECT_RATIO = (0.9, 3)
    RATIO_LEDS = (0.67, 1.5)


class DRAW:
    COLOR_PANEL = (0, 0, 255)
    COLOR_NOT_PANEL = (0, 220, 255)

    THICKNESS = 2
    FONT = 0  # choose OpenCV font
    FONT_SIZE = 0.46
    LABEL_OFFSET = (-15, 4)
