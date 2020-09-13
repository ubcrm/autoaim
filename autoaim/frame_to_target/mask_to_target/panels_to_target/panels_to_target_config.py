import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'


class DRAW:
    TARGET_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 255)

    TARGET_RADIUS = 3
    DISTANCE_FORMAT = '%.2f'
    DISTANCE_OFFSET = (-16, -16)
    FONT = 0  # choose OpenCV font
    FONT_SIZE = 0.46
