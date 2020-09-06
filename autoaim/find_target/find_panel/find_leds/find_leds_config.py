import os
from pathlib import Path


DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

distance:  # fitted distance function
  height_1m_rel: 0.078  # [frame height] realtive led height at 1 meter distance
  height_1m:  # [pixel] assigned during runtime based on frame height
  offset: 0.0267

criteria:  # confidence config for an led
  distance: [0.3, 0.5, 3, 4]  # [meter]
  ratio_dims: [1.5, 2.5, 100, 100]
  angle: [-30, -20, 20, 30]  # [degree]

  led: 0.5  # minimum confidence to consider an led valid
