import os
from pathlib import Path

from source.common.module import Module
from .data_labeler import DataLabeler
from .label_editor import LabelEditor

"""
in: vala's labels (json file)
out: json file 
"""


class Data(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.label_editor = LabelEditor(self.properties)
        self.data_labeler = DataLabeler(self.properties)
        self.process(self.properties["data_json"])

    def process(self, json):
        edited = self.label_editor.process(json)
        return self.data_labeler.process(edited)
