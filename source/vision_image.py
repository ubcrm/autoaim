from resource import bit_mask, detect_shape, match_leds, find_center
from tensorflow_pipeline import tensorflow_pipeline
from imutils.video import FPS
import tensorflow as tf
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())


# Load model from disk
# print('[INFO] loading model from disk...')
# model_path = '../assets/tensorflow_pipeline/model/saved_model.pb'
# settings_json = '../assets/tensorflow_pipeline/training_pipeline_settings_unix.json'
# Tf = tensorflow_pipeline.TensorflowPipeline(settings_json)
# model = Tf.load_model(model_path)

image = cv2.imread(args['image'])

# start frames per second counter
fps = FPS().start()

# 1. Preprocess image/frame
frame = imutils.resize(image, width=400)
cv2.imshow('image',frame)
cv2.waitKey(0)

# 2. Mask LEDs
mask = bit_mask.find_led_from_image(frame)
print(mask)

# 3. Locate LEDs
rectangles = detect_shape.find_rectangles(mask)
print(rectangles)

# 4. Match pairing LEDs
nn_input = detect_shape.reformat_cv_rectangle(rectangles)
print(nn_input)
#prediction = tf.keras.predict(rectangles)

# 5. Locate Target Center Coordinates

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
