import cv2
from itertools import permutations


class Led():
    def __init__(self, id, width, height, angle, center):
        self.id = str(id)
        self.width = width
        self.height = height
        self.angle = angle
        self.center = center

    def toDict(self):
        cntr = {
            "x": self.center[0],
            "y": self.center[1]
            }
        data = {
            "width": self.width,
            "height": self.height,
            "angle": self.angle,
            "center": cntr
            }
        return data


class LedPair():
    def __init__(self, id, led1, led2, isPanel):
        self.id = str(id)
        self.led1 = led1
        self.led2 = led2
        self.isPanel = isPanel

    def toDict(self):
        data = {
            "led1": self.led1.toDict(),
            "led2": self.led2.toDict(),
            "isPanel": self.isPanel
            }
        return data


class LedPerms():
    def __init__(self, file_name, leds, panels):
        self.file_name = file_name
        self.leds = leds
        self.panels = panels
        self.ledPairs = []
        self.generatePairs()

    def generatePairs(self):
        perms = permutations(self.leds, 2)
        for i, (led1, led2) in enumerate(perms):
            isPanel = ((led1.id, led2.id) in self.panels or (led2.id, led1.id) in self.panels)
            self.ledPairs += [LedPair(str(i), led1, led2, isPanel)]

    def toDict(self):
        data = {}
        for pair in self.ledPairs:
            data[pair.id] = pair.toDict()
        return data
