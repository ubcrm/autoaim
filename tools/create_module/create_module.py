import create_module_config as CONFIG
from pathlib import Path
import os
import re


class CreateModule:
    def __init__(self, name_lower, dir_create):
        self.name_lower = name_lower
        self.name_pascal = _convert_lower_to_pascal(name_lower)
        self.dir_create = dir_create
        self.dir_module = Path(dir_create) / name_lower

        self._assert_name_is_lower()
        self._assert_dir_create_exists()
        self._assert_no_dir_module_exists()

    def run(self, create_main=False):
        os.mkdir(self.dir_module)
        os.mkdir(self.dir_module / f'{self.name_lower}_assets')

        self._create_module_file(CONFIG.BASE_FILENAME)
        self._create_module_file(CONFIG.CONFIG_FILENAME)
        if create_main:
            self._create_module_file(CONFIG.MAIN_FILENAME)

    def _create_module_file(self, filename_format):
        module_filepath = str(self.dir_module / filename_format.format(self.name_lower))
        template_filepath = CONFIG.ASSETS_DIRECTORY / filename_format.format(CONFIG.TEMPLATE_LOWER)
        with open(module_filepath, 'w') as file:
            content = self._generate_template_content(template_filepath)
            file.write(content)

    def _generate_template_content(self, filepath):
        content = filepath.read_text().replace(CONFIG.TEMPLATE_LOWER, self.name_lower) \
            .replace(CONFIG.TEMPLATE_PASCAL, self.name_pascal)
        return content

    def _assert_name_is_lower(self):
        lowercase_pattern = r'^[a-z]+(_[a-z]+)*$'  # pattern matching lowercase_with_underscores
        if not re.match(lowercase_pattern, self.name_lower):
            raise RuntimeError(CONFIG.NAME_NOT_LOWERCASE_ERROR.format(self.name_lower))

    def _assert_dir_create_exists(self):
        if not os.path.exists(self.dir_create):
            raise RuntimeError(CONFIG.NO_CREATE_DIR_EXISTS_ERROR.format(self.dir_create))

    def _assert_no_dir_module_exists(self):
        if os.path.exists(self.dir_module):
            raise RuntimeError(CONFIG.MODULE_DIR_EXISTS_ERROR.format(self.dir_module))


def _convert_lower_to_pascal(string):
    return string.title().replace('_', '')
