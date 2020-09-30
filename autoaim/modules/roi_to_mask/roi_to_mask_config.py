import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

RANGE = ((0, 0, 250), (180, 255, 255))
DILATE_REL = 0.0037  # (roi frame height)
MORPH_REL = (0.0025, 0.008)  # (roi frame height)

DEBUG_MASK_WEIGHT = 0.7
