"""
Reads data from Data/ and trains the Neural network on this data.
The network is then saved to be used in LED_match.py
"""
import datetime
import math
import tensorflow as tf
import numpy as np
import json
import sys


def get_json_from_file(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)


class TensorflowPipeline:
    def __init__(self, settings_json):
        self.settings = get_json_from_file(settings_json)
        self.model = None
        tf.saved_model.save(self.model, self.settings["model_path"])

    def train_model(self, data_json="from_settings"):
        data_path = data_json
        if data_json == "from_settings":
            data_path = self.settings["data_path"]
        train_x, train_y, test_x, test_y = self.create_data(data_path)
        self.evaluate_model(test_x, test_y)
        self.model = self.create_model(train_x, train_y)

    def evaluate_model(self, x, y):
        try:
            print("Evaluating model")
            self.model.evaluate(x, y)
        except ValueError:
            print("Tried to evaluate model non-existent model. Either load or train a model first.")

    def save_model(self):
        print("Saving model")
        tf.saved_model.save(self.model, self.settings["model_path"])

    @staticmethod
    def create_nn_input(leds):
        led_1 = leds[0]
        led_2 = leds[1]
        dw = abs(led_1["width"] - led_2["width"])
        dh = abs(led_1["height"] - led_2["height"])
        da = abs(led_1["angle"] - led_2["angle"])
        dx = abs(led_1["center"]["x"] - led_2["center"]["x"])
        dy = abs(led_1["center"]["y"] - led_2["center"]["y"])
        return [dw, dh, da, dx, dy]

    def create_data(self, json_filename):
        data = get_json_from_file(json_filename)  # nothing to parse until training data is made
        data_x = [self.create_nn_input((data[pair]["led1"], data[pair]["led2"])) for pair in data]
        data_y = [data[pair]["isPanel"] for pair in data]
        for i in range(len(data_y)):
            if data_y[i] == 1:
                data_y[i] = [1, 0]
            else:
                data_y[i] = [0, 1]

        split_idx = int(len(data) * self.settings["train_test_ratio"])
        t_x = np.array(data_x[:split_idx])
        t_y = np.array(data_y[:split_idx])
        te_x = np.array(data_x[:split_idx])
        te_y = np.array(data_y[:split_idx])
        return t_x, t_y, te_x, te_y

    def create_layers(self):
        i_size = self.settings["learning"]["input_size"]
        hidden_size = math.ceil((i_size + 1) / 2)
        return [
            tf.keras.layers.Dense(i_size, activation=tf.nn.relu),
            tf.keras.layers.Dense(hidden_size),
            tf.keras.layers.Dense(2, activation=tf.nn.softmax)
        ]

    def create_model(self, x, y):
        m = tf.keras.models.Sequential()
        for layer in self.create_layers():
            m.add(layer)
        m.compile(
            optimizer='adam',
            loss="categorical_crossentropy",
            metrics=['accuracy'])
        log_dir = self.settings["log_dir"] + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        m.fit(x, y, epochs=self.settings["learning"]["epochs"], callbacks=[tensorboard_callback])
        return m


if __name__ == "__main__":
    pipeline = TensorflowPipeline(sys.argv[1])
