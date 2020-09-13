import create_module_config as CONFIG
from create_module import create_module
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a template module.')
    parser.add_argument('name_lower', help='module name in lowercase_with_underscores')
    parser.add_argument('-d', '--creation_dir', default='.', type=os.path.abspath, help='relative creation directory')
    parser.add_argument('-m', '--create_main', nargs='?', const=True, default=CONFIG.DEFAULT_CREATE_MAIN,
                        help='whether to create main file')
    args = parser.parse_args()
    create_module(args.name_lower, args.creation_dir, create_main=args.create_main)
