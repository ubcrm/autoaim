from resource import bit_mask, detect_shape, match_leds, find_center
from tensorflow_pipeline import tensorflow_pipeline as tp
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
model = tp.TensorflowPipeline.load_model(model_path)

print('\n'+'[INFO] loading image from disk...')
image = cv2.imread(args['image'])

# start frames per second counter
print('[INFO] starting frames per second counter...')
fps = FPS().start()

# 1. Preprocess image/frame
#frame = imutils.resize(image, width=400)
cv2.imshow('image', image)
cv2.waitKey(0)

# 2. Mask LEDs
mask = bit_mask.find_led_from_image(image)
print('\n'+'[INFO] mask:'+'\n')
print(mask)
cv2.imshow('mask', mask)
cv2.waitKey(0)

# 3. Locate LEDs
rectangles = detect_shape.find_rectangles(mask)
print('\n'+'[INFO] rectangles:'+'\n')
print(rectangles)

# 4. Match pairing LEDs
led = []
inputs = []

for r in rectangles:
	reformat = detect_shape.reformat_cv_rectangle(r)
	led.append(reformat)

for j in range(len(led)-1):
	leds = (led[j], led[j+1])
	video_dims = (1920, 1080)
	res = tp.TensorflowPipeline.create_nn_input(leds, video_dims)
	inputs.append(res)

print('\n'+'[INFO] inputs:'+'\n')
print(inputs)

data_x = np.array(inputs)
print('\n'+'[INFO] inputs as np array:'+'\n')
print(data_x)
print('\n')

confidences = []

for x in data_x:
	nn_input = np.asarray([data_x[0], data_x[1]])
	prediction = tp.TensorflowPipeline.model_predict(model, nn_input)
	confidences.append(prediction)

print('\n'+'[INFO] confidences:')
print(confidences)

# 5. Locate Target Center Coordinates

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
