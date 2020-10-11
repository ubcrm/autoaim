from roi_to_mask_config import *
import cv2
import numpy as np


def roi_to_mask(roi_frame, debug=None):
    height = roi_frame.original_dims[1] * roi_frame.scale_factor
    dilate_dim = round(DILATE_REL * height)
    morph_dims = (round(MORPH_REL[0] * height), round(MORPH_REL[1] * height))

    mask = cv2.inRange(roi_frame.image, *RANGE)
    mask = cv2.dilate(mask, np.ones((dilate_dim, dilate_dim)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_dims)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    roi_frame.image = mask

    '''
    if debug is not None:
        unmasked = debug.frame.image
        mask = debug.frame.to_current_image(roi_frame.to_original_image(pad_value=255))
        masked = cv2.bitwise_and(unmasked, unmasked, mask=mask)
        debug.frame.image = cv2.addWeighted(masked, DEBUG_MASK_WEIGHT, unmasked, 1 - DEBUG_MASK_WEIGHT, 0)
    '''
    return roi_frame
