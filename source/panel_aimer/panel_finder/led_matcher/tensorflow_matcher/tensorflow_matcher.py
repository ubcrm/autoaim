from source.module import Module
from pathlib import Path
import os
import numpy as np
import tensorflow as tf
from datetime import datetime
import json
from ...led_matcher.led_matcher import LedPair
from ...led_finder.led_finder import BoundingRect


# todo: fix this module
class TensorflowMatcher(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        if self.config['mode'] == 'train':
            with open(self.wd / self.config['data_path']) as data_file:
                self.data = json.load(data_file)
            self.shape = self.config['learning']['network_shape']
            self.model = self.create_model()
            self.train_model()
            self.save_model()

        elif self.config['mode'] == 'load' or self.config['mode'] == 'convert':
            self.model = self.load_model(self.config['model_path'])

            if self.config['mode'] == 'convert':
                self.save_to_tensorflow()

    def train_model(self):
        """
        Trains the model.
        :return: text_x and text_y paramters, which can be fed into evaluate_model()
        """
        # load data from json file
        train_x, train_y, test_x, test_y = self.create_data()

        # train model, update tensorboard
        log_append = self.config['log_dir'] + datetime.now().strftime('%Y%m%d-%H%M%S')
        log_dir = Path(self.wd / log_append)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        self.model.fit(train_x, train_y, epochs=self.config['learning']['epochs'], callbacks=[tensorboard_callback],
                       class_weight={0: 1., 1: 7.})

        return test_x, test_y

    def evaluate_model(self, x, y):
        """
        Evaluates the model.
        :param x: Data input
        :param y: Desired output
        """
        try:
            print('Evaluating model')
            self.model.evaluate(x, y, verbose=1)
        except ValueError:
            print('Tried to evaluate model non-existent model. Either load or train a model first.')

    def save_model(self, path=None):
        """
        Saves the model to the directory specified deploy script
        """
        print('Saving model')
        if path is None:
            path = self.config['model_path']

        self.model.save(self.wd / path)

    def save_to_tensorflow(self):
        frozen_graph = self.freeze_session(output_names=[out.op.name for out in self.model.outputs])
        tf.compat.v1.train.write_graph(frozen_graph, str(self.wd / self.config['create_tf_model_path']),
                                       'model.pb', as_text=False)

    def freeze_session(self, keep_var_names=None, output_names=None, clear_devices=True):
        """
        Freezes the state of a session into a pruned computation graph.

        Creates a new computation graph where variable nodes are replaced by
        constants taking their current value in the session. The new graph will be
        pruned so subgraphs that are not necessary to compute the requested
        outputs are removed.
        :param keep_var_names: A list of variable names that should not be frozen,
                              or None to freeze all the variables in the graph.
        :param output_names: Names of the relevant graph outputs.
        :param clear_devices: Remove the device directives from the graph for better portability.
        :return: The frozen graph definition.
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
            path = self.config['model_path']

        return tf.keras.models.load_model(self.wd / path)

    def create_data(self, data=None):
        """
        Parses a json file storing training data into network input
        :return: numpy array of network input
        """
        if data is None:
            data = self.data
        data_x, data_y = [], []
        for value in data.values():
            led1 = BoundingRect('', (
                (value['led1']['width'], value['led1']['height']),
                (value['led1']['x_center'], value['led1']['y_center']),
                value['led1']['angle']), {})
            led2 = BoundingRect('', (
                (value['led2']['width'], value['led2']['height']),
                (value['led2']['x_center'], value['led2']['y_center']),
                value['led2']['angle']), {})
            data_x.append(create_nn_input(LedPair(led1, led2)))
            data_y.append([0, 1] if value['isPanel'] else [1, 0])

        # split into training and testing data
        split_idx = int(len(data) * self.config['train_test_ratio'])
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
            tf.keras.layers.Dense(units=self.shape[0], activation=tf.nn.relu, input_shape=(self.shape[0],)),
            tf.keras.layers.Dense(self.shape[1]),
            tf.keras.layers.Dense(2, activation=tf.nn.softmax)
        ]

    def create_model(self):
        """
        Create the tensorflow model specifying optimizer, loss, and metrics
        :return: the tensorflow model
        """
        m = tf.keras.models.Sequential()
        o = tf.keras.optimizers.Adam(learning_rate=self.config['learning']['learning_rate'])

        for layer in self.create_layers():
            m.add(layer)
        m.compile(optimizer=o, loss='binary_crossentropy', metrics=['accuracy'])
        return m

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
