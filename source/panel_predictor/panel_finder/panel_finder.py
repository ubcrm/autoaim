from source.panel_predictor.panel_finder.led_finder.led_finder import LEDFinder
from source.module import Module
from pathlib import Path
import os


def combined_panel(rect_a, rect_b):
    center = find_dict_center([rect_a, rect_b])
    width = abs(rect_a["x_center"] - rect_b["x_center"]) + (rect_a["width"] + rect_b["width"]) / 2
    height = abs(rect_a["y_center"] - rect_b["y_center"]) + (rect_a["height"] + rect_b["height"]) / 2
    angle = (rect_a["angle"] + rect_b["angle"]) / 2
    new_rect = {"x_center": center[0], "y_center": center[1], "width": width, "height": height, "angle": angle}

    return new_rect


def find_dict_center(bounds):
    """
        finds the center of 2 rectangles

        :param bounds: 2 rectangles in the dictionary form
        :return: the center in the form [x,y]
        """
    targetcX = int((bounds[0]["x_center"] + bounds[1]["x_center"]) / 2.0)
    targetcY = int((bounds[0]["y_center"] + bounds[1]["y_center"]) / 2.0)
    return targetcX, targetcY


class PanelFinder(Module):
    def __init__(self, parent=None, state=None):
        if state["framework"] == "tensorflow":
            from source.panel_predictor.panel_finder.panel_classifier.panel_classifier import PanelClassifier
            state["mode"] = "load"
            self.classifier = PanelClassifier(self, state=state)
        elif state["framework"] == "opencv":
            from source.panel_predictor.panel_finder.panel_classifier.inference_opencv import OpenCVClassifier
            self.classifier = OpenCVClassifier(self, state=state)

        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        self.led_finder = LEDFinder(self)
        self.panel = None

    def predict_leds(self, led_a, led_b, frame_dims):
        return self.classifier.process((led_a, led_b), frame_dims)
        # return 0.01

    def process(self, frame):
        """
        find a robot panel from and image
        :param frame: an image that may contain a robot
        :return: a dict describing a rotated rectangle
        """
        frame_dims = frame.shape[:2]
        leds = self.led_finder.process(frame)
        leds = sorted(leds, key=lambda x: x['angle'])

        if len(leds) > 1:
            best_pair = (leds[0], leds[1], self.predict_leds(leds[0], leds[1], frame_dims))

            for i in range(1, len(leds) - 1):
                confidence = self.predict_leds(leds[i], leds[i + 1], frame_dims)
                if confidence > best_pair[2]:
                    best_pair = (leds[i], leds[i + 1], confidence)

            return combined_panel(best_pair[0], best_pair[1]), best_pair[2]
