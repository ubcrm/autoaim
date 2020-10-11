from modules.frame_to_roi.frame_to_roi import frame_to_roi
from modules.roi_to_mask.roi_to_mask import roi_to_mask
from modules.mask_to_leds.mask_to_leds import mask_to_leds
from modules.leds_to_panels.leds_to_panels import leds_to_panels
from modules.panels_to_target.panels_to_target import panels_to_target
from modules.target_to_coords.target_to_coords import target_to_coords
from modules.predict_coords.predict_coords import predict_coords
from modules.send_coords.send_coords import send_coords
from autoaim_config import *
import cv2
import numpy as np


def autoaim(source, do_debug=DEFAULT_DO_DEBUG):
    debug = Debug() if do_debug else None
    capture = cv2.VideoCapture(source)
    successful, image = capture.read()
    frame = Frame(image, 1)

    if not successful:
        raise RuntimeError(CAPTURE_ERROR.format(source))

    target = None
    while successful:
        if do_debug:
            debug.new_frame(Frame(image, frame.count))

        roi = frame_to_roi(frame, target, debug)
        mask = roi_to_mask(roi, debug)
        leds = mask_to_leds(mask, debug)
        panels = leds_to_panels(leds, debug)
        target = panels_to_target(panels, debug)
        coords = target_to_coords(target, debug)
        aim_coords = predict_coords(coords, debug)
        send_coords(aim_coords, debug)

        if do_debug:
            debug.show()
        successful, image = capture.read()
        frame = Frame(image, frame.count + 1)


class Debug:
    def __init__(self):
        self.frame = None
        self.logs = None

    def new_frame(self, frame):
        self.frame = frame
        self.logs = []

    def show(self):
        cv2.imshow(WIN_TITLE, self.frame.image)
        cv2.waitKey(FRAME_DELAY)

    def print(self):
        print(LOG_FRAME_FORMAT.format(self.frame.count))
        print('\n'.join(self.logs))


class Frame:
    def __init__(self, image, count):
        self.image = image
        self.original_dims = image.shape[1:: -1]
        self.dims = self.original_dims
        self.topleft = [0, 0]
        self.scale_factor = 1
        self.count = count

    def crop(self, start, end):
        '''
        :param start: (x, y) of the top left crop point, inclusive
        :param end: (x, y) of the bottom right crop point, inclusive
        '''
        start = self._clip(start, self.dims)
        end = self._clip(end, self.dims) + 1
        self.image = self.image[start[1]: end[1], start[0]: end[0]]
        self.dims = end - start
        self.topleft = start

    def center_crop(self, center, width, height=None):
        '''
        :param center: (x, y) of point to crop around
        :param width: width of crop window
        :param height: height of crop window, default is width
        '''
        height = width if height is None else height
        center = np.array(center)
        delta = np.array([width // 2, height // 2])
        self.crop(center - delta, center + delta)

    def scale(self, factor):
        '''
        :param factor: integer factor to scale down by, factor=4 scales down by 4
        '''
        self.dims //= factor
        self.scale_factor = factor
        self.image = cv2.resize(self.image, tuple(self.dims))

    def to_original(self, point):
        point = np.array(point)
        original = self._clip(point * self.scale_factor + self.topleft, self.original_dims)
        return original

    def to_current(self, point):
        point = np.array(point)
        current = self._clip(point * self.scale_factor + self.topleft, self.dims)
        return current

    @staticmethod
    def _clip(point, dims):
        point = np.array([
            np.clip(point[0], 0, dims[0] - 1),
            np.clip(point[1], 0, dims[1] - 1)])
        return point
