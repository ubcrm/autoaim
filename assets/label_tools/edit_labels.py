import cv2, os, json


DIR = os.path.dirname(os.path.abspath(__file__))
LABELS_IN = '/input/labels.json'
LABELS_OUT = '/data/image_labels.json'
IMAGE_IN = '/input/image-%d.jpg'
IMAGE_OUT = '/data/images/%d.jpg'

IMAGE_CNT = 655
PRINT_TO_TERMINAL = True


def edit_label(label):
    label['x1'] = int(label.pop('X1'))
    label['y1'] = int(label.pop('Y1'))
    label['x2'] = int(label.pop('X2'))
    label['y2'] = int(label.pop('Y2'))
    label['width'] = int(label['width'])
    label['height'] = int(label['height'])
    label['center']['x'] = int(label['center']['x'])
    label['center']['y'] = int(label['center']['y'])


with open(DIR + LABELS_IN, 'r') as f_in:
    labels_dict = json.load(f_in)

for i in range(0, IMAGE_CNT):
    if PRINT_TO_TERMINAL:
        print('Processing %d.jpg/%d.jpg' % (i, IMAGE_CNT - 1))

    labels_dict['%d.jpg' % i] = labels_dict.pop('image-%d.jpg' % (i+1))
    labels = labels_dict['%d.jpg' % i]

    for label in labels.values():
        edit_label(label)

    image = cv2.imread(DIR + IMAGE_IN % (i+1))
    cv2.imwrite(DIR + IMAGE_OUT % i, image)

with open(DIR + LABELS_OUT, 'w') as f_out:
    json.dump(labels_dict, f_out, indent=4)

if PRINT_TO_TERMINAL:
    print('New labels and images saved successfully.')
