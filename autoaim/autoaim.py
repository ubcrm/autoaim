from modules.frame_to_roi import frame_to_roi
from modules.roi_to_mask import roi_to_mask
from modules.mask_to_leds import mask_to_leds
from modules.leds_to_panels import leds_to_panels
from modules.panels_to_target import panels_to_target
from modules.target_to_coords import target_to_coords
from modules.predict_coords import predict_coords
from modules.send_coords import send_coords
import cv2
import numpy as np
import json
import time

FRAME_SCALE = 2
DEBUG_SCALE = 2
MODE_RUN, MODE_DEBUG, MODE_TEST = 0, 1, 2
FRAME_DELAY = 0  # (ms)


def autoaim(source, mode=MODE_DEBUG, data_file=None):
    com = Common()
    com.debug = (mode == MODE_DEBUG)
    com.test = (mode == MODE_TEST)

    if com.test:
        if data_file is None:
            raise RuntimeError('Provide data file to test against.')
        if type(source) is int:
            raise RuntimeError('Provide video source containing test footage.')
        print('Testing implementation...')
        coords_data = []
        failed_count = 0
        start_time = time.time()

    capture = cv2.VideoCapture(source)
    successful, frame = capture.read()
    if not successful:
        raise RuntimeError(f'Failed to read from video source "{source}".')
    com.frame_count = 1
    com.top_left = np.array([0, 0])
    com.orig_dims = np.array([capture.get(3), capture.get(4)]).astype(int)
    frame_dims = tuple(np.round(com.orig_dims / FRAME_SCALE).astype(int))
    debug_dims = tuple(np.round(com.orig_dims / DEBUG_SCALE).astype(int))
    target = None

    while True:
        successful, frame = capture.read()
        if not successful:
            break
        com.frame_count += 1
        frame = cv2.resize(frame, frame_dims)
        if com.debug:
            com.debug_frame = cv2.resize(frame, debug_dims)
            print(f'\n----- Frame {com.frame_count} -----')

        roi = frame_to_roi(frame, target, com)
        mask = roi_to_mask(roi, com)
        leds = mask_to_leds(mask, com)
        panels = leds_to_panels(leds, com)
        target = panels_to_target(panels, com)
        coords = target_to_coords(target, com)
        aim_coords = predict_coords(coords, com)
        send_coords(aim_coords, com)

        if com.debug:
            cv2.imshow('Debug Output', com.debug_frame)
            if cv2.waitKey(FRAME_DELAY) == ord('q'):
                break
        elif com.test:
            if coords is None:
                failed_count += 1
            else:
                coords_data.append(coords)

    if com.test:
        end_time = time.time()
        print(f'Time per frame: {(end_time - start_time) / com.frame_count * 1E3:.1f} ms')
        print('Deviations in (rho, phi, z): {:.2f}, {:.2f}, {:.2f}'.format(*calc_deviations(coords_data, data_file)))
        print(f'Failed detection ratio: {failed_count / com.frame_count:.2f}')
    cv2.destroyAllWindows()


def calc_deviations(data, data_file):
    with open(data_file, 'r') as file:
        absolute = json.load(file)
        absolute = list(absolute.values())[1:]  # skip first frame

    measured = np.array(data)
    deviations = np.divide(np.subtract(absolute, measured), absolute) ** 2
    deviations = np.sqrt(np.average(deviations, axis=0))
    return deviations


class Common:
    def __init__(self):
        self.debug, self.test = None, None
        self.frame_count = None
        self.debug_frame = None
        self.top_left = None
        self.orig_dims = None
        self.frame_scale = FRAME_SCALE

    def orig_to_frame(self, point):
        return np.round(np.array(point) / FRAME_SCALE).astype(int)

    def orig_to_debug(self, point):
        return np.round(np.array(point) / DEBUG_SCALE).astype(int)

    def frame_to_orig(self, point):
        return (self.top_left + point) * FRAME_SCALE
