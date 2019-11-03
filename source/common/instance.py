from pathlib import Path
import json


class Instance:
    def __init__(self):
        self.property = None  # placeholder instance variable


def get_json_from_file(filename):
    return json.loads(Path(filename).read_text())
