from wheel_vision import WheelVision
import cv2

feed = cv2.VideoCapture('videos/red_on_rotating.mov')
vision = WheelVision(feed, (1010, 470), 800)
vision.run(mode_calib=True, show_plot=False, show_disp=True, cont_recntr=True)
