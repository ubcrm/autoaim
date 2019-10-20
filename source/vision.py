from source.resource import bit_mask, detect_shape, match_leds, find_center
from source.tensorflow_pipeline import tensorflow_pipeline
import tensorflow as tf
import argparse
import imutils
import cv2

# Load model from disk
print('[INFO] loading model from disk...')

# model_path = '../assets/tensorflow_pipeline/model/saved_model.pb'

# settings_json = '../assets/tensorflow_pipeline/training_pipeline_settings_unix.json'

# Tf = tensorflow_pipeline.TensorflowPipeline(settings_json)

# model = Tf.load_model(model_path)

image_path = '~/code/robomaster/datasets/RoboMasterLabelledImagesSet1/image-550.jpg'
image = cv2.imread(image_path)
cv2.imshow('image', image)
cv2.waitKey(0)

# initialize the video stream, allow the camera sensor to warmup
# print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# time.sleep(1.0)

# print('[INFO] beginning detector')

# start frames per second counter
# fps = FPS().start()

# while True:
# frame = vs.read()

# 1. Preprocess image/frame
frame = imutils.resize(image, width=400)
cv2.imshow('image', frame)

# 2. Mask LEDs
mask = over_exposed_threshold(frame)
print(mask)

# 3. Locate LEDs
rectangles = find_rectangles(mask)
print(rectangles)

# 4. Match pairing LEDs
# prediction = tf.keras.predict(rectangles)

# print(prediction)

# 5. Locate Target Center Coordinates
