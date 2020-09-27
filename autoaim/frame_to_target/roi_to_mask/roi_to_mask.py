import roi_to_mask_config as CONFIG
import cv2
import numpy as np


def roi_to_mask(roi, debug_frame=None):
    height = roi.shape[0]
    dilate_dim = round(CONFIG.DILATE_REL * height)
    morph_dims = (round(CONFIG.MORPH_REL[0] * height), round(CONFIG.MORPH_REL[1] * height))

    mask = cv2.inRange(roi, *CONFIG.RANGE)
    mask = cv2.dilate(mask, np.ones((dilate_dim, dilate_dim)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_dims)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    '''
    if debug_frame is not None:
        masked_frame = cv2.bitwise_and(roi, roi, mask=mask)
        debug_frame[:] = cv2.addWeighted(masked_frame, CONFIG.DEBUG_MASK_WEIGHT, roi, 1 - CONFIG.DEBUG_MASK_WEIGHT, 0)
    '''
    return mask
