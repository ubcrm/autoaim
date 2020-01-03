from source.module import Module
from pathlib import Path
import os
import cv2
from .panel_finder.panel_finder import PanelFinder
import time


class PanelAimer(Module):
    def __init__(self, parent, **config):
        self.wd = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.wd, parent, config)

        self.panel_finder = PanelFinder(self)

    def process(self, feed_option):
        """
        Run aim assist, sending target aim coordinates to gimbal
        :param feed_option: integer indicating camera or path of video file
        """
        time_start = int(time.time())
        feed = cv2.VideoCapture(feed_option)

        ret, frame = feed.read()
        while ret:
            self.panel_finder.process(frame)
            ret, frame = feed.read()

            if self.config['mode'] != 'compete':
                if self.config['mode'] == 'debug':
                    key_pressed = cv2.waitKey(0)
                else:
                    key_pressed = cv2.waitKey(self.config['delay'])
                if key_pressed == ord(self.config['key_quit']):
                    break

        average_fps = self.panel_finder.frame_count / (time.time() - time_start)
        print('Time per frame: %dms\nFrames per second: %d' % (1e3 / max(1e-3, average_fps), average_fps))
        feed.release()
        cv2.destroyAllWindows()
