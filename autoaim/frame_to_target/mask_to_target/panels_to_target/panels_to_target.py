import panels_to_target_config as CONFIG
import cv2


def panels_to_target(panels, debug_frame=None):
    target_panel = panels[0]
    if debug_frame is not None:
        draw_target(debug_frame, target_panel)
    return target_panel.center


def draw_target(frame, panel):
    distance_position = tuple([sum(p) for p in zip(panel.center, CONFIG.DRAW.DISTANCE_OFFSET)])
    cv2.circle(frame, panel.center, CONFIG.DRAW.TARGET_RADIUS, CONFIG.DRAW.TARGET_COLOR, -1)
    cv2.putText(frame, CONFIG.DRAW.DISTANCE_FORMAT.format(panel.distance),
                distance_position, CONFIG.DRAW.FONT, CONFIG.DRAW.FONT_SIZE, CONFIG.DRAW.TEXT_COLOR)
