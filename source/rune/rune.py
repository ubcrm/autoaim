import os
from pathlib import Path
from source.common.module import Module
from source.rune.predict_target.predict_target import PredictTarget
from source.rune.preprocess.preprocess import Preprocess


class Rune(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.preprocess = Preprocess()
        self.predict_target = PredictTarget()
        self.rune_center = self.properties["rune_center"]

    def process(self, frame):
        cropped, left, top = self.preprocess.process(frame, self.rune_center)
        prediction = self.predict_target.process(cropped)
        if prediction is not None:
            return [prediction[0] + left, prediction[1] + top]