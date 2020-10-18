import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

EPSILON = 1E-5
LABEL_FORMAT = '{}-{}'
DRAW_NOT_PANELS = False


class CRITERIA:
    ANGLE_DIFF = (0, 4)
    ASPECT_RATIO = (2, 4)
    RATIO_LEDS = (0.8, 1.25)


class DRAW:
    COLOR_PANEL = (0, 0, 255)
    COLOR_NOT_PANEL = (0, 220, 255)

    THICKNESS = 1
    FONT = 0  # choose OpenCV font
    FONT_SIZE = 0.46
    LABEL_OFFSET = (-15, 4)
