"""
Will be refactored into the openCV module
"""

import cv2
from source.tensorflow_pipeline.tensorflow_pipeline import get_json_from_file


def get_leds_from_frame(frame):
    return False  # will use ../LED_find


def run_webcam():
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        frame_leds = get_leds_from_frame(img)
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


if __name__ == "__main__":
    settings = get_json_from_file("training_pipeline_settings.json")
    mode = settings["mode"]
    if mode == "webcam":
        run_webcam()
