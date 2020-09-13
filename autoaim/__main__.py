import autoaim_config as CONFIG
from autoaim import autoaim
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=os.path.abspath, help='input video path')
    parser.add_argument('-s', '--source', type=int, default=CONFIG.DEFAULT_SOURCE, help='video device number')
    args = parser.parse_args()

    source = args.video if args.video is not None else args.source
    autoaim(source)
