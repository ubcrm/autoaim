from source.common.module import Module
from pathlib import Path
import os
from source.panel_predictor.panel_finder.panel_finder import PanelFinder
import time


class PanelPredictor(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.panel = None
        self.panel_finder = PanelFinder(state=state)  # this panel finder needs no additional properties
        self.past_targets = []

    def process(self, frame):
        panel = self.panel_finder.process(frame)
        if panel is not None:
            if len(self.past_targets) == self.properties["reference_frames"]:
                self.past_targets.pop(0)
            self.past_targets.append((panel["x_center"], panel["y_center"], time.time()))
        if len(self.past_targets) == self.properties["reference_frames"]:
            if self.properties["prediction_type"] == "linear":
                velocity = self.average_velocity()
                foresight_time = time.time() - self.past_targets[-1][2] + self.properties["seconds_ahead"]
                prediction = (round(self.past_targets[-1][0] + velocity[0] * foresight_time), round(self.past_targets[-1][1] + velocity[1] * foresight_time))
                return prediction

    def average_velocity(self):
        avg_velocity = [0, 0]
        for i in range(len(self.past_targets) - 1):
            pointA = self.past_targets[i]
            pointB = self.past_targets[i + 1]
            deltaX = pointB[0] - pointA[0]
            deltaY = pointB[1] - pointA[1]
            deltaT = pointB[2] - pointA[2]
            avg_velocity[0] += deltaX / deltaT / (len(self.past_targets) - 1)
            avg_velocity[1] += deltaY / deltaT / (len(self.past_targets) - 1)
        return avg_velocity
