from autoaim_config import DO_DEBUG
from frame_to_roi_config import *
import cv2


def frame_to_roi(capture, target):
    capture.scale_down(SCALE_FRAME)

    if (target is not None) and (capture.frame_count % ROI_PERIOD != 0):
        width = CROP.MARGIN_LARGE  # * target.distance
        height = CROP.MARGIN_SMALL  # * target.distance
        capture.center_crop(target, width, height)

    if DO_DEBUG:
        cv2.rectangle(capture.debug_frame,
                      tuple(capture.point_to_debug([0, 0])),
                      tuple(capture.point_to_debug(capture.dims)),
                      DEBUG.COLOUR, DEBUG.THICKNESS)
    return capture
