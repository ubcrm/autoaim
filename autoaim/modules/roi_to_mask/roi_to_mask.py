from autoaim_config import DO_DEBUG
from roi_to_mask_config import *
import cv2
import numpy as np


def roi_to_mask(capture):
    scaled_height = capture.original_dims[1] // capture.scale_factor
    dilate_dim = round(DILATE_REL * scaled_height)
    morph_dims = (round(MORPH_REL[0] * scaled_height), round(MORPH_REL[1] * scaled_height))

    mask = cv2.inRange(capture.frame, *RANGE)
    mask = cv2.dilate(mask, np.ones((dilate_dim, dilate_dim)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_dims)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    capture.frame = mask

    if DO_DEBUG:
        debug_mask = capture.frame_to_debug(pad_value=0)
        masked = cv2.bitwise_and(capture.debug_frame, capture.debug_frame, mask=debug_mask)
        capture.debug_frame = cv2.addWeighted(masked, DEBUG_MASK, capture.debug_frame, 1 - DEBUG_MASK, 0)
    return capture
