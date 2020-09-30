from mask_to_leds import mask_to_leds
from leds_to_panels import leds_to_panels
from panels_to_target import panels_to_target


def mask_to_target(mask, debug_frame=None):
    leds = mask_to_leds(mask, debug_frame=debug_frame)
    panels = leds_to_panels(leds, debug_frame=debug_frame)
    target = panels_to_target(panels, debug_frame=debug_frame)
    return target, panels
