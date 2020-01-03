from source.panel_aimer.panel_finder.led_matcher.tensorflow_matcher.tensorflow_matcher import TensorflowMatcher
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', default='assets/data/train.json', help='Path to the train data file')
    parser.add_argument('-m', '--mode', default='train', help='Mode of the classifier: train, load, convert')
    parser.add_argument('-M', '--model', default='assets/model/model.pb',
                        help='Path to data file to store or load trained model')
    args = vars(parser.parse_args())
    TensorflowMatcher(None, mode=args['mode'], data_path=args['data'], model_path=args['model'])
