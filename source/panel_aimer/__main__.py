from source.panel_aimer.panel_aimer import PanelAimer
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='debug', help='Mode of panel aimer: run, debug, compete')
    parser.add_argument('-f', '--feed', default='0', help='Feed option: # of camera device, path to video file')
    args = vars(parser.parse_args())

    # target_aimer = PanelAimer(None, mode=args['mode'])
    # target_aimer.process(args['feed'])
    target_aimer = PanelAimer(None, mode='run')
    target_aimer.process('assets/videos/robot_3.mp4')
