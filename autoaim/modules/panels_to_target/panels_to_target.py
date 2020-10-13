from autoaim_config import DO_DEBUG
from panels_to_target_config import *
import cv2


def panels_to_target(panels, capture):
    if len(panels) == 0:
        return None

    target_panel = panels[0]
    if DO_DEBUG:
        draw_target(capture, target_panel)
    return target_panel.center


def draw_target(capture, panel):
    distance_position = tuple([sum(p) for p in zip(capture.point_to_debug(panel.center), DRAW.DISTANCE_OFFSET)])
    cv2.circle(capture.debug_frame, tuple(capture.point_to_debug(panel.center)),
               DRAW.TARGET_RADIUS, DRAW.TARGET_COLOR, -1)
    cv2.putText(capture.debug_frame, DRAW.DISTANCE_FORMAT.format(panel.distance),
                distance_position, DRAW.FONT, DRAW.FONT_SIZE, DRAW.TEXT_COLOR)
