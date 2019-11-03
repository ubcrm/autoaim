from source.common.instance import get_json_from_file
from .data_labeler import DataLabeler
from .label_editor import LabelEditor
from pathlib import Path
import os

"""
in: vala's labels (json file)
out: json file 
"""


class Data:
    def __init__(self, state=None):
        if state is None:
            state = {}
        settings_path = os.path.dirname(os.path.abspath(__file__))
        self.properties = get_json_from_file(Path(settings_path) / "settings.json")
        self.properties.update(state)  # merges static settings and dynamically passed state. States override settings.
        self.label_editor = LabelEditor(self.properties)
        self.data_labeler = DataLabeler(self.properties)
        self.process(self.properties["data_json"])

    def process(self, json):
        edited = self.label_editor.process(json)
        return self.data_labeler.process(edited)
