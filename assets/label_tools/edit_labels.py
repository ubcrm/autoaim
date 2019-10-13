import cv2, os, json

#------------------------- FUNCTION DEFINITIONS -------------------------
def edit_label(label):
    label['x1'] = int(label.pop('X1'))
    label['y1'] = int(label.pop('Y1'))
    label['x2'] = int(label.pop('X2'))
    label['y2'] = int(label.pop('Y2'))
    label['width'] = int(label['width'])
    label['height'] = int(label['height'])
    label['center']['x'] = int(label['center']['x'])
    label['center']['y'] = int(label['center']['y'])


#------------------------- CONSTANTS -------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
LABELS_IN = '/data/image_labels_raw.json'
LABELS_OUT = '/data/image_labels_edited.json'
IMAGE_IN = '/data/images/image-%d.jpg'
IMAGE_OUT = '/data/images/%d.jpg'

IMAGE_CNT = 655
PRINT_TO_TERMINAL = True
CONVERT_IMAGES = False


#------------------------- MAIN BODY -------------------------
with open(DIR + LABELS_IN, 'r') as f_in:
    labels_dict = json.load(f_in)

for i in range(0, IMAGE_CNT):
    if PRINT_TO_TERMINAL:
        print('Processing %d of %d' % (i+1, IMAGE_CNT))

    labels_dict['%d.jpg' % i] = labels_dict.pop('image-%d.jpg' % (i+1))
    labels = labels_dict['%d.jpg' % i]
    for label in labels.values():
        edit_label(label)

    if CONVERT_IMAGES:
        image = cv2.imread(DIR + IMAGE_IN % (i+1))
        cv2.imwrite(DIR + IMAGE_OUT % i, image)

with open(DIR + LABELS_OUT, 'w') as f_out:
    json.dump(labels_dict, f_out, indent=4)

if PRINT_TO_TERMINAL:
    print('Edited labels and images saved.')
