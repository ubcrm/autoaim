import autoaim_config as CONFIG
from find_target.find_target import FindTarget
from map_coords.map_coords import MapCoords
from send_coords.send_coords import SendCoords
import cv2


class Autoaim:
    def __init__(self):
        self.find_target = FindTarget()
        self.map_coords = MapCoords()
        self.send_coords = SendCoords()
        self.count_frame = 0

    def run(self, capture_device):
        feed = cv2.VideoCapture(capture_device)

        while True:
            _, frame = feed.read()
            self.count_frame += 1

            target = self.find_target.run(frame)
            coords = self.map_coords.run(target)
            self.send_coords.run(coords)
