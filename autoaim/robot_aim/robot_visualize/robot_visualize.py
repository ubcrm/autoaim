from assets.module import Module
from pathlib import Path
import os
import cv2
import numpy as np
import time


class RobotVisualize(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)
        if self.config['save']['do']:
            self.video_write = cv2.VideoWriter(self.config['save']['name'] % time.time(),
                                               cv2.VideoWriter_fourcc(*'mp4v'), self.config['save']['fps'],
                                               tuple(self.parent.config['view']['dims']))

    def process(self, frame, roi, leds, not_leds, panels, not_panels, panel, target):
        """
        Display and log led/target info for debugging.
        """
        if self.parent.config['mode'] == 'debug':
            self.draw_bounding_rects(frame, leds + not_leds if self.config['draw']['not_led'] else leds)
            self.draw_led_pairs(frame, panels + not_panels if self.config['draw']['not_panel'] else panels)
            self.log(self.parent.parent.frame_count, leds + not_leds, panels + not_panels)

        self.draw_panels(frame, panels)
        cv2.circle(frame, target, self.config['target_radius'], self.config['colors']['target'], -1)
        cv2.line(frame, panel.center, target, self.config['colors']['target'], self.config['line_thickness'])

        if self.config['save']['do']:
            self.video_write.write(frame)

    def draw_bounding_rects(self, frame, leds):
        for led in leds:
            tag = 'led' if led.is_led else 'not_led'
            cv2.polylines(frame, [np.array(led.corners)], True,
                          self.config['colors'][tag], self.config['line_thickness'])
            cv2.putText(frame, led.label, sum_tuples(led.center, self.config['text']['position']['led_label']),
                        self.config['text']['font'], self.config['text']['scale_label'], self.config['colors'][tag])

    def draw_led_pairs(self, frame, panels):
        for panel in panels:
            tag = 'targets' if panel.is_panel else 'not_panel'
            cv2.polylines(frame, [np.array(panel.corners)], True,
                          self.config['colors'][tag], self.config['line_thickness'])
            cv2.putText(frame, panel.label, sum_tuples(panel.center, self.config['text']['position']['panel_label']),
                        self.config['text']['font'], self.config['text']['scale_label'], self.config['colors'][tag])

    def draw_panels(self, frame, panels):
        for panel in panels:
            cv2.circle(frame, panel.center, self.config['target_radius'], self.config['colors']['targets'], -1)
            cv2.putText(frame, '%.2f' % panel.distance,
                        sum_tuples(panel.center, self.config['text']['position']['distance']),
                        self.config['text']['font'], self.config['text']['scale'],
                        self.config['colors']['text'])

    def log(self, frame_count, leds, panels):
        print('{0} Frame {1} {0}'.format('-' * self.config['text']['dash_count'], frame_count))
        for led in sorted(leds, key=lambda l: l.label):
            led.log()
        for panel in sorted(panels, key=lambda p: p.label):
            panel.log()


def sum_tuples(tuple1, tuple2):
    return tuple(sum(value_pair) for value_pair in zip(tuple1, tuple2))
