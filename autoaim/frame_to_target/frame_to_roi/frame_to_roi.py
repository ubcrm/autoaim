import frame_to_roi_config as CONFIG
import cv2


def frame_to_roi(roi, debug_frame=None):
    height, width = roi.shape[:2]
    resize_dims = (round(height * CONFIG.SCALE), round(width * CONFIG.SCALE))

    roi = cv2.resize(roi, resize_dims)
    if debug_frame is not None:
        debug_frame[:] = cv2.resize(debug_frame, resize_dims)
    return roi

