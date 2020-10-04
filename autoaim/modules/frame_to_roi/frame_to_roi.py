from frame_to_roi_config import *
import cv2


def frame_to_roi(frame, target, debugger=None):
    height, width, _ = frame.shape
    resize_dims = (round(width * SCALE), round(height * SCALE))
    frame = cv2.resize(frame, resize_dims)
    height, width, _ = frame.shape

    # TODO - make crop outline in the debug frame more visible after masking

    roi = frame.copy()

    # (x, y)
    top_left = [0, 0]
    bottom_right = [width, height]
    if target is not None:
        margin = CROP.MARGIN_LARGE  # * target.distance
        top_left = [max(target[0] - margin, 0), max(target[1] - margin, 0)]
        bottom_right = [min(target[0] + margin, width), min(target[1] + margin, height)]

        roi = roi[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # TODO - update crop frame object

    if debugger is not None:
        debugger.frame.resize(frame.shape, refcheck=False)
        debugger.frame[:] = frame
        cv2.rectangle(debugger.frame, tuple(top_left), tuple(bottom_right), DEBUG.COLOUR, DEBUG.THICKNESS)

    return roi
