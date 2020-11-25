import cv2
import numpy as np

ROI_PERIOD = 10
CROP_DIMS_REL = (1.5, 0.5)
COLOR = (0, 255, 0)
THICKNESS = 1


def frame_to_roi(frame, target, com):
    if (target is None) or (com.frame_count % ROI_PERIOD == 0):
        com.top_left[:] = [0, 0]
        return frame

    crop_dims = np.array(CROP_DIMS_REL) * com.orig_dims[1] / target.distance

    start_orig = clip(target.center - crop_dims // 2, com.orig_dims)
    end_orig = clip(target.center + crop_dims // 2, com.orig_dims)
    start, end = com.orig_to_frame(start_orig), com.orig_to_frame(end_orig)
    roi = frame[start[1]: end[1], start[0]: end[0]]
    com.top_left = start

    if com.debug:
        cv2.rectangle(com.debug_frame, tuple(com.orig_to_debug(start_orig)),
                      tuple(com.orig_to_debug(end_orig)), COLOR, THICKNESS)
    return roi


def clip(point, dims):
    x = np.clip(point[0], 0, dims[0])
    y = np.clip(point[1], 0, dims[1])
    return np.array([x, y])
