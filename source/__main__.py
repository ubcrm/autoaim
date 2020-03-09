from source import Source
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feed', default='0', help='Feed option: capture device #')
    args = vars(parser.parse_args())

    source = Source(None, **args)
    source.process()
