from resource import bit_mask, detect_shape, match_leds, find_center
from tensorflow_pipeline.tensorflow_pipeline import TensorflowPipeline
from imutils.video import FPS
import tensorflow as tf
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-m", "--model", required=True,
	help="path to keras model file")
args = vars(ap.parse_args())

# Load model from disk
print('[INFO] loading model from disk...')
model_path = args['model']
model = TensorflowPipeline.load_model(model_path)

print('\n'+'[INFO] loading image from disk...')
image = cv2.imread(args['image'])

# start frames per second counter
print('[INFO] starting frames per second counter...')
fps = FPS().start()

# 1. Preprocess image/frame
#image = imutils.resize(image, width=400)
cv2.imshow('image', image)
cv2.waitKey(0)

# 2. Mask LEDs
mask = bit_mask.under_exposed_threshold(image)
print('\n'+'[INFO] mask:'+'\n')
print(mask)
cv2.imshow('mask', mask)
cv2.waitKey(0)

# 3. Locate LEDs
rectangles = detect_shape.find_rectangles(mask)
print('\n'+'[INFO] rectangles:'+'\n')
print(rectangles)

# 4. Match pairing LEDs
leds = []
inputs = []

for r in rectangles:
	reformat = detect_shape.reformat_cv_rectangle(r)
	leds.append(reformat)

print(leds)
centers = {}

for i in range(len(leds)):
	for j in range(len(leds)):
		if i == j:
			continue
		video_dims = (1920, 1080)

		first_bound = (leds[i]['x_center'],leds[i]['y_center'])
		second_bound = (leds[j]['x_center'],leds[j]['y_center'])
		center = find_center.find_target_center((first_bound, second_bound))

		res = TensorflowPipeline.create_nn_input((leds[i], leds[j]), video_dims)
		inputs.append([res])
		centers[res[3]] = center

print('\n'+'[INFO] inputs:'+'\n')
for i in inputs:
	print(i)
print("------")

best_input = inputs[0]
highest_confidence = 0

for i in np.asarray(inputs):
	prediction = TensorflowPipeline.model_predict(model, i)
	if prediction[0][1] > highest_confidence:
		best_input = i
		highest_confidence = prediction[0][1]

print('\n'+'[INFO] best input and confidence:')
print(best_input, highest_confidence)

# 5. Locate Target Center Coordinates
center_coordinates = centers[best_input[0][3]]
cv2.circle(image, (center_coordinates[0], center_coordinates[1]), 3, (0, 255, 0), -1)
cv2.imshow("Center", image)
cv2.waitKey(0)

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
