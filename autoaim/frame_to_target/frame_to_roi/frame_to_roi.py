import frame_to_roi_config as CONFIG
import cv2


def frame_to_roi(frame, debug_frame=None):
    height, width = frame.shape[:2]
    crop_dims = (round(height * CONFIG.SCALE), round(width * CONFIG.SCALE))

    frame = cv2.resize(frame, crop_dims)
    if debug_frame is not None:
        debug_frame[:] = cv2.resize(debug_frame, crop_dims)
    return frame

