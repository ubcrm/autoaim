import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

#TODO: dict or in ./_assests/ or a mask_assests.yml thing?
range: [[0, 0, 250], [180, 255, 255]]

dilate_rel: 0.0037  # [resized frame height] dilation size
dilate:  # [pixel] dilation size

morph_rel: [0.0025, 0.008]  # [resized frame height] mask morphing size
morph:  # [pixel] mask morphing size
