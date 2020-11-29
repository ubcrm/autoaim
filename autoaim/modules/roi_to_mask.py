import cv2
import numpy as np

RANGE = ((0, 0, 253), (180, 255, 255))
DILATE_REL = 0.003  # fractional height
MORPH_REL = (0.004, 0.01)  # fractional height
DEBUG_MASK_WEIGHT = 0.5


def roi_to_mask(roi, com):
    mask = cv2.inRange(cv2.cvtColor(roi, cv2.COLOR_BGR2HSV), *RANGE)
    dilate_dim = np.ceil(DILATE_REL * com.orig_dims[1]).astype(int)
    mask = cv2.dilate(mask, np.ones((dilate_dim, dilate_dim)))

    morph_dims = tuple(np.ceil(np.array(MORPH_REL) * com.orig_dims[1]).astype(int))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_dims)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    if com.debug:
        start = com.orig_to_debug(com.frame_to_orig([0, 0]))
        end = com.orig_to_debug(com.frame_to_orig(mask.shape[1::-1]))

        debug_mask = np.full(com.debug_frame.shape[:2], 0, dtype=np.uint8)
        debug_mask[start[1]: end[1], start[0]: end[0]] = cv2.resize(mask, tuple(end - start))
        masked = cv2.bitwise_and(com.debug_frame, com.debug_frame, mask=debug_mask)
        com.debug_frame = cv2.addWeighted(masked, DEBUG_MASK_WEIGHT, com.debug_frame, 1 - DEBUG_MASK_WEIGHT, 0)
    return mask
