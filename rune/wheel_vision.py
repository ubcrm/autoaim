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
import time
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import cv2
from settings import *


class WheelVision():

    class Panels():
        def __init__(self, firstAngle, firstLumin, rotDir):
            self.timeInit = time.time()
            self.angles = [round(firstAngle)]
            self.lumins = [round(firstLumin)]
            self.states = [STATE_ACTIVATING]
            self.activated = False
            self.rotDir = rotDir

            for i in range(1, CNT_PANELS):
                self.angles += [round(firstAngle + i * ANGLE_SEP) % ANGLE_MAX]
                self.lumins += [0]
                self.states += [STATE_INACTIVE]

        def angleActivating(self):
            for index in range(CNT_PANELS):
                if self.states[index] == STATE_ACTIVATING:
                    return self.angles[index]
            return None

        def anglesInactive(self):
            angles = []
            for index in range(CNT_PANELS):
                if self.states[index] == STATE_INACTIVE:
                    angles += [self.angles[index]]
            return angles

        def calibrate(self, angle):
            # calibrate given an angle close to a lit panel
            pass

    class Capture():
        def __init__(self, src, srcDims, srcClr, cropCntr, cropDim):
            self.src = src
            self.srcDims = srcDims
            self.srcClr = srcClr

            self.frame = None
            self.frameClr = None
            self.cropDim = cropDim
            self.cropTL = (round(cropCntr[0] - cropDim/2),
                           round(cropCntr[1] - cropDim/2))
            self.cropBR = (round(cropCntr[0] + cropDim/2),
                           round(cropCntr[1] + cropDim/2))

        def setCropCntrFm(self, cropCntrFm):
            sclFactor = FRAME_DIM / self.cropDim
            cropCntrDx = round((cropCntrFm[0] - FRAME_DIM/2) / sclFactor)
            cropCntrDy = round((cropCntrFm[1] - FRAME_DIM/2) / sclFactor)
            self.cropTL = (self.cropTL[0] + cropCntrDx,
                           self.cropTL[1] + cropCntrDy)
            self.cropBR = (self.cropBR[0] + cropCntrDx,
                           self.cropBR[1] + cropCntrDy)

        def updateBW(self):
            read, self.frame = self.src.read()
            self.frameClr = self.srcClr
            if read:
                self.cropAndResize()
                self.convertColor('BW')
            return read

        def cropAndResize(self):
            self.frame = self.frame[self.cropTL[1]: self.cropBR[1],
                                    self.cropTL[0]: self.cropBR[0]]
            self.frame = cv2.resize(self.frame, (FRAME_DIM, FRAME_DIM))

        def convertColor(self, clr):
            if self.frameClr != clr:
                if clr == 'BW':
                    self.convertColor('GRAY')
                    _, self.frame = cv2.threshold(self.frame, LUM_THRESH_BW,
                                                  LUM_MAX, cv2.THRESH_BINARY)
                elif self.frameClr == 'BW':
                    conversion = eval('cv2.COLOR_' + 'GRAY' + '2' + clr)
                    self.frame = cv2.cvtColor(self.frame, conversion)
                else:
                    conversion = eval('cv2.COLOR_' + self.frameClr + '2' + clr)
                    self.frame = cv2.cvtColor(self.frame, conversion)
                self.frameClr = clr

        def drawCirc(self, cntr, rad, clr, thickness=2):
            cv2.circle(self.frame, (round(cntr[0]), round(cntr[1])),
                       round(rad), clr, thickness)

        def drawSqr(self, coordsCntr, dim, clr, thickness=1):
            xTL, yTL = coordsCntr
            points = np.array([[round(xTL-dim/2), round(yTL-dim/2)],
                               [round(xTL+dim/2), round(yTL-dim/2)],
                               [round(xTL+dim/2), round(yTL+dim/2)],
                               [round(xTL-dim/2), round(yTL+dim/2)]],
                              dtype=np.int32)
            cv2.polylines(self.frame, [points], True, clr, thickness=thickness)

        def show(self, title, delayMs):
            cv2.imshow(title, self.frame)
            cv2.waitKey(delayMs)

    def __init__(self, src, srcDims, srcClr, cropCntr, cropDim):
        self.cap = self.Capture(src, srcDims, srcClr, cropCntr, cropDim)
        self.panels = None
        self.rotDir = None  # ±1 indicates CW/CCW wheel rotation

        # TODO: REMOVE THESE OPTIONS IN THE FINAL VERSION OF THE CODE
        self.showDisp = None
        self.showPlot = None
        self.timeStart = None
        self.timeSetup = None
        self.timeStop = None
        self.cntFrames = 0

    # ---------- HANDLING DIFFERENT MODES OF EXECUTION ---------- #
    def run(self, modeCalib=False, showDisp=True, showPlot=False,
            contRecntr=False):
        self.timeStart = time.time()
        self.showDisp = showDisp
        self.showPlot = showPlot

        if not contRecntr and self.cap.updateBW():
            self.recntrCap()
        self.initPanels()
        self.timeSetup = time.time()

        if modeCalib:
            modeFunc = self.calib
        else:
            modeFunc = self.bare
        while self.cap.updateBW():
            if contRecntr and (self.cntFrames % WHEEL_RECNTR_FREQ == 0):
                self.recntrCap()
            modeFunc()
            self.cntFrames += 1

        self.timeStop = time.time()
        self.printTime()

    def calib(self):
        self.cap.convertColor('BGR')
        self.cap.drawCirc(FRAME_CNTR, MASK_RAD, GREEN, MASK_DIM)
        self.cap.drawCirc(FRAME_CNTR, 2, RED, -1)
        self.cap.drawCirc(FRAME_CNTR, TARGET_RAD, RED)
        self.cap.drawCirc(FRAME_CNTR, WHEEL_RAD, GREEN)
        self.cap.drawSqr((FRAME_CNTR[0] - CNTR_OFFSET[0],
                          FRAME_CNTR[1] - CNTR_OFFSET[1]), R_DIM, GREEN)
        self.cap.drawSqr((FRAME_CNTR[0] - CNTR_OFFSET[0],
                          FRAME_CNTR[1] - CNTR_OFFSET[1]), CNTR_DIM, GREEN)
        self.cap.show('Calibration', 10)

    def bare(self):

        if self.showDisp:
            self.cap.convertColor('BGR')
            if self.wheelStatus == STAGE_SHOOT:
                angleTarget = self.panelActivatingAngle * DEG_TO_RAD
                coordsTarget = (round(WHEEL_CNTR[0] + TARGET_RAD * sin(angleTarget)),
                                round(WHEEL_CNTR[1] - TARGET_RAD * cos(angleTarget)))
                cv2.circle(self.frame, coordsTarget, 5, RED, -1)
            cv2.imshow('Bare', self.frame)
            cv2.waitKey(50)

    # ---------- FOR DEBUGGING AND OPTIMIZATION PURPOSES ---------- #
    def printTime(self):
        setupTime = self.timeSetup - self.timeStart
        totalTime = self.timeStop - self.timeStart
        print('Frame Processing Rate: {:.3} fps'
              .format(self.cntFrames / (totalTime - setupTime)))
        print('Setup Time: {:.3} s'.format(setupTime))
        print('Total Execution Time: {:.3} s'.format(totalTime))

    def plot(self, luminVals):
        plt.plot(ANGLE_VALS, luminVals)
        plt.plot(ANGLE_VALS, [LUM_THRESH_LOW] * INC_ANGLE_MAX, 'red')
        plt.plot(ANGLE_VALS, [LUM_THRESH_HIGH] * INC_ANGLE_MAX, 'red')

        for angle, lumin, state in zip(self.panels.angles, self.panels.lumins,
                                       self.panels.states):
            if state == STATE_ACTIVE:
                pointsActive, = plt.plot(angle, lumin, 's', mfc='black',
                                         mec='black', label='Active')
            elif state == STATE_ACTIVATING:
                pointsActivating, = plt.plot(angle, lumin, '^', mfc='black',
                                             mec='black', label='Activating')
            elif state == STATE_INACTIVE:
                pointsInactive, = plt.plot(angle, lumin, 'o', mfc='black',
                                           mec='black', label='Inactive')

        handles = []
        if STATE_ACTIVE in self.panels.states:
            handles += [pointsActive]
        if STATE_ACTIVATING in self.panels.states:
            handles += [pointsActivating]
        if STATE_INACTIVE in self.panels.states:
            handles += [pointsInactive]

        plt.xlabel('Angle [°]')
        plt.ylabel('Luminosity [0-255]')
        plt.legend(handles=handles)
        plt.show()

    # ---------- INITIAL SETUP AND PREPARATION ---------- #
    def recntrCap(self):
        startCoords = (round(FRAME_DIM/2 - CNTR_DIM/2 - CNTR_OFFSET[0]),
                       round(FRAME_DIM/2 - CNTR_DIM/2 - CNTR_OFFSET[1]))
        endCoords = (round(FRAME_DIM/2 + CNTR_DIM/2 - R_DIM - CNTR_OFFSET[0]),
                     round(FRAME_DIM/2 + CNTR_DIM/2 - R_DIM - CNTR_OFFSET[1]))
        maxLumin = 0

        for yTL in range(startCoords[1], endCoords[1], WHEEL_R_INC):
            for xTL in range(startCoords[0], endCoords[0], WHEEL_R_INC):
                newLumin = self.calcSqrLumin((xTL, yTL), R_DIM)
                if maxLumin < newLumin:
                    maxLumin = newLumin
                    wheelCntr = (xTL + R_DIM/2 + CNTR_OFFSET[0],
                                 yTL + R_DIM/2 + CNTR_OFFSET[1])
        self.cap.setCropCntrFm(wheelCntr)

    def initPanels(self):
        while self.cap.updateBW() and self.panels is None:
            luminVals = []
            for angle in ANGLE_VALS:
                luminVals += [self.calcLuminAngle(angle)]
            self.findPeaks(luminVals)
            peaks = self.calcPeaks()
            if len(peaks) == 1:
                index = int(peaks[0])
                self.panels = self.Panels(index * ANGLE_INC, luminVals[index],
                                          self.calcRotDir(index * ANGLE_INC))

    def calcRotDir(self, angleActivating):
        angleDiff = anglePrev = 0
        for i in range(WHEEL_ROTDIR_CNT + 1):
            luminVals = []
            for angle in range(angleActivating - ANGLE_ESTIMATE_DIST,
                               angleActivating + ANGLE_ESTIMATE_DIST,
                               ANGLE_INC):
                luminVals += [self.calcLuminAngle(angle)]

            angleNew = self.findPeaks(luminVals)[0]
            if i != 0:
                angleDiff += self.calcDiffAngle(angleNew, anglePrev,
                                                ANGLE_ESTIMATE_DIST,
                                                2 * ANGLE_ESTIMATE_DIST)
            anglePrev = angleNew
        self.rotDir = -1

    def calcPeaks(self, angle, range):
        pass


    def calcDiffAngle(self, angleNew, anglePrev, proximity, range):
        diff = angleNew - anglePrev
        if abs(diff) <= proximity:
            pass
        elif diff <= -range:
            diff
        return

    # ---------- CORE ALGORITHM EXECUTION ---------- #
    def calcSqrLumin(self, coordsTL, dim):
        cntPixels = 0
        cntWhites = 0
        for y in range(round(coordsTL[1]), round(coordsTL[1] + dim)):
            for x in range(round(coordsTL[0]), round(coordsTL[0] + dim)):
                cntPixels += 1
                if self.cap.frame[y][x]:
                    cntWhites += 1
        return round(LUM_MAX * cntWhites / cntPixels)

    def calcLuminAngle(self, angle):
        angle *= DEG_TO_RAD
        xTL = FRAME_DIM/2 + MASK_RAD * sin(angle) - MASK_DIM/2
        yTL = FRAME_DIM/2 - MASK_RAD * cos(angle) - MASK_DIM/2
        return self.calcSqrLumin((xTL, yTL), MASK_DIM)

    def findPeaks(self, vals):
        peakIndices, _ = find_peaks(vals + vals[0:1],
                                    height=(LUM_THRESH_LOW, LUM_MAX))
        peaks = []
        for peakIndex in peakIndices:
            peaks += [peakIndex % len(vals)]
        return peaks
