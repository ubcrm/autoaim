from itertools import combinations


class Led:
    def __init__(self, id, center, dims, angle):
        self.id = str(id)
        self.width = int(dims[0])
        self.height = int(dims[1])
        self.center = (int(center[0]), int(center[1]))
        self.angle = int(angle)

    def to_dict(self):
        data = {
            "width": self.width,
            "height": self.height,
            "angle": self.angle,
            "x_center": self.center[0],
            "y_center": self.center[1]
        }
        return data


class LedPair:
    def __init__(self, id, led1, led2, is_panel):
        self.id = str(id)
        self.led1 = led1
        self.led2 = led2
        self.isPanel = is_panel

    def to_dict(self):
        data = {
            "led1": self.led1.to_dict(),
            "led2": self.led2.to_dict(),
            "isPanel": self.isPanel
        }
        return data


class LedCombs:
    def __init__(self, id, leds, panels):
        self.id = str(id)
        self.leds = leds
        self.panels = [(str(pair[0]), str(pair[1])) for pair in panels]
        self.ledPairs = []
        self.generate_pairs()

    def generate_pairs(self):
        combs = combinations(self.leds, 2)
        for i, (led1, led2) in enumerate(combs):
            isPanel = int((led1.id, led2.id) in self.panels or (led2.id, led1.id) in self.panels)
            self.ledPairs += [LedPair(str(i), led1, led2, isPanel)]

    def to_dict(self):
        data = {}
        for pair in self.ledPairs:
            data[pair.id] = pair.to_dict()
        return data
