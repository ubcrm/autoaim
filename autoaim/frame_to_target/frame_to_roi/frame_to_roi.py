import frame_to_roi_config as CONFIG
import itertools
import cv2
from numpy import linalg


def frame_to_roi(roi, panels, debug_frame=None):
    height, width, _ = roi.shape
    resize_dims = (round(width * CONFIG.SCALE), round(height * CONFIG.SCALE))
    roi = cv2.resize(roi, resize_dims)

    # TODO
    #   - fix error when returning cropped_roi (which is what should be returned)
    #       - error occurs with red_underexposed_1.mp4
    #   - Keep crop location relative to frame origin for determining target coordinates
    #   - margin should vary with distance
    #   - consider PanelPair class
    #   - make crop outline in the debug frame more visible after masking

    # (x, y)
    top_left = [0, 0]
    bottom_right = [width, height]

    # if no panels, do not crop
    # crop with extra wide margin
    if len(panels) == 1:
        top_left = [max(panels[0].center[0] - CONFIG.CROP.MARGIN_LARGE, 0),
                    max(panels[0].center[1] - CONFIG.CROP.MARGIN_LARGE, 0)]
        bottom_right = [min(panels[0].center[0] + CONFIG.CROP.MARGIN_LARGE, width),
                        min(panels[0].center[1] + CONFIG.CROP.MARGIN_LARGE, height)]

    # find furthest panels, crop with margin
    elif len(panels) > 1:
        furthest = -1
        furthest_panel_pair = []

        # not very pythonic
        for panel_pair in itertools.combinations(panels, 2):
            dist = linalg.norm([(panel_pair[0].center[i] - panel_pair[1].center[i]) for i in range(2)])
            if dist > furthest:
                furthest = dist
                furthest_panel_pair = panel_pair

        left_panel, right_panel = furthest_panel_pair[0].center[0], furthest_panel_pair[1].center[0]
        if left_panel > right_panel:
            left_panel, right_panel = right_panel, left_panel

        top_panel, bottom_panel = furthest_panel_pair[0].center[1], furthest_panel_pair[1].center[1]
        if top_panel > bottom_panel:
            top_panel, bottom_panel = bottom_panel, top_panel

        top_left = [max(left_panel - CONFIG.CROP.MARGIN_SMALL, 0),
                    max(top_panel - CONFIG.CROP.MARGIN_SMALL, 0)]
        bottom_right = [min(right_panel + CONFIG.CROP.MARGIN_SMALL, width),
                        min(bottom_panel + CONFIG.CROP.MARGIN_SMALL, height)]

    cropped_roi = roi[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    if debug_frame is not None:
        debug_frame.resize(roi.shape, refcheck=False)
        debug_frame[:] = roi
        cv2.rectangle(debug_frame, tuple(top_left), tuple(bottom_right), CONFIG.DEBUG.COLOUR, CONFIG.DEBUG.THICKNESS)

    return roi
