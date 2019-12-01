import os
from pathlib import Path

from source.common.module import Module


class PreprocessRune(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)

    def process(self, frame, rune_center):
        """
        :param frame: power rune image to be cropped
        :param rune_center: center coordinate of power rune in the frame
        :return: tuple of cropped image, amount to shift frame left, top by
        """
        frame = frame.copy()
        dims = frame.shape[:2]
        radius = self.properties["scaling"] * dims[0] / 2
        top = round(rune_center[1] * dims[0] - radius)
        bottom = round(rune_center[1] * dims[0] + radius)
        left = round(rune_center[0] * dims[1] - radius)
        right = round(rune_center[0] * dims[1] + radius)
        crop_img = frame[top:bottom, left:right]
        return crop_img, left, top
