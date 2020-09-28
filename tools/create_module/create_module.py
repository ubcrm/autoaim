from create_module_config import *
from pathlib import Path
import os
import re

name_lower = None
name_pascal = None


def create_module(name, creation_dir, create_main=DEFAULT_CREATE_MAIN):
    global name_lower, name_pascal
    name_lower = name
    name_pascal = convert_lower_to_pascal(name_lower)
    module_dir = Path(creation_dir) / name_lower

    assert_name_is_lower(name)
    assert_creation_dir_exists(creation_dir)
    assert_no_module_dir_exists(module_dir)

    os.mkdir(module_dir)
    os.mkdir(module_dir / f'{name_lower}_assets')

    create_module_file(module_dir, INIT_FILENAME)
    create_module_file(module_dir, BASE_FILENAME)
    create_module_file(module_dir, CONFIG_FILENAME)
    if create_main:
        create_module_file(module_dir, MAIN_FILENAME)


def create_module_file(module_dir, filename_format):
    module_filepath = str(module_dir / filename_format.format(name_lower))
    template_filepath = ASSETS_DIRECTORY / filename_format.format(TEMPLATE_LOWER)
    with open(module_filepath, 'w') as file:
        content = generate_template_content(template_filepath)
        file.write(content)


def generate_template_content(filepath):
    content = filepath.read_text().replace(TEMPLATE_LOWER, name_lower) \
        .replace(TEMPLATE_PASCAL, name_pascal)
    return content


def convert_lower_to_pascal(name):
    return name.title().replace('_', '')


def assert_name_is_lower(name):
    lowercase_pattern = r'^[a-z]+(_[a-z]+)*$'  # pattern matching lowercase_with_underscores
    if not re.match(lowercase_pattern, name):
        raise RuntimeError(NAME_NOT_LOWERCASE_ERROR.format(name))


def assert_creation_dir_exists(creation_dir):
    if not os.path.exists(creation_dir):
        raise RuntimeError(NO_CREATION_DIR_EXISTS_ERROR.format(creation_dir))


def assert_no_module_dir_exists(module_dir):
    if os.path.exists(module_dir):
        raise RuntimeError(MODULE_DIR_EXISTS_ERROR.format(module_dir))
