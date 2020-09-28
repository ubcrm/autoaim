from autoaim_config import *
from frame_to_target.frame_to_target import frame_to_target
from target_to_coords.target_to_coords import target_to_coords
from predict_coords.predict_coords import predict_coords
from send_coords.send_coords import send_coords
import cv2


def autoaim(source):
    frame_count = 0
    capture = cv2.VideoCapture(source)

    successful, frame = capture.read()
    while successful:
        frame_count += 1
        run_frame(frame)
        successful, frame = capture.read()


def run_frame(frame):
    target = frame_to_target(frame)
    coords = target_to_coords(target)
    coords = predict_coords(coords)
    send_coords.run(coords)
