import argparse
import cv2

from source.rune.predict_target.assign_panels.assign_panels import AssignPanels

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', default="assets/image-2.png", help="Specifies the path to rune image file")
    parser.add_argument('-m', '--mode', default='debug', help="Mode to run in. Choose from 'run', 'debug'")
    args = parser.parse_args()

    assigner = AssignPanels(state={"mode": args.mode})
    panel_states = assigner.process(cv2.imread(args.image))
    print(panel_states)
