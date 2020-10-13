import autoaim_config
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=os.path.abspath, help='input video path')
    parser.add_argument('-s', '--source', type=int, default=autoaim_config.SOURCE, help='video device number')
    parser.add_argument('-d', '--debug', nargs='?', const=True, default=autoaim_config.DO_DEBUG, help='debug mode')
    args = parser.parse_args()

    autoaim_config.SOURCE = args.video if args.video is not None else args.source
    autoaim_config.DO_DEBUG = args.debug

    from autoaim import autoaim
    autoaim()

