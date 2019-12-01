import cv2
import os
import numpy as np
import math
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from source.common.module import Module


class AssignPanels(Module):
    def __init__(self, parent, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
        # todo: obtain and set frame size here
        self.frame = None

    def process(self, centered_frame):
        """
        :param centered_frame: a square cropped image of the power rune in BGR colorspace
        :return: a list of angles of panels and their states
        """
        self.frame = centered_frame
        frame_gray = cv2.cvtColor(centered_frame, cv2.COLOR_BGR2GRAY)
        _, frame_bw = cv2.threshold(frame_gray, self.properties["lumin_threshold"], 255, cv2.THRESH_BINARY)
        lumins = self.calc_lumins_lines(frame_bw)
        states = self.find_states(lumins)

        if self.properties["mode"] == 'debug':
            self.plot_lumins(lumins, states)
            cv2.imshow('Frame B&W', frame_bw)
            cv2.imshow('Frame BGR', self.frame)
            cv2.waitKey(1)

        return states

    def calc_lumin_square(self, frame_bw, coords_center):
        # todo: move size_frame attribute to predict_target.settings?
        size_square = self.properties["size_square_mask"] * len(frame_bw)
        cnt_pixels = 0
        cnt_whites = 0

        for y in range(round(coords_center[1] - size_square / 2), round(coords_center[1] + size_square / 2)):
            for x in range(round(coords_center[0] - size_square / 2), round(coords_center[0] + size_square / 2)):
                cnt_pixels += 1
                if frame_bw[y][x]:
                    cnt_whites += 1

        return 255 * cnt_whites/cnt_pixels

    def calc_lumins_squares(self, frame_bw):
        # todo: move radius to parent module maybe? depends on how he does it.
        lumins_squares = []
        for angle in range(0, 360, self.properties["angle_increment_mask"]):
            angle *= 3.1415 / 180
            size_frame = len(frame_bw)

            x_center = len(frame_bw) / 2 + self.properties["radius_square_mask"] * size_frame * math.sin(angle)
            y_center = len(frame_bw) / 2 - self.properties["radius_square_mask"] * size_frame * math.cos(angle)
            lumins_squares += [self.calc_lumin_square(frame_bw, (x_center, y_center))]

            if self.properties["mode"] == 'debug':
                self.draw_square((x_center, y_center))

        return lumins_squares

    def calc_lumins_lines(self, frame_bw):
        lumins_lines = []
        for angle in range(0, 360, self.properties["angle_increment_mask"]):
            angle *= 3.1415 / 180
            size_frame = len(frame_bw)
            cnt_pixels = 0
            cnt_whites = 0

            for radius in range(
                    int(self.properties["radius_line_mask_min"] * size_frame),
                    int(self.properties["radius_line_mask_max"] * size_frame)
            ):
                x = round(size_frame / 2 + radius * math.sin(angle))
                y = round(size_frame / 2 - radius * math.cos(angle))
                cnt_pixels += 1
                if frame_bw[y][x]:
                    cnt_whites += 1

                if self.properties["mode"] == 'debug':
                    self.frame[y][x] = tuple(self.properties["color_mask_debug"])
            lumins_lines += [255 * cnt_whites/cnt_pixels]

        return lumins_lines

    def find_peak_angles(self, lumins):
        inc_peak_distance = int(self.properties["angle_peak_distance"] / self.properties["angle_increment_mask"])
        peak_indices, _ = find_peaks(
            lumins[-inc_peak_distance: -1] + lumins + lumins[0: inc_peak_distance],
            height=(self.properties["lumin_peak_min"], 255),
            distance=self.properties["angle_peak_distance"]
        )
        peak_angles = []
        for peak_index in peak_indices:
            peak_angles += [(peak_index-inc_peak_distance+1) % len(lumins) * self.properties["angle_increment_mask"]]

        return peak_angles

    def assign_state(self, lumin):
        # todo: fix the panel state defined by parent issue
        if lumin > self.properties["lumin_peak_border"]:
            return self.properties["panel_states"]["active"]
        elif self.properties["lumin_peak_min"] < lumin <= self.properties["lumin_peak_border"]:
            return self.properties["panel_states"]["activating"]
        else:
            return self.properties["panel_states"]["inactive"]

    def find_states(self, lumins):
        states = {}
        for peak_angle in self.find_peak_angles(lumins):
            states[peak_angle] = self.assign_state(lumins[int(peak_angle/self.properties["angle_increment_mask"])])
        return states

    def plot_lumins(self, lumins, states):
        angles = range(0, 360, self.properties["angle_increment_mask"])
        plt.plot(angles, lumins)
        plt.plot(angles, [self.properties["lumin_peak_min"]] * len(angles), 'red')
        plt.plot(angles, [self.properties["lumin_peak_border"]] * len(angles), 'red')

        for angle, state in states.items():
            if state == self.properties["panel_states"]["active"]:
                marker = 'o'
                label = "Active"
            elif state == self.properties["panel_states"]["activating"]:
                marker = '^'
                label = "Activating"
            else:
                marker = 'x'
                label = "Inactive"
            plt.plot(angle, lumins[int(angle/self.properties["angle_increment_mask"])],
                     marker, mfc='black', mec='black', label=label)

        plt.xlabel('Angle [°]')
        plt.ylabel('Luminosity [0-255]')
        plt.show()

    def draw_square(self, coords_center):
        x_tl, y_tl = coords_center
        size = round(self.properties["size_square_mask"] * len(self.frame))
        points = np.array([
            [round(x_tl - size / 2), round(y_tl - size / 2)],
            [round(x_tl + size / 2), round(y_tl - size / 2)],
            [round(x_tl + size / 2), round(y_tl + size / 2)],
            [round(x_tl - size / 2), round(y_tl + size / 2)]],
            dtype=np.int32
        )
        cv2.polylines(self.frame, [points], True, self.properties["color_mask_debug"], 1)
