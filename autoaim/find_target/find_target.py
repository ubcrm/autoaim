from crop_robot import CropRobot
from mask import Mask
from find_leds import FindLeds
from match_leds import MatchLeds
from select_panel import SelectPanel
from predict_target import PredictTarget
from visualize import Visualize


class FindTarget:
    def __init__(self):
        self.crop_robot = CropRobot()
        self.mask = Mask()
        self.find_leds = FindLeds()
        self.match_leds = MatchLeds()
        self.select_panel = SelectPanel()
        self.predict_target = PredictTarget()
        self.visualize = Visualize()

    def run(self, frame):
        roi = self.crop_robot.run(frame)
        mask = self.mask.run(roi)
        leds, not_leds = self.find_leds.run(mask)
        panels, not_panels = self.match_leds.run(leds)
        panel = self.select_panel.run(panels)
        target = self.predict_target.run(panel)

        if('mode'] != 'compete':
            self.visualize.run(frame, roi, leds, not_leds, panels, not_panels, panel, target)
            if('mode'] == 'debug':
                cv2.imshow('title_roi'], roi)
                cv2.im(['title_mask'], mask)
            cv2.imshow('title_frame'], frame)

        return target
