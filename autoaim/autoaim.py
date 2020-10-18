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


def autoaim():
    capture = Capture()
    target = None

    while capture.next_frame():
        if DO_DEBUG:
            print(LEG_FRAME.format(capture.frame_count))

        roi = frame_to_roi(capture, target)
        mask = roi_to_mask(roi)
        leds = mask_to_leds(mask)
        panels = leds_to_panels(leds, capture)
        target = panels_to_target(panels, capture)
        coords = target_to_coords(target, capture)
        aim_coords = predict_coords(coords, capture)
        send_coords(aim_coords, capture)

        if DO_DEBUG:
            cv2.imshow(DEBUG_WIN_TITLE, capture.debug_frame)
            cv2.waitKey(FRAME_DELAY)


class Capture:
    def __init__(self):
        self.capture = cv2.VideoCapture(SOURCE)
        self.frame = None
        self.debug_frame = None
        self.original_dims = None
        self.dims = None
        self.top_left = None
        self.scale_factor = None
        self.frame_count = -1

        if not self.next_frame():
            raise RuntimeError(CAPTURE_ERROR.format(SOURCE))
        self.original_dims = np.array(self.frame.shape[1:: -1])

    def next_frame(self):
        successful, frame = self.capture.read()
        if not successful:
            return False

        self.frame = frame
        self.dims = np.array(frame.shape[1:: -1])
        self.top_left = np.array([0, 0])
        self.scale_factor = 1
        self.frame_count += 1
        if DO_DEBUG:
            self.debug_frame = cv2.resize(frame, tuple(self.dims // DEBUG_SCALE))
        return True

    def crop(self, start, end):
        '''
        :param start: (x, y) of the top left crop point, inclusive
        :param end: (x, y) of the bottom right crop point, exclusive
        '''
        start = self._clip(start, self.dims)
        end = self._clip(end, self.dims)
        self.frame = self.frame[start[1]: end[1], start[0]: end[0]]
        self.dims = end - start
        self.top_left = start

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

    def scale_down(self, factor):
        '''
        :param factor: integer factor to scale down by (preferably divides frame dims)
        '''
        self.dims //= factor
        self.top_left //= factor
        self.scale_factor *= factor
        self.frame = cv2.resize(self.frame, tuple(self.dims))

    def point_to_debug(self, point):
        '''
        Obtain the original pixel coordinates of a point in current image.
        '''
        point = np.array(point)
        debug_point = self._clip(
            (point + self.top_left) * self.scale_factor // DEBUG_SCALE,
            self.original_dims // DEBUG_SCALE)
        return debug_point

    def frame_to_debug(self, pad_value=0):
        '''
        Obtain the original version of the current image.
        :param pad_value: value to use on the cropped regions of original image.
        '''
        dims = self.dims * self.scale_factor // DEBUG_SCALE
        debug_dims = self.original_dims[1:: -1] // DEBUG_SCALE
        if len(self.frame.shape) == 3:  # color image
            debug_dims += [self.frame.shape[2]]
        start = self.top_left * self.scale_factor // DEBUG_SCALE
        end = (self.top_left + self.dims) * self.scale_factor // DEBUG_SCALE

        debug_frame = np.full(debug_dims, pad_value, dtype=np.uint8)
        debug_frame[start[1]: end[1], start[0]: end[0]] = cv2.resize(self.frame, tuple(dims))
        return debug_frame

    @staticmethod
    def _clip(point, dims):
        point = np.array([
            np.clip(point[0], 0, dims[0]),
            np.clip(point[1], 0, dims[1])])
        return point
