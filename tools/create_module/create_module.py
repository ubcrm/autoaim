from pathlib import Path
import os
import re

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIRECTORY = DIR / f'{os.path.basename(DIR)}_assets'
DEFAULT_CREATE_MAIN = False

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
    create_module_file(module_dir, '__init__.py')
    create_module_file(module_dir, '{}.py')
    if create_main:
        create_module_file(module_dir, '__main__.py')


def create_module_file(module_dir, filename_format):
    module_filepath = str(module_dir / filename_format.format(name_lower))
    template_filepath = ASSETS_DIRECTORY / filename_format.format('template')
    with open(module_filepath, 'w') as file:
        content = generate_template_content(template_filepath)
        file.write(content)


def generate_template_content(filepath):
    content = filepath.read_text().replace('template', name_lower)
    return content


def convert_lower_to_pascal(name):
    return name.title().replace('_', '')


def assert_name_is_lower(name):
    lowercase_pattern = r'^[a-z]+(_[a-z]+)*$'  # pattern matching lowercase_with_underscores
    if not re.match(lowercase_pattern, name):
        raise RuntimeError(f'Module name "{name}" does not follow lowercase_with_underscores')


def assert_creation_dir_exists(creation_dir):
    if not os.path.exists(creation_dir):
        raise RuntimeError(f'Creation directory "{creation_dir}" does not exist')


def assert_no_module_dir_exists(module_dir):
    if os.path.exists(module_dir):
        raise RuntimeError(f'Module directory "{module_dir}" already exists')
