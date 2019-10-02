from led_manager import *
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))


led1 = Led("a", 800, 500, 67, (200, 750))
led2 = Led("b", 200, 100, 0, (350, 340))
led3 = Led("c", 450, 90, 34, (920, 740))
led4 = Led("d", 80, 520, 35, (100, 690))

perms = LedPerms("image_1.jpg", [led1, led2, led3, led4], [("a", "c")])

with open(DIR + '/data/demo.json', 'w') as file:
    json.dump(perms.toDict(), file, indent=2)
