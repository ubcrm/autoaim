from autoaim import Autoaim
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--capture_device', default=0, help='capture device number')
    args = parser.parse_args()

    autoaim = Autoaim()
    autoaim.run(args.capture_device)
