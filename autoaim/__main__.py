import argparse
import os
from autoaim import autoaim

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=0, help='execution mode 0/1/2 for run/debug/test')
    parser.add_argument('-s', '--source', type=int, default=0, help='video device number')
    parser.add_argument('-v', '--video', type=os.path.abspath, help='input video path')
    parser.add_argument('-d', '--data_file', type=os.path.abspath, help='test data file path')
    args = parser.parse_args()

    source = args.video if (args.video is not None) else args.source
    autoaim(source, mode=args.mode, data_file=args.data_file)
