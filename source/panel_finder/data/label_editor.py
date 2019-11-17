from source.instance import get_json_from_file
from source.common.module import Module
from pathlib import Path
import cv2
import os


class LabelEditor(Module):
    def __init__(self, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, state=state)

    def edit_label(self, l):
        """
        Edits the label passed by Vala's software
        :param out: label for leds
        """
        out = l
        out['x1'] = int(out.pop('X1'))
        out['y1'] = int(out.pop('Y1'))
        out['x2'] = int(out.pop('X2'))
        out['y2'] = int(out.pop('Y2'))
        out['width'] = int(out['width'])
        out['height'] = int(out['height'])
        out['center']['x'] = int(out['center']['x'])
        out['center']['y'] = int(out['center']['y'])
        return out

    def edit_labels(self, labels):
        c = self.properties["image_count"]
        should_log = self.properties["logging"]
        should_convert = self.properties["convert_images"]
        for i in range(0, c):
            if should_log:
                print('Processing %d of %d' % (i + 1, c))

            labels['%d.jpg' % i] = labels.pop('image-%d.jpg' % (i + 1))
            labels = labels['%d.jpg' % i]
            for label in labels.values():
                self.edit_label(label)

            if should_convert:
                image = cv2.imread(self.properties["image_in"] % (i + 1))
                cv2.imwrite(self.properties["image_out"] % i, image)

    def process(self, json=None):
        if json is None:
            labels = get_json_from_file(self.properties["labels_in"])
        else:
            labels = get_json_from_file(json)
        return self.edit_labels(labels)
