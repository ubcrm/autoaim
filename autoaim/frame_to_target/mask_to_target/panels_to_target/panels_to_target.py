from panels_to_target_config import *
import cv2


def panels_to_target(panels, debug_frame=None):
    if len(panels) == 0:
        return None

    target_panel = panels[0]
    if debug_frame is not None:
        draw_target(debug_frame, target_panel)
    return target_panel.center


def draw_target(frame, panel):
    distance_position = tuple([sum(p) for p in zip(panel.center, DRAW.DISTANCE_OFFSET)])
    cv2.circle(frame, panel.center, DRAW.TARGET_RADIUS, DRAW.TARGET_COLOR, -1)
    cv2.putText(frame, DRAW.DISTANCE_FORMAT.format(panel.distance),
                distance_position, DRAW.FONT, DRAW.FONT_SIZE, DRAW.TEXT_COLOR)
