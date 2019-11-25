from source.panel_predictor.panel_finder.panel_classifier import PanelClassifier
import argparse

if __name__ == "__main__":

    classifierState = {}

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data',
                        help="Specifies the path to the data file to train the model")
    parser.add_argument('-m', '--mode', required=True,
                        help="Sets the mode of the classifier. Options: train, load")
    parser.add_argument('-M', '--model',
                        help="Specifies the path to the data file to store or load the trained model, (load, train, convert, pi)")

    args = vars(parser.parse_args())

    if args["mode"]:
        classifierState["mode"] = args["mode"]
    if args["data"]:
        classifierState["data_path"] = args["data"]
    if args["model"]:
        classifierState["model_path"] = args["model"]

    classifier = PanelClassifier(state=classifierState)
