"""
Reads data from Data/ and trains the Neural network on this data.
The network is then saved to be used in led_match.py
"""

import datetime
import os
from pathlib import Path

import numpy as np
import tensorflow as tf

from source.common.module import Module
from source.instance import get_json_from_path, ROOT_DIR


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


class PanelClassifier(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state, default={"mode": "train"})

        if self.properties["mode"] == "train":
            self.data = get_json_from_path(ROOT_DIR / self.properties["data_path"])
            self.shape = self.properties["learning"]["network_shape"]
            self.model = self.create_model()
            self.train_model()
            self.save_model()
            # self.save_to_tensorflow()

        elif self.properties["mode"] == "load":
            self.model = self.load_model(self.properties["model_path"])

    def train_model(self):
        """
        Trains the model.
        :return text_x and text_y paramters, which can be fed into
         evaluate_model()
        """

        # load data from json file
        train_x, train_y, test_x, test_y = self.create_data()

        # train model, update tensorboard
        log_dir = self.properties["log_dir"] + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        log_dir = log_dir.replace("/", os.path.sep)
        print(os.path.sep)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        self.model.fit(train_x, train_y, epochs=self.properties["learning"]["epochs"], callbacks=[tensorboard_callback],
                       class_weight={0: 1.,
                                     1: 7.})

        return test_x, test_y

    def evaluate_model(self, x, y):
        """
        Evaluates the model.
        :param x: Data input
        :param y: Desired output
        """
        try:
            print("Evaluating model")
            self.model.evaluate(x, y, verbose=1)
        except ValueError:
            print("Tried to evaluate model non-existent model. Either load or train a model first.")

    def save_model(self, path=None):
        """
        Saves the model to the directory specified deploy script
        """
        print("Saving model")
        if path is None:
            path = self.properties["model_path"]
        self.model.save(ROOT_DIR / path)

    def save_to_tensorflow(self):
        frozen_graph = self.freeze_session(output_names=[out.op.name for out in self.model.outputs])
        tf.compat.v1.train.write_graph(frozen_graph, str(self.working_dir), "my_model.pb", as_text=False)

    def freeze_session(self, keep_var_names=None, output_names=None, clear_devices=True):
        """
        Freezes the state of a session into a pruned computation graph.

        Creates a new computation graph where variable nodes are replaced by
        constants taking their current value in the session. The new graph will be
        pruned so subgraphs that are not necessary to compute the requested
        outputs are removed.
        @param session The TensorFlow session to be frozen.
        @param keep_var_names A list of variable names that should not be frozen,
                              or None to freeze all the variables in the graph.
        @param output_names Names of the relevant graph outputs.
        @param clear_devices Remove the device directives from the graph for better portability.
        @return The frozen graph definition.
        """

        session = tf.compat.v1.keras.backend.get_session()
        graph = session.graph
        with graph.as_default():
            freeze_var_names = list(
                set(v.op.name for v in tf.compat.v1.global_variables()).difference(keep_var_names or []))
            output_names = output_names or []
            output_names += [v.op.name for v in tf.compat.v1.global_variables()]
            input_graph_def = graph.as_graph_def()
            if clear_devices:
                for node in input_graph_def.node:
                    node.device = ""
            frozen_graph = tf.compat.v1.graph_util.convert_variables_to_constants(
                session, input_graph_def, output_names, freeze_var_names)
            return frozen_graph

    def load_model(self, path=None):
        """
        Loads the saved_model from path
        :param path: path to the tensorflow checkpoint
        :return: The loaded model
        """
        if path is None:
            path = self.properties["model_path"]

        return tf.keras.models.load_model(ROOT_DIR / path)

    @staticmethod
    def model_predict(model, model_input):
        o = model.predict(model_input)
        # print(o, o.argmax())
        return o

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

    def create_data(self, data=None, video_dims=None):
        """
        Parses a json file storing training data into network input
        :return: numpy array of network input
        """

        if data is None:
            data = self.data

        if video_dims is None:
            video_dims = (self.properties["video_dims"]["w"], self.properties["video_dims"]["h"])
        data_x = []
        for pair in data:
            led_1 = data[pair]["led1"]
            led_2 = data[pair]["led2"]
            data_x.append(PanelClassifier.create_nn_input((led_1, led_2), video_dims))

        data_y = [data[pair]["isPanel"] for pair in data]
        for i in range(len(data_y)):
            if data_y[i] == 1:
                data_y[i] = [0, 1]
            else:
                data_y[i] = [1, 0]

        # split into training and testing data
        split_idx = int(len(data) * self.properties["train_test_ratio"])
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

    def process(self, leds, frame_dims):
        formatted_input = np.asarray([PanelClassifier.create_nn_input(leds, frame_dims)])
        return self.model.predict(formatted_input)[0][0]-self.model.predict(formatted_input)[0][1]
