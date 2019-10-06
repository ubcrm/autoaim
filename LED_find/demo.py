from led_manager import *
import json
import os

# current directory path and JSON write path
DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DATA = '/data/demo.json'

# create leds with parameters that specify their bounding rectangles
# id, width, height, angle, (x_center, y_center)
led1 = Led("a", 800, 500, 67, (200, 750))
led2 = Led("b", 200, 100, 0, (350, 340))
led3 = Led("c", 450, 90, 34, (920, 740))
led4 = Led("d", 80, 520, 35, (100, 690))

# create all combinations of leds and indicate the ones that form a panel
# id, list_leds, list_panel_pairs
combs = LedCombs("image_1", [led1, led2, led3, led4], [("a", "c")])

# write all data to a JSON file
with open(DIR + FILE_DATA, 'w') as file:
    json.dump(combs.toDict(), file, indent=2)
