import cv2

TARGET_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)
TARGET_RADIUS = 3


def panels_to_target(panels, com):
    if len(panels) == 0:
        return None

    target = Target(panels[0])
    if com.debug:
        target.draw(com)
    return target


class Target:
    def __init__(self, panel):
        self.center = panel.center
        self.distance = panel.distance

    def draw(self, com):
        center = tuple(com.orig_to_debug(self.center))
        cv2.circle(com.debug_frame, center, TARGET_RADIUS, TARGET_COLOR, -1)
