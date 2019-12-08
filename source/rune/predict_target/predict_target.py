import os
from pathlib import Path
import time
import numpy as np

from source.module import Module
from source.rune.predict_target.assign_panels.assign_panels import AssignPanels


class PredictTarget(Module):
    def __init__(self, parent, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        self.assign_panels = AssignPanels({"mode": "not debug"})
        self.frames_calculated = 0
        self.angles = []

    def process(self, image):
        """
        Saves the target panels for consecutive frames
        After collecting several frames it predicts where the target will be
        :param image: an image cropped around the power rune
        :return: None or (x,y)
        """
        angles, t = self.assign_panels.process(image), time.time()
        if angles:
            angle = self.get_activating_angle(angles)
            if angle is None:
                self.frames_calculated = 0
                self.angles = []
                return None
            self.angles.append((angle, t))
            self.frames_calculated += 1
        if self.frames_calculated >= self.properties["tracking_frames"]:
            speed = self.calculate_rotational_velocity(self.angles)
            target_arm = self.angles[-1][0]
            target_angle = np.radians(target_arm + speed * self.properties["seconds_ahead"])
            target_point = (
                image.shape[0] * self.properties["arm_length"] * np.sin(target_angle) + image.shape[0] / 2,
                image.shape[0] * self.properties["arm_length"] * -np.cos(target_angle) + image.shape[1] / 2)
            self.frames_calculated = 0
            self.angles = []
            return target_point
        else:
            return None

    @staticmethod
    def calculate_rotational_velocity(angles_list):
        if len(angles_list) <= 1:
            return 0
        avg_speed = 0
        for i in range(len(angles_list) - 1):
            delta_angle = angles_list[i + 1][0] - angles_list[i][0]
            delta_time = angles_list[i + 1][1] - angles_list[i][1]
            if delta_angle < 0:
                delta_angle += 365
            avg_speed += delta_angle / delta_time
        return avg_speed / (len(angles_list) - 1)

    def get_activating_angle(self, targets):
        for angle, value in targets.items():
            if value == self.properties["panel_states"]["activating"]:
                if angle is None:
                    print(targets)
                return angle
