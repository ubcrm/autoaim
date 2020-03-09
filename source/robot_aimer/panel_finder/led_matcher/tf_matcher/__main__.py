from source.target_aimer.panel_finder.led_matcher.tf_matcher.tf_matcher import TfMatcher
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', default='videos/data/train.json', help='Path to the train data file')
    parser.add_argument('-m', '--mode', default='train', help='Mode of the classifier: train, load, convert')
    parser.add_argument('-M', '--model', default='videos/model/model.pb',
                        help='Path to data file to store or load trained model')
    args = vars(parser.parse_args())
    TfMatcher(None, mode=args['mode'], data_path=args['data'], model_path=args['model'])
