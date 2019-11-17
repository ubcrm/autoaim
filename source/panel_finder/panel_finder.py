from source.panel_finder.panel_classifier.panel_classifier import PanelClassifier
from source.panel_finder.led_finder.led_finder import LEDFinder
from source.instance import get_json_from_file
from source.panel_finder.find_center import find_target_center, find_dict_center
from pathlib import Path
import os


def combined_panel(rect_a, rect_b):
    center = find_dict_center([rect_a, rect_b])
    width = abs(rect_a["x_center"] - rect_b["x_center"]) + (rect_a["width"] + rect_b["width"]) / 2
    height = abs(rect_a["y_center"] - rect_b["y_center"]) + (rect_a["height"] + rect_b["height"]) / 2
    angle = (rect_a["angle"] + rect_b["angle"]) / 2
    new_rect = {"x_center": center[0], "y_center": center[1], "width": width, "height": height, "angle": angle}

    return new_rect


class PanelFinder:
    def __init__(self, state=None):
        if state is None:
            state = {}
        working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.properties = get_json_from_file(working_dir / "settings.json")
        self.properties.update(state)  # merges static settings and dynamically passed state. States override settings.
        self.classifier = PanelClassifier(state={"mode": "load"})
        self.led_finder = LEDFinder()
        self.panel = None

    def predict_leds(self, led_a, led_b, frame_dims):
        return self.classifier.process((led_a, led_b), frame_dims)

    def process(self, frame):
        frame_dims = frame.shape[:2]
        leds = self.led_finder.process(frame)
        leds = sorted(leds, key=lambda x: x['angle'])

        if len(leds) > 1:
            best_pair = (leds[0], leds[1], self.predict_leds(leds[0], leds[1], frame_dims))

            for i in range(1, len(leds) - 1):
                confidence = self.predict_leds(leds[i], leds[i + 1], frame_dims)
                if confidence > best_pair[2]:
                    best_pair = (leds[i], leds[i + 1], confidence)

            if best_pair[2] > 0.5:
                self.panel = combined_panel(best_pair[0], best_pair[1])
        return self.panel
