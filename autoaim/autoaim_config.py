import os
from pathlib import Path


DO_DEBUG = False  # shared between all modules

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

SOURCE = 0
CAPTURE_ERROR = 'Failed to read from video source "{}".'

DEBUG_WIN_TITLE = 'Debug Output'
DEBUG_SCALE = 2
FRAME_DELAY = 0  # (ms)
LEG_FRAME = '---------- Frame {} ----------'
