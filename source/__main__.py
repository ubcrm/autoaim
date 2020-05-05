from source.panel_predictor.panel_predictor import PanelPredictor
from source.panel_predictor.panel_finder.panel_finder import PanelFinder
from source.gimbal.gimbal import Gimbal
from imutils.video import VideoStream
from source.uart.uart import Uart
import argparse
import cv2


def display_frame(frame, prediction=None):
    if prediction is not None:
        target, distance, confidence = prediction
        cv2.circle(frame, target, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def predict_panels(panel_predictor, gimbal, uart, capture, display=True):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)
        frame_shape = frame.shape[:2]
        prediction = panel_predictor.process(frame)
        
        if prediction is not None:
            target, distance, cumulative_confidence = prediction
            delta_angle = gimbal.process(target[0], target[1], frame_shape)
            uart.send_string(str(delta_angle[0]) + '\r')
        
        if display:
            display_frame(frame, prediction)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
                break
        ret, frame = capture.read()  # get next frame
    capture.release()
    cv2.destroyAllWindows()


def display_panel_finder(frame, confidence=None, target=None):
    # Display the resulting image
    if target is not None:
        cv2.circle(frame, (target["x_center"], target["y_center"]), 6, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", (target["x_center"], target["y_center"]), 
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def find_panels(panel_finder, gimbal, uart, capture, display=True):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)
        frame_shape = frame.shape[:2]
        confidence, target, _ = panel_finder.process(frame)
        
        if target is not None:
            delta_angle = gimbal.process(target["x_center"], target["y_center"], frame_shape)
            uart.send_string(str(delta_angle[0]) + '\r')
        
        if display:
            display_panel_finder(frame, confidence, target)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
                break
        ret, frame = capture.read()  # get next frame
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', "--mode", default="predict", help="Options: predict, find, rune")
    parser.add_argument('-i', "--input", default="webcam", help="Options: webcam, video")
    parser.add_argument("-v", "--video", help="Path to video")
    parser.add_argument('-c', "--camera", default="webcam", help="Which camera to use, e.g. raspberry, webcam")
    parser.add_argument('-f', '--framework', default="opencv",
                        help="Specifies which framework to use as inference, e.g. opencv, tensorflow")
    parser.add_argument('-s', '--show', type=bool, help='Conditonal for displaying frame', default=True)
    args = vars(parser.parse_args())

    panel_finder = PanelFinder(state={"framework": args["framework"]})
    panel_predictor = PanelPredictor(state={"framework": args["framework"]})
    gimbal = Gimbal()
    uart = Uart()

    if args["input"] == "video" and args["video"]:
        input_stream = cv2.VideoCapture(args["video"])
    else:
        input_stream = cv2.VideoCapture(0)

    if args["mode"] == 'predict':
        predict_panels(panel_predictor, gimbal, uart, input_stream, args["show"])
    elif args["mode"] == 'find':
        find_panels(panel_finder, gimbal, uart, input_stream, args["show"])
