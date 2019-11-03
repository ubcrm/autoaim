''' RoboMaster Power Rune Vision

This code enables recognition of the 'Activating' target panel on the power
rune in the 2019 RoboMaster challenge 'Standard Racing & Smart Firing' to be
shot. Both a one-time recognition (image) and a continuous recognition (video)
option are available.

Running this code requires the following packages to be installed:
    - numpy: NumPy, fundamental scientific computing package
    - scipy: SciPy, scientific computing package
    - cv2: OpenCV, computer vision and machine learning package
    - matplotlib: 2D plotting package

The file "settings.py" containing default values and constants should be
placed in the same directory as this file.
'''

from math import sin, cos
import cv2, time
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from settings import *




class Panels():
    def __init__(self, first_angle, first_lumin, rot_dir):
        self.time_init = time.time()
        self.angles = [round(first_angle)]
        self.lumins = [round(first_lumin)]
        self.states = [STATE_ACTIVATING]
        self.activated = False
        self.rot_speed = rot_speed

        for i in range(1, CNT_PANELS):
            self.angles += [round(first_angle + i * ANGLE_SEP) % ANGLE_MAX]
            self.lumins += [0]
            self.states += [STATE_INACTIVE]

    def angle_activating(self):
        for index in range(CNT_PANELS):
            if self.states[index] == STATE_ACTIVATING:
                return self.angles[index]
        return None

    def angles_inactive(self):
        angles = []
        for index in range(CNT_PANELS):
            if self.states[index] == STATE_INACTIVE:
                angles += [self.angles[index]]
        return angles

    def calibrate(self, angle):
        # calibrate given an angle close to a lit panel
        pass





class Capture():
    def __init__(self, src, src_dims, crop_cntr, crop_dim, src_clr):
        self.src = src
        self.src_dims = src_dims
        self.src_clr = src_clr

        self.frame = None
        self.frame_clr = None
        self.crop_dim = crop_dim
        self.crop_tl = (round(crop_cntr[0] - crop_dim/2), round(crop_cntr[1] - crop_dim/2))
        self.crop_br = (round(crop_cntr[0] + crop_dim/2), round(crop_cntr[1] + crop_dim/2))

    def set_crop_cntr_fm(self, crop_cntr_fm):
        scl_factor = FRAME_DIM / self.crop_dim
        crop_cntr_dx = round((crop_cntr_fm[0] - FRAME_DIM/2) / scl_factor)
        crop_cntr_dy = round((crop_cntr_fm[1] - FRAME_DIM/2) / scl_factor)
        self.crop_tl = (self.crop_tl[0] + crop_cntr_dx, self.crop_tl[1] + crop_cntr_dy)
        self.crop_br = (self.crop_br[0] + crop_cntr_dx, self.crop_br[1] + crop_cntr_dy)

    def update_bw(self):
        read, self.frame = self.src.read()
        self.frame_clr = self.src_clr
        if read:
            self.crop_and_resize()
            self.convert_color('BW')
        return read

    def crop_and_resize(self):
        self.frame = self.frame[self.crop_tl[1]: self.crop_br[1], self.crop_tl[0]: self.crop_br[0]]
        self.frame = cv2.resize(self.frame, (FRAME_DIM, FRAME_DIM))

    def convert_color(self, clr):
        if self.frame_clr != clr:
            if clr == 'BW':
                self.convert_color('GRAY')
                _, self.frame = cv2.threshold(self.frame, LUM_THRESH_BW,
                                                LUM_MAX, cv2.THRESH_BINARY)
            elif self.frame_clr == 'BW':
                conversion = eval('cv2.COLOR_' + 'GRAY' + '2' + clr)
                self.frame = cv2.cvtColor(self.frame, conversion)
            else:
                conversion = eval('cv2.COLOR_' + self.frame_clr + '2' + clr)
                self.frame = cv2.cvtColor(self.frame, conversion)
            self.frame_clr = clr

    def draw_circ(self, cntr, rad, clr, thickness=2):
        cv2.circle(self.frame, (round(cntr[0]), round(cntr[1])),
                    round(rad), clr, thickness)

    def draw_sqr(self, coords_cntr, dim, clr, thickness=1):
        x_tl, y_tl = coords_cntr
        points = np.array([[round(x_tl-dim/2), round(y_tl-dim/2)], [round(x_tl+dim/2), round(y_tl-dim/2)], [round(x_tl+dim/2), round(y_tl+dim/2)], [round(x_tl-dim/2), round(y_tl+dim/2)]], dtype=np.int32)
        cv2.polylines(self.frame, [points], True, clr, thickness=thickness)

    def show(self, title, delay_ms):
        cv2.imshow(title, self.frame)
        cv2.waitKey(delay_ms)





class WheelVision():
    def __init__(self, src, src_dims, crop_cntr, crop_dims, src_clr='BGR'):
        self.cap = Capture(src, src_dims, crop_cntr, crop_dims, src_clr)
        self.panels = None
        self.rotDir = None  # ±1 indicates CW/CCW wheel rotation

        # TODO: REMOVE THESE OPTIONS IN THE FINAL VERSION OF THE CODE
        self.show_disp = None
        self.show_plot = None
        self.timeStart = None
        self.timeSetup = None
        self.timeStop = None
        self.cntFrames = 0

    # ---------- HANDLING DIFFERENT MODES OF EXECUTION ---------- #
    def run(self, mode_calib=False, show_disp=True, show_plot=False, cont_recntr=False):
        self.time_start = time.time()
        self.show_disp = show_disp
        self.show_plot = show_plot

        if not cont_recntr and self.cap.update_bw():
            self.recntr_cap()
        self.init_panels()
        self.time_setup = time.time()

        if mode_calib:
            mode_func = self.calib
        else:
            mode_func = self.bare
        while self.cap.update_bw():
            if cont_recntr and (self.cnt_frames % WHEEL_RECNTR_FREQ == 0):
                self.recntr_cap()
            mode_func()
            self.cnt_frames += 1

        self.time_stop = time.time()
        self.print_time()


    def calib(self):
        self.cap.convert_color('BGR')
        self.cap.draw_circ(FRAME_CNTR, MASK_RAD, GREEN, MASK_DIM)
        self.cap.draw_circ(FRAME_CNTR, 2, RED, -1)
        self.cap.draw_circ(FRAME_CNTR, TARGET_RAD, RED)
        self.cap.draw_circ(FRAME_CNTR, WHEEL_RAD, GREEN)
        self.cap.draw_sqr((FRAME_CNTR[0] - CNTR_OFFSET[0], FRAME_CNTR[1] - CNTR_OFFSET[1]), R_DIM, GREEN)
        self.cap.draw_sqr((FRAME_CNTR[0] - CNTR_OFFSET[0], FRAME_CNTR[1] - CNTR_OFFSET[1]), CNTR_DIM, GREEN)
        self.cap.show('Calibration', 10)

    def bare(self):

        if self.show_disp:
            self.cap.convert_color('BGR')
            if self.wheel_status == STAGE_SHOOT:
                angle_target = self.panel_activating_angle * DEG_TO_RAD
                coords_target = (round(WHEEL_CNTR[0] + TARGET_RAD * sin(angle_target)), round(WHEEL_CNTR[1] - TARGET_RAD * cos(angle_target)))
                cv2.circle(self.frame, coords_target, 5, RED, -1)
            cv2.imshow('Bare', self.frame)
            cv2.waitKey(50)

    # ---------- FOR DEBUGGING AND OPTIMIZATION PURPOSES ---------- #
    def print_time(self):
        setup_time = self.time_setup - self.time_start
        total_time = self.time_stop - self.time_start
        print('Frame Processing Rate: {:.3} fps'
              .format(self.cnt_frames / (total_time - setup_time)))
        print('Setup Time: {:.3} s'.format(setup_time))
        print('Total Execution Time: {:.3} s'.format(total_time))

    def plot(self, lumin_vals):
        plt.plot(ANGLE_VALS, lumin_vals)
        plt.plot(ANGLE_VALS, [LUM_THRESH_LOW] * INC_ANGLE_MAX, 'red')
        plt.plot(ANGLE_VALS, [LUM_THRESH_HIGH] * INC_ANGLE_MAX, 'red')

        for angle, lumin, state in zip(self.panels.angles, self.panels.lumins, self.panels.states):
            if state == STATE_ACTIVE:
                points_active, = plt.plot(angle, lumin, 's', mfc='black',  mec='black', label='Active')
            elif state == STATE_ACTIVATING:
                points_activating, = plt.plot(angle, lumin, '^', mfc='black', mec='black', label='Activating')
            elif state == STATE_INACTIVE:
                points_inactive, = plt.plot(angle, lumin, 'o', mfc='black', mec='black', label='Inactive')

        handles = []
        if STATE_ACTIVE in self.panels.states:
            handles += [points_active]
        if STATE_ACTIVATING in self.panels.states:
            handles += [points_activating]
        if STATE_INACTIVE in self.panels.states:
            handles += [points_inactive]

        plt.xlabel('Angle [°]')
        plt.ylabel('Luminosity [0-255]')
        plt.legend(handles=handles)
        plt.show()

    # ---------- INITIAL SETUP AND PREPARATION ---------- #
    def recntr_cap(self):
        start_coords = (round(FRAME_DIM/2 - CNTR_DIM/2 - CNTR_OFFSET[0]), round(FRAME_DIM/2 - CNTR_DIM/2 - CNTR_OFFSET[1]))
        end_coords = (round(FRAME_DIM/2 + CNTR_DIM/2 - R_DIM - CNTR_OFFSET[0]), round(FRAME_DIM/2 + CNTR_DIM/2 - R_DIM - CNTR_OFFSET[1]))
        max_lumin = 0

        for y_tl in range(start_coords[1], end_coords[1], WHEEL_R_INC):
            for x_tl in range(start_coords[0], end_coords[0], WHEEL_R_INC):
                new_lumin = self.calc_sqr_lumin((x_tl, y_tl), R_DIM)
                if max_lumin < new_lumin:
                    max_lumin = new_lumin
                    wheel_cntr = (x_tl + R_DIM/2 + CNTR_OFFSET[0], y_tl + R_DIM/2 + CNTR_OFFSET[1])
        self.cap.set_crop_cntr_fm(wheel_cntr)

    def init_panels(self):
        while self.cap.update_bw() and self.panels is None:
            lumin_vals = []
            for angle in ANGLE_VALS:
                lumin_vals += [self.calc_lumin_angle(angle)]
            self.find_peaks(lumin_vals)
            peaks = self.calc_peaks()
            if len(peaks) == 1:
                index = int(peaks[0])
                self.panels = Panels(index * ANGLE_INC, lumin_vals[index], self.calc_rot_dir(index * ANGLE_INC))

    def calc_rot_dir(self, angle_activating):
        angle_diff = angle_prev = 0
        for i in range(WHEEL_rot_dir_CNT + 1):
            lumin_vals = []
            for angle in range(angle_activating - ANGLE_ESTIMATE_DIST, angle_activating + ANGLE_ESTIMATE_DIST, ANGLE_INC):
                lumin_vals += [self.calc_lumin_angle(angle)]

            angle_new = self.find_peaks(lumin_vals)[0]
            if i != 0:
                angle_diff += self.calc_diff_angle(angle_new, angle_prev, ANGLE_ESTIMATE_DIST, 2 * ANGLE_ESTIMATE_DIST)
            angle_prev = angle_new
        self.rot_dir = -1

    def calc_peaks(self, angle, range):
        pass


    def calc_diff_angle(self, angle_new, angle_prev, proximity, range):
        diff = angle_new - angle_prev
        if abs(diff) <= proximity:
            pass
        elif diff <= -range:
            diff
        return

    # ---------- CORE ALGORITHM EXECUTION ---------- #
    def calc_sqr_lumin(self, coords_tl, dim):
        cnt_pixels = 0
        cnt_whites = 0
        for y in range(round(coords_tl[1]), round(coords_tl[1] + dim)):
            for x in range(round(coords_tl[0]), round(coords_tl[0] + dim)):
                cnt_pixels += 1
                if self.cap.frame[y][x]:
                    cnt_whites += 1
        return round(LUM_MAX * cnt_whites / cnt_pixels)

    def calc_lumin_angle(self, angle):
        angle *= DEG_TO_RAD
        x_tl = FRAME_DIM/2 + MASK_RAD * sin(angle) - MASK_DIM/2
        y_tl = FRAME_DIM/2 - MASK_RAD * cos(angle) - MASK_DIM/2
        return self.calc_sqr_lumin((x_tl, y_tl), MASK_DIM)

    def find_peaks(self, vals):
        peak_indices, _ = find_peaks(vals + vals[0:1], height=(LUM_THRESH_LOW, LUM_MAX))
        peaks = []
        for peak_index in peak_indices:
            peaks += [peak_index % len(vals)]
        return peaks
