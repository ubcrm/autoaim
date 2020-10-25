import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'


PIXEL_SIZE= 0.00000112 #pixel zise is 1.12 µm by 1.12 µm
FOCU_LENGTH=0.00304   #focu length is 3.04 mm


TOTAL_NUMBER_OF_PIXELS_IN_X_AXIS=3280
TOTAL_NUMBER_OF_PIXELS_IN_Y_AXIS=2464
#Sensor resolution is 3280 × 2464 pixels
