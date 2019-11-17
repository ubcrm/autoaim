import sys
import argparse

from source.panel_finder.panel_classifier.panel_classifier import PanelClassifier

if __name__ == "__main__":

    classifierState = {"mode": sys.argv[1]}

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', action='store_true',
                        help="Specifies the path to the data file to train the model")
    parser.add_argument('-m', '--model', action='store_true',
                        help="Specifies the path to the data file to store or load the trained model")

    args = parser.parse_args()

    if args.data:
        classifierState["data_path"] = args.data

    if args.model:
        classifierState["model_path"] = args.model

    classifier = PanelClassifier(state=classifierState)
