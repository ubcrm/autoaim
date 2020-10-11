from frame_to_roi_config import *
import cv2


def frame_to_roi(frame, target, debug=None):
    frame.scale(SCALE)
    width, height = frame.dims

    # TODO - make crop outline in the debug frame more visible after masking

    # (x, y)
    top_left = [0, 0]
    bottom_right = [width, height]
    if target is not None and (frame.count + 1) % ROI_PERIOD != 1:
        margin_x = CROP.MARGIN_LARGE  # * target.distance
        margin_y = CROP.MARGIN_LARGE  # * target.distance

        frame.center_crop(target, margin_x, margin_y)

    if debug is not None:
        debug.frame.scale(SCALE)
        #debug.frame.image[:] = frame
        a = tuple(frame.to_original([0, 0]))
        b = tuple(frame.to_original(frame.dims))
        print(a)
        print(b)
        cv2.rectangle(debug.frame.image, tuple(frame.to_original([0, 0])), tuple(frame.to_original(frame.dims)),
                      (0,255,0), DEBUG.THICKNESS)

    return frame
