from frame_to_target_config import *
from frame_to_target import frame_to_target
import argparse
import cv2
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=os.path.abspath, help='input video path')
    parser.add_argument('-s', '--source', type=int, default=DEFAULT_SOURCE, help='video device number')
    parser.add_argument('-d', '--debug', nargs='?', const=True, default=DEFAULT_DEBUG, help='debug mode')
    args = parser.parse_args()

    source = args.video if args.video is not None else args.source
    capture = cv2.VideoCapture(source)
    successful, frame = capture.read()

    if not successful:
        raise RuntimeError(CAPTURE_ERROR.format(source))

    while successful:
        frame_to_target(frame, debug=args.debug)
        successful, frame = capture.read()
