from source.module import Module
from pathlib import Path
import os
import numpy as np
import cv2
from ..tensorflow_matcher.tensorflow_matcher import create_nn_input


class OpencvMatcher(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        self.model = cv2.dnn.readNetFromTensorflow(str(self.wd / self.config['load_model']))
        
    def process(self, led_pair):
        formatted_input = np.asarray([create_nn_input(led_pair)])
        prediction = self.model.predict(formatted_input)
        led_pair.confidences = {'confidence': prediction[0][1]}
        led_pair.is_panel = prediction[0][1] >= self.config['panel_criterion']
