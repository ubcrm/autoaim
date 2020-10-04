import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

DEFAULT_SOURCE = 0
DEFAULT_DO_DEBUG = False
CAPTURE_ERROR = 'Failed to read from video source "{}".'

WIN_TITLE = 'Debug Output'
FRAME_DELAY = 40  # (ms)
