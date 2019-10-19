"""
Reads data from Data/ and trains the Neural network on this data.
The network is then saved to be used in led_match.py
"""

import tensorflow as tf
import numpy as np
import datetime
import argparse
import math
import json
import sys


def get_json_from_file(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)


class TensorflowPipeline:
    def __init__(self, settings_json, data_json):
        self.settings = get_json_from_file(settings_json)
        self.data = get_json_from_file(data_json)
        self.shape = self.settings["learning"]["network_shape"]
        self.model = self.create_model()

    def train_model(self):
        """
        Trains and evaluates the model.
        :param data_json: JSON file containing training data. If no data is passed, it will use the file in settings.
        """

        # load data from json
        train_x, train_y, test_x, test_y = self.create_data()

        # train model, update tensorboard
        log_dir = self.settings["log_dir"] + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        self.model.fit(train_x, train_y, epochs=self.settings["learning"]["epochs"], callbacks=[tensorboard_callback])

        self.model.evaluate(test_x, test_y, verbose=1)

    def evaluate_model(self, x, y):
        """
        Evaluates the model.
        :param x: Data input
        :param y: Desired output
        """
        try:
            print("Evaluating model")
            self.model.evaluate(x, y)
        except ValueError:
            print("Tried to evaluate model non-existent model. Either load or train a model first.")

    def save_model(self):
        """
        Saves the model to the directory specified in settings
        """
        print("Saving model")
        tf.saved_model.save(self.model, self.settings["model_path"])
        self.model.save(self.settings["model_path"])

    @staticmethod
    def load_model(path):
        """
        Loads the saved_model from path
        :param path: path to the tensorflow checkpoint
        :return: The loaded model
        """
        return tf.keras.models.load_model(path)

    @staticmethod
    def model_predict(model, model_input):
        o = model.predict(model_input)
        print(o)
        return o.argmax()


    def create_nn_input(self, leds):
        """
        Creates one input for the network from leds
        :param leds: One pair of LEDs represented as a python dictionary
        :return: list of inputs for the neural network
        """
        led_1 = leds[0]
        led_2 = leds[1]
        dw = abs(led_1["width"] - led_2["width"]) / self.settings["video_dims"]["w"]
        dh = abs(led_1["height"] - led_2["height"]) / self.settings["video_dims"]["h"]
        da = abs(led_1["angle"] - led_2["angle"]) / 90
        dx = abs(led_1["x_center"] - led_2["x_center"]) / self.settings["video_dims"]["w"]
        dy = abs(led_1["y_center"] - led_2["y_center"]) / self.settings["video_dims"]["h"]
        return [dw, dh, da, dx, dy]

    def create_data(self):
        """
        Parses a json file storing training data into network input
        :param json_filename: path to training data
        :return: numpy array of network input
        """
        data = self.data
        data_x = [self.create_nn_input((data[pair]['led1'], data[pair]['led2'])) for pair in data]
        data_y = [data[pair]["isPanel"] for pair in data]
        for i in range(len(data_y)):
            if data_y[i] == 1:
                data_y[i] = [1, 0]
            else:
                data_y[i] = [0, 1]

        # split into training and testing data
        split_idx = int(len(data) * self.settings["train_test_ratio"])
        t_x = np.array(data_x[:split_idx])
        t_y = np.array(data_y[:split_idx])
        te_x = np.array(data_x[split_idx:])
        te_y = np.array(data_y[split_idx:])
        return t_x, t_y, te_x, te_y

    def create_layers(self):
        """
        Generate the neural network layers.
        Current structure: 3 dense layers of size 5, 3, 2
        Output layer is a classifier of pair vs. not pair
        :return: network layers as list
        """
        return [
            tf.keras.layers.Dense(self.shape[0], activation=tf.nn.relu),
            tf.keras.layers.Dense(self.shape[1]),
            tf.keras.layers.Dense(2, activation=tf.nn.softmax)
        ]

    def create_model(self):
        """
        Create the tensorflow model specifying optimizer, loss, and metrics
        :return: the tensorflow model
        """
        m = tf.keras.models.Sequential()
        for layer in self.create_layers():
            m.add(layer)
        m.compile(
            optimizer='adam',
            loss="categorical_crossentropy",
            metrics=['accuracy'])
        return m


if __name__ == "__main__":

    model_path = sys.argv[1]
    settings = sys.argv[2]
    training_data = sys.argv[3]

    pipeline = TensorflowPipeline(settings, training_data)
    pipeline.train_model()
    pipeline.save_model()

    m = TensorflowPipeline.load_model(model_path)
    training_x, training_y, testing_x, testing_y = m.create_data(training_data)
    print(TensorflowPipeline.model_predict(m, training_x[0]))
