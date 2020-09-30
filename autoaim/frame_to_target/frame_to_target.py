from frame_to_target_config import *
from frame_to_roi import frame_to_roi
from roi_to_mask import roi_to_mask
from mask_to_target.mask_to_target import mask_to_target
import cv2


feedback_panels = []


def frame_to_target(frame, debug=DEFAULT_DEBUG):
    global feedback_panels
    debug_frame = frame.copy() if debug else None
    roi = frame_to_roi(frame, feedback_panels, debug_frame=debug_frame)
    mask = roi_to_mask(roi, debug_frame=debug_frame)
    target, feedback_panels = mask_to_target(mask, debug_frame=debug_frame)

    if debug:
        cv2.imshow(WIN_TITLE, debug_frame)
        cv2.waitKey(FRAME_DELAY)
    return target
