from .panel_aimer.panel_aimer import PanelAimer
import argparse
import cv2
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='debug', help='Mode of panel aimer: run, debug, compete')
    parser.add_argument('-f', '--feed', default='0', help='Feed option: # of camera device, path to video file')
    args = vars(parser.parse_args())

    time_start = int(time.time())
    robot_aimer = PanelAimer(None, mode=args['mode'])
    feed = cv2.VideoCapture(args['feed'])

    ret, frame = feed.read()
    while ret:
        robot_aimer.process(frame)

    average_fps = int(feed.get(cv2.CAP_PROP_FRAME_COUNT)) / (time.time() - time_start)
    print('Time per frame: %dms\nFrames per second: %d' % (1e3 / max(1e-3, average_fps), average_fps))
    feed.release()
    cv2.destroyAllWindows()
