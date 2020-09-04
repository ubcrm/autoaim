import os
from pathlib import Path

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIRECTORY = DIR / f'{NAME}_assets'

MAIN_FILENAME = '__main__.py'
BASE_FILENAME = '{}.py'
CONFIG_FILENAME = '{}_config.py'

TEMPLATE_LOWER = 'template'
TEMPLATE_PASCAL = 'Template'

NAME_NOT_LOWERCASE_ERROR = 'Module name "{}" does not follow lowercase_with_underscores'
NO_CREATE_DIR_EXISTS_ERROR = 'Creation directory "{}" does not exist'
MODULE_DIR_EXISTS_ERROR = 'Module directory "{}" already exists'
