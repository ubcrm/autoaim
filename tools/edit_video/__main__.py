from edit_video_config import *
from edit_video import EditVideo
import os


if __name__ == '__main__':
    filenames = [f for f in os.listdir(str(ASSETS_DIR)) if os.path.isfile(str(ASSETS_DIR / f))]

    for i, filename in enumerate(filenames):
        video = EditVideo(filename)
        video.rotate_ccw().export()
