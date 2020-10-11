from roi_to_mask_config import *
import cv2
import numpy as np


def roi_to_mask(roi, debug=None):
    height = roi.shape[0]
    dilate_dim = round(DILATE_REL * height)
    morph_dims = (round(MORPH_REL[0] * height), round(MORPH_REL[1] * height))

    mask = cv2.inRange(roi, *RANGE)
    mask = cv2.dilate(mask, np.ones((dilate_dim, dilate_dim)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_dims)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    '''
    if debugger is not None:
        masked_frame = cv2.bitwise_and(roi, roi, mask=mask)
        debugger.frame[:] = cv2.addWeighted(masked_frame, DEBUG_MASK_WEIGHT, roi, 1 - DEBUG_MASK_WEIGHT, 0)
    '''
    return mask
