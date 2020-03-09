from source.module import Module
from pathlib import Path
import os
import numpy as np
import cv2
from ..tf_matcher.tf_matcher import create_nn_input


class OpencvMatcher(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        self.model = cv2.dnn.readNetFromTensorflow(str(self.wd / self.config['load_model']))
        
    def process(self, led_pair):
        formatted_input = np.asarray([create_nn_input(led_pair)])
        self.model.setInput(formatted_input)
        prediction = self.model.forward()
        led_pair.confidences = {'confidence': prediction[0][1]}
        led_pair.is_panel = prediction[0][1] >= self.config['panel_criterion']
