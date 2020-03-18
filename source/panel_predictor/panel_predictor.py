from source.module import Module
from pathlib import Path
import os
from .panel_finder.panel_finder import PanelFinder
import time


class PanelPredictor(Module):
    def __init__(self, parent=None, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        self.panel = None
        self.panel_finder = PanelFinder(self, state=state)  # this panel finder needs no additional properties
        self.past_targets = []

    def process(self, frame):
        """
        predicts where the center of the panel will be
        :param frame: an image that may contain a robot
        :return: ((x,y), confidence)  coordinates of panel and confidence it will be there
        
        panel = self.panel_finder.process(frame)
        if panel is not None:
            panel, confidence = panel
            if len(self.past_targets) == self.properties["reference_frames"]:
                self.past_targets.pop(0)
            self.past_targets.append((panel["x_center"], panel["y_center"], time.time(), confidence))
        if len(self.past_targets) == self.properties["reference_frames"]:
            if self.properties["prediction_type"] == "linear":
                return self.linear_prediction(frame)
        """
        return self.panel_finder.process(frame)

    def linear_prediction(self, frame):
        frame_size = ((frame.shape[0]) ** 2 + (frame.shape[1]) ** 2) ** (1 / 2)
        distance = 1 / max(1e-3, frame.shape[1] / self.properties["distance_1m_height_rel"] / 1080)
        velocity, distance_confidence = self.average_velocity(frame_size)
        foresight_time = time.time() - self.past_targets[-1][2] + self.properties["seconds_ahead"]
        target = (round(self.past_targets[-1][0] + velocity[0] * foresight_time),
                      round(self.past_targets[-1][1] + velocity[1] * foresight_time))
        foresight_confidence = (1 / (foresight_time * self.properties["time_confidence_falloff"] + 1))
        cumulative_confidence = distance_confidence * foresight_confidence
        return target, distance, cumulative_confidence

    def average_velocity(self, max_distance):
        avg_velocity = [0, 0]
        error = 1
        data_points = (len(self.past_targets) - 1)
        for i in range(len(self.past_targets) - 1):
            pointA = self.past_targets[i]
            pointB = self.past_targets[i + 1]
            deltaX = pointB[0] - pointA[0]
            deltaY = pointB[1] - pointA[1]
            deltaT = pointB[2] - pointA[2]
            distance = (deltaX ** 2 + deltaY ** 2) ** (1 / 2) / max_distance
            avg_velocity[0] += deltaX / deltaT / data_points
            avg_velocity[1] += deltaY / deltaT / data_points
            distance_error = distance ** 2 / data_points * self.properties["distance_confidence_falloff"]
            confidence = 1 / ((pointA[3] + pointB[3]) / 2)
            error += distance_error * confidence ** self.properties["model_confidence_weight"]
        return avg_velocity, 1 / error
