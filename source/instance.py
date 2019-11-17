from pathlib import Path
import os
import json


def get_json_from_file(filename):
    return json.loads(Path(filename).read_text())


def get_json_from_path(path):
    return json.loads(path.read_text())


class Instance:
    state = {
        "root_dir": Path(os.path.dirname(os.path.abspath(__file__))).parent  # project root
    }
