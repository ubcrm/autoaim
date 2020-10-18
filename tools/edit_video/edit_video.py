from edit_video_config import *
import cv2
import numpy as np


class EditVideo:
    def __init__(self, filename):
        self.filename = filename
        self.capture = cv2.VideoCapture(str(ASSETS_DIR / self.filename))
        self.dims = np.array([self.capture.get(3), self.capture.get(4)], dtype=np.uint)  # width, height
        self.fps = int(self.capture.get(5))
        self.edit_funcs = []

    def crop(self, start, end):
        start = self._clip(start, self.dims)
        end = self._clip(end, self.dims)

        def crop_func(frame):
            return frame[start[1]: end[1], start[0]: end[0]]
        self.dims[:] = [end[0] - start[0], end[1] - start[1]]
        self.edit_funcs.append(crop_func)
        return self

    def vertical_crop(self, start, end):
        return self.crop([0, start], [self.dims[0], end])

    def horizontal_crop(self, start, end):
        return self.crop([start, 0], [end, self.dims[1]])

    def rotate_ccw(self, count=1):
        def rotate_func(frame):
            return np.rot90(frame, k=count)
        self.dims[:] = self.dims[::-1]
        self.edit_funcs.append(rotate_func)
        return self

    def export(self, path=None):
        if path is None:
            path = str(EXPORT_DIR / self.filename)
        video_writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, tuple(self.dims))

        successful, frame = self.capture.read()
        while successful:
            for edit_func in self.edit_funcs:
                frame = edit_func(frame)
            video_writer.write(frame)
            successful, frame = self.capture.read()

    @staticmethod
    def _clip(point, dims):
        point = np.array([
            np.clip(point[0], 0, dims[0]),
            np.clip(point[1], 0, dims[1])])
        return point
