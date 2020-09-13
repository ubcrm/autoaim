import frame_to_roi_config as CONFIG
import cv2


def frame_to_roi(roi, debug_frame=None):
    height, width, _ = roi.shape
    resize_dims = (round(width * CONFIG.SCALE), round(height * CONFIG.SCALE))
    roi = cv2.resize(roi, resize_dims)

    if debug_frame is not None:
        debug_frame.resize(roi.shape, refcheck=False)
        debug_frame[:] = roi
    return roi

