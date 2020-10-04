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


def autoaim(source, do_debug=DEFAULT_DO_DEBUG):
    debugger = Debugger() if do_debug else None
    capture = cv2.VideoCapture(source)
    successful, frame = capture.read()

    if not successful:
        raise RuntimeError(CAPTURE_ERROR.format(source))

    target = None
    target_count = 0
    while successful:
        if do_debug:
            debugger.new_frame(frame)

        target_count = (target_count + 1) % ROI_PERIOD
        if target_count == 0:
            target = None

        target = (400, 300)     # TODO - remove this, only here for testing purposes
        roi = frame_to_roi(frame, target, debugger)
        mask = roi_to_mask(roi, debugger)
        leds = mask_to_leds(mask, debugger)
        panels = leds_to_panels(leds, debugger)
        target = panels_to_target(panels, debugger)
        coords = target_to_coords(target, debugger)
        aim_coords = predict_coords(coords, debugger)
        send_coords(aim_coords, debugger)

        if do_debug:
            debugger.show()
        successful, frame = capture.read()


class Debugger:
    def __init__(self):
        self.frame_count = 0
        self.frame = None
        self.logs = None

    def new_frame(self, frame):
        self.frame_count += 1
        self.frame = frame.copy()
        self.logs = []

    def show(self):
        cv2.imshow(WIN_TITLE, self.frame)
        cv2.waitKey(FRAME_DELAY)

    def print(self):
        print('\n'.join(self.logs))
