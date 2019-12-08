from source.instance import get_json_from_path
from source.module import Module
from pathlib import Path
import numpy as np
import cv2
import os


def find_ratio(a, b):
    """
    Compares two numbers by finding the ratio between them. The result is between 0 and 1.
    When using this function, please the numbers passed have the same sign.

    1 means they are identical
    0 means one is infinitely larger than the other
    :param a: first number to compare
    :param b: second number to compare
    :return: ratio between them, between 0 and 1
    """
    if a == 0 or b == 0:  # prevent div by 0
        return 0
    return a / b if a < b else b / a


class OpenCVClassifier(Module):
    def __init__(self, parent, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        self.net = self.load_model()

    def load_model(self, path=None):
        """
        Loads the saved_model from path
        :param path: path to the tensorflow frozen pb path
        :return: The loaded model
        """
        if path is None:
            path = self.properties["load_tf_model"]

        return cv2.dnn.readNetFromTensorflow(str(self.working_dir / path))

    @staticmethod
    def model_predict(net, nn_input):
        net.setInput(nn_input)
        return net.forward()

    @staticmethod
    def create_nn_input(leds, video_dims):
        """
        Creates one input for the network from leds
        :param leds: One pair of LEDs represented as a python dictionary
        :param video_dims: Tuple of video dimensions (w, h)
        :return: list of inputs for the neural network
        """
        led_1 = leds[0]
        led_2 = leds[1]
        dw = find_ratio(led_1["width"], led_2["width"])  # width diff
        dh = find_ratio(led_1["height"], led_2["height"])  # height diff
        da = abs(led_1["angle"] - led_2["angle"]) / 90  # angle change
        dx = find_ratio(led_1["x_center"], led_2["x_center"])  # x pos diff
        dy = find_ratio(led_1["y_center"], led_2["y_center"])  # y pos diff
        return [dw, dh, da, dx, dy]


    def process(self, leds, frame_dims):
        formatted_input = np.asarray([OpenCVClassifier.create_nn_input(leds, frame_dims)])
        prediction = self.model_predict(self.net, formatted_input)
        return prediction[0][1]
