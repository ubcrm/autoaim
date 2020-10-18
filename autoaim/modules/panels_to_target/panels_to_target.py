from autoaim_config import DO_DEBUG
from panels_to_target_config import *
import cv2


def panels_to_target(panels, capture):
    if len(panels) == 0:
        return None

    target = Target(capture, panels[0])
    if DO_DEBUG:
        target.draw(capture)
    return target


class Target:
    def __init__(self, capture, panel):
        self.loc = panel.center
        self.loc_debug = tuple(capture.point_to_debug(panel.center))
        self.distance = panel.distance

    def draw(self, capture):
        distance_position = tuple([sum(p) for p in zip(self.loc_debug, DRAW.DISTANCE_OFFSET)])
        cv2.circle(capture.debug_frame, self.loc_debug,
                   DRAW.TARGET_RADIUS, DRAW.TARGET_COLOR, -1)
        cv2.putText(capture.debug_frame, DRAW.DISTANCE_FORMAT.format(self.distance),
                    distance_position, DRAW.FONT, DRAW.FONT_SIZE, DRAW.TEXT_COLOR)
