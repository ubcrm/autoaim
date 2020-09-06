from create_module import CreateModule
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a template module.')
    parser.add_argument('name_lower', help='module name in lowercase_with_underscores')
    parser.add_argument('-d', '--dir_create', default='.', type=os.path.abspath, help='relative creation directory')
    parser.add_argument('-m', '--create_main', nargs='?', const=True, default=False, help='whether to create main file')
    args = parser.parse_args()

    modularize = CreateModule(args.name_lower, args.dir_create)
    modularize.run(create_main=args.create_main)
