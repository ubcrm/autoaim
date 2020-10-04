from autoaim_config import *
from autoaim import autoaim
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=os.path.abspath, help='input video path')
    parser.add_argument('-s', '--source', type=int, default=DEFAULT_SOURCE, help='video device number')
    parser.add_argument('-d', '--debug', nargs='?', const=True, default=DEFAULT_DO_DEBUG, help='debug mode')
    args = parser.parse_args()

    source = args.video if args.video is not None else args.source
    autoaim(source, do_debug=args.debug)

