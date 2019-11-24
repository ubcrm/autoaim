import os
from pathlib import Path

import numpy as np

from source.common.module import Module
from source.rune.predict_target.assign_panels.assign_panels import AssignPanels


class PredictTarget(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.assign_panels = AssignPanels(state)
        self.frames_calculated = 0
        self.angles = []

    def process(self, image):
        if self.frames_calculated + 1 < self.properties["tracking_frames"]:
            self.angles.append(self.assign_panels.process(image, state=False))
            self.frames_calculated += 1
            return None
        else:
            self.angles.append(self.assign_panels.process(image, state=True))
            speed = self.calculate_rotational_velocity(self.angles)
            target_arm = None
            for angle, value in self.angles[-1].items():
                if value == self.properties["panel_states"]["activating"]:
                    target_arm = angle
            target_angle = target_arm + speed * self.properties["frames_ahead"]
            target_point = (image.shape[0] * self.properties["arm_length"] * np.cos(target_angle) + image.shape[0] / 2,
                            image.shape[0] * self.properties["arm_length"] * -np.sin(target_angle) + image.shape[1] / 2)
            self.frames_calculated = 0
            return target_point

    @staticmethod
    def calculate_rotational_velocity(angles_list):
        if len(angles_list) == 1:
            return 0
        avg_speed = 0
        for i in range(len(angles_list) - 1):
            angles1 = angles_list[i].keys()
            angles2 = angles_list[i + 1].keys()
            avg_speed += (sum(np.subtract(angles1, angles2))) / len(angles1)
        return avg_speed / (len(angles_list) - 1)
