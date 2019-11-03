# """
# Reads data from Data/ and trains the Neural network on this data.
# The network is then saved to be used in led_match.py
# """
#
# import tensorflow as tf
# import numpy as np
# import datetime
# import argparse
# import math
# import json
# import sys
#
#
# def get_json_from_file(filename):
#     with open(filename, 'r') as json_file:
#         return json.load(json_file)
#
#
# class PanelClassifier:
#     def __init__(self, settings_path, data_path, model_path):
#         self.settings = get_json_from_file(settings_path)
#         self.data = get_json_from_file(data_path)
#         self.shape = self.settings["learning"]["network_shape"]
#         self.model = self.create_model()
#
#     def train_model(self):
#         """
#         Trains the model.
#         :return text_x and text_y paramters, which can be fed into
#          evaluate_model()
#         """
#
#         # load data from json file
#         train_x, train_y, test_x, test_y = self.create_data()
#
#         # train model, update tensorboard
#         log_dir = self.settings["log_dir"] + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#         tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
#         self.model.fit(train_x, train_y, epochs=self.settings["learning"]["epochs"], callbacks=[tensorboard_callback],
#                        class_weight={0: 1.,
#                                      1: 7.})
#
#         return test_x, test_y
#
#     def evaluate_model(self, x, y):
#         """
#         Evaluates the model.
#         :param x: Data input
#         :param y: Desired output
#         """
#         try:
#             print("Evaluating model")
#             self.model.evaluate(x, y, verbose=1)
#         except ValueError:
#             print("Tried to evaluate model non-existent model. Either load or train a model first.")
#
#     def save_model(self):
#         """
#         Saves the model to the directory specified deploy script
#         """
#         print("Saving model")
#         self.model.save(model_path)
#
#     @staticmethod
#     def load_model(path):
#         """
#         Loads the saved_model from path
#         :param path: path to the tensorflow checkpoint
#         :return: The loaded model
#         """
#         return tf.keras.models.load_model(path)
#
#     @staticmethod
#     def model_predict(model, model_input):
#         o = model.predict(model_input)
#         # print(o, o.argmax())
#         return o
#
#     @staticmethod
#     def create_nn_input(leds, video_dims):
#         """
#         Creates one input for the network from leds
#         :param leds: One pair of LEDs represented as a python dictionary
#         :param video_dims: Tuple of video dimensions (w, h)
#         :return: list of inputs for the neural network
#         """
#         led_1 = leds[0]
#         led_2 = leds[1]
#         dw = abs(led_1["width"] - led_2["width"]) / video_dims[0]  # width change
#         dh = abs(led_1["height"] - led_2["height"]) / video_dims[1]  # height change
#         da = abs(led_1["angle"] - led_2["angle"]) / 90  # angle change
#         dx = abs(led_1["x_center"] - led_2["x_center"]) / video_dims[0]
#         dy = abs(led_1["y_center"] - led_2["y_center"]) / video_dims[1]
#         return [dw, dh, da, dx, dy]
#
#     def create_data(self):
#         """
#         Parses a json file storing training data into network input
#         :return: numpy array of network input
#         """
#         data = self.data
#
#         video_dims = (self.settings["video_dims"]["w"], self.settings["video_dims"]["h"])
#         data_x = []
#         for pair in data:
#             led_1 = data[pair]["led1"]
#             led_2 = data[pair]["led2"]
#             data_x.append(PanelClassifier.create_nn_input((led_1, led_2), video_dims))
#
#         data_y = [data[pair]["isPanel"] for pair in data]
#         for i in range(len(data_y)):
#             if data_y[i] == 1:
#                 data_y[i] = [0, 1]
#             else:
#                 data_y[i] = [1, 0]
#
#         # split into training and testing data
#         split_idx = int(len(data) * self.settings["train_test_ratio"])
#         t_x = np.array(data_x[:split_idx])
#         t_y = np.array(data_y[:split_idx])
#         te_x = np.array(data_x[split_idx:])
#         te_y = np.array(data_y[split_idx:])
#         return t_x, t_y, te_x, te_y
#
#     def create_layers(self):
#         """
#         Generate the neural network layers.
#         Current structure: 3 dense layers of size 5, 3, 2
#         Output layer is a classifier of pair vs. not pair
#         :return: network layers as list
#         """
#         return [
#             tf.keras.layers.Dense(self.shape[0], activation=tf.nn.relu),
#             tf.keras.layers.Dense(self.shape[1]),
#             tf.keras.layers.Dense(2, activation=tf.nn.softmax)
#         ]
#
#     def create_model(self):
#         """
#         Create the tensorflow model specifying optimizer, loss, and metrics
#         :return: the tensorflow model
#         """
#         m = tf.keras.models.Sequential()
#         for layer in self.create_layers():
#             m.add(layer)
#         m.compile(
#             optimizer='adam',
#             loss="categorical_crossentropy",
#             metrics=['accuracy'])
#         return m
#
#
# if __name__ == "__main__":
#     settings_path = sys.argv[1]
#     data_path = sys.argv[2]
#     model_path = sys.argv[3]
#
#     pipeline = PanelClassifier(settings_path, data_path, model_path)
#
#     test_x, test_y = pipeline.train_model()
#     pipeline.evaluate_model(test_x, test_y)
#     pipeline.save_model()
#
#     m = PanelClassifier.load_model(model_path)
#
#     training_x, training_y, testing_x, testing_y = pipeline.create_data()
#
#     network_input = np.asarray([training_x[0]])
#     print("The model predicts:", PanelClassifier.model_predict(m, network_input))
#     print("The actual value is:", training_y[0].argmax())
