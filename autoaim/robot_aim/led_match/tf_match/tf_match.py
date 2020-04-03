from assets.module import Module
from pathlib import Path
import os
import numpy as np
import tensorflow as tf


class TfMatch(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.model = self.load_model(self.config['model_path'])

    def load_model(self, path=None):
        """
        Loads the saved_model from path
        :param path: path to the tensorflow checkpoint
        :return: The loaded model
        """
        if path is None:
            path = self.config['model_path']

        return tf.keras.models.load_model(self.wd / path)

    def process(self, led_pair):
        formatted_input = np.asarray([create_nn_input(led_pair)])
        prediction = self.model.predict(formatted_input)
        led_pair.confidences = {'confidence': prediction[0][1]}
        led_pair.is_panel = prediction[0][1] >= self.config['panel_criterion']


def find_ratio(a, b):
    """
    :param a: first number
    :param b: second number
    :return: ratio between them, between 0 and 1
    """
    if a == 0 or b == 0:  # prevent division by 0
        return 0
    return a / b if a < b else b / a


def create_nn_input(led_pair):
    """
    Creates one input for the network from an led pair
    :param led_pair: an LedPair object
    :return: list of inputs for the neural network
    """
    led1 = led_pair.led_left
    led2 = led_pair.led_right
    dw = find_ratio(led1.width, led2.width)
    dh = find_ratio(led1.height, led2.height)
    da = max(90, abs(led1.angle - led2.angle)) / 90
    dx = find_ratio(led1.center[0], led2.center[0])
    dy = find_ratio(led1.center[1], led2.center[1])
    return [dw, dh, da, dx, dy]
