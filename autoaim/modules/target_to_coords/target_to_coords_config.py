import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'


#PIXEL_SIZE= 0.00000112 #pixel zise is 1.12 µm by 1.12 µm
PIXEL_SIZE= 0.0000014
#FOCU_LENGTH=0.00304   #focu length is 3.04 mm
FOCU_LENGTH=0.0028   #focu length is 3.04 mm
#
# TOTAL_NUMBER_OF_PIXELS_IN_X_AXIS=3280
# TOTAL_NUMBER_OF_PIXELS_IN_Y_AXIS=2464
# #Sensor resolution is 3280 × 2464 pixels

TOTAL_NUMBER_OF_PIXELS_IN_X_AXIS_IN_VEDIO=540
TOTAL_NUMBER_OF_PIXELS_IN_Y_AXIS_IN_VEDIO=500
# resolution of video, video might have different resolution than raw data from camera

TOTAL_NUMBER_OF_PIXELS_IN_X_AXIS_OF_CAMERA=1920
TOTAL_NUMBER_OF_PIXELS_IN_Y_AXIS_OF_CAMERA=1080
# resolution of camera
