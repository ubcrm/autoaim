from source.common.module import Module
from source.rune.assign_panels.assign_panels import AssignPanels
from pathlib import Path
import os


class PredictTarget(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)
        self.assign_panels = AssignPanels(state)
        self.angles = None

    def process(self, image):
        if self.angles is None:
            self.angles = self.assign_panels.process(image, state=False)
            return None
        else:
            angles = self.assign_panels.process(image, state=True)
            speed = self.calculate_rotational_velocity(self.angles, angles)

    @staticmethod
    def calculate_rotational_velocity(angles1, angles2):
        pass
