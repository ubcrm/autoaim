from modules.frame_to_roi.frame_to_roi import frame_to_roi
from modules.roi_to_mask.roi_to_mask import roi_to_mask
from modules.mask_to_leds.mask_to_leds import mask_to_leds
from modules.leds_to_panels.leds_to_panels import leds_to_panels
from modules.panels_to_target.panels_to_target import panels_to_target
from modules.target_to_coords.target_to_coords import target_to_coords
from modules.predict_coords.predict_coords import predict_coords
from modules.send_coords.send_coords import send_coords
from autoaim_config import *
import cv2


def autoaim(source, debug=DEFAULT_DEBUG):
    frame_count = 0
    capture = cv2.VideoCapture(source)

    successful, frame = capture.read()
    if not successful:
        raise RuntimeError(CAPTURE_ERROR.format(source))

    panels = []

    while successful:
        frame_count += 1
        debug_frame = frame.copy() if debug else None

        roi = frame_to_roi(frame, panels, debug_frame)
        mask = roi_to_mask(roi, debug_frame)
        leds = mask_to_leds(mask, debug_frame)
        panels = leds_to_panels(leds, debug_frame)
        target = panels_to_target(panels, debug_frame)
        coords = target_to_coords(target)
        aim_coords = predict_coords(coords)
        send_coords(aim_coords)

        if debug:
            cv2.imshow(WIN_TITLE, debug_frame)
            cv2.waitKey(FRAME_DELAY)

        successful, frame = capture.read()
