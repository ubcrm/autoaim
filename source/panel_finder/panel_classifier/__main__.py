import sys

from source.panel_finder.panel_classifier.panel_classifier import PanelClassifier

if __name__ == "__main__":
    for i in range(5):
        classifierState = {"mode": sys.argv[1]}
        if len(sys.argv) > 2:
            classifierState["data_path"] = sys.argv[2]
        if len(sys.argv) > 3:
            classifierState["model_path"] = sys.argv[3]
        classifier = PanelClassifier(state=classifierState)

    # test_x, test_y = pipeline.train_model()
    # pipeline.evaluate_model(test_x, test_y)
    # pipeline.save_model()
    # m = PanelClassifier.load_model(model_path)

    # training_x, training_y, testing_x, testing_y = classifier.create_data()
    # print("The model predicts:", classifier.process(training_x[0], (1920, 1080)))
    # print("The actual value is:", training_y[0].argmax())
