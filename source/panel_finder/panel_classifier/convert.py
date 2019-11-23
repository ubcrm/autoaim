from source.instance import get_json_from_path
from source.common.module import Module
from pathlib import Path
import tensorflow as tf
import os

class Convert(Module):
    '''Class creates a blank tensorflow 1.14 model, loads the weights
       created in the tensorflow 2.0 runtime, then saves the whole model
       as a tensorflow 1.14 model 
       
       *** Run the code in the tf114 virtual environment ***
    '''

    def __init__(self):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir)
        self.shape = self.properties["learning"]["network_shape"]
        self.model = self.create_model()
        self.save_model()

    def create_model(self):
        """
        Create the tensorflow model specifying optimizer, loss, and metrics
        :return: the tensorflow model
        """
        m = tf.keras.models.Sequential()
        o = tf.keras.optimizers.Adam(
            learning_rate=self.properties["learning"]["learning_rate"]
        )

        for layer in self.create_layers():
            m.add(layer)
        m.compile(
            optimizer=o,
            loss="binary_crossentropy",
            metrics=['accuracy'])
        return m

    def create_layers(self):
        """
        Generate the neural network layers.
        Current structure: 3 dense layers of size 5, 3, 2
        Output layer is a classifier of pair vs. not pair
        :return: network layers as list
        """
        return [
            tf.keras.layers.Dense(units=self.shape[0], activation=tf.nn.relu, input_shape=(self.shape[0],)),
            tf.keras.layers.Dense(self.shape[1]),
            tf.keras.layers.Dense(2, activation=tf.nn.softmax)
        ]

    def save_model(self):
        self.model.load_weights(self.properties["model_weights_path"])
        self.model.save(self.properties["tf114_model_path"])

if __name__ == '__main__':
    Convert()