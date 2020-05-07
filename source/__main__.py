from source.panel_predictor.panel_predictor import PanelPredictor
from source.panel_predictor.panel_finder.panel_finder import PanelFinder
from source.gimbal.gimbal import Gimbal
from source.uart.uart import Uart
import argparse
import numpy as np
import cv2
import os


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

# INCOMPLETE
def create_angle_log_file():
    new_filename = "angle_deltas"
    list_dir = os.listdir('./')
    found = False
    print(list_dir)
    for item in list_dir:
        if item.find("angle_deltas"):
            found = True
            num = 1 + int(item[-5])    #.txt is 4 characters
            new_file = new_filename + str(num) + ".txt"
    new_file = new_filename + ".txt"
    open(new_file, "w")
    new_file.write("delta_x     delta_y")
    return new_file


def display_panel_finder(frame, confidence=None, target=None, frame_shape=(0,0), delta_angles=(0,0)):
    # Display the resulting image
    if target is not None:
        cv2.circle(frame, (target["x_center"], target["y_center"]), 6, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", (target["x_center"], target["y_center"]), 
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255))
        origin = (int(frame_shape[1] / 2), int(frame_shape[0] / 2,))
        cv2.arrowedLine(frame, origin, (target["x_center"], target["y_center"]), (0,0,255), 5)
        cv2.putText(frame, "yaw: {}".format(int(delta_angles[0])), (frame_shape[1]-160, 40), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0),2)
        cv2.putText(frame, "pitch: {}".format(int(delta_angles[1])), (frame_shape[1]-160, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0),2)
    cv2.imshow('Press q to quit', frame)
    return frame


def find_panels(panel_finder, gimbal, uart, capture, display=True, serial=False, make_video=False, save_image=False):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    pause_flag = False
    count = 0

    if make_video:
        # Define the codec and create VideoWriter object
        resized_frame = cv2.pyrDown(frame)
        frame_shape = resized_frame.shape[:2]   #(rows,cols)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (frame_shape[1],frame_shape[0]))

    while ret:
        if not pause_flag:
            resized_frame = cv2.pyrDown(frame)
            frame_shape = resized_frame.shape[:2]   #(rows,cols)
            confidence, target, _ = panel_finder.process(resized_frame)

            if target is not None:
                delta_angles = gimbal.process(target["x_center"], target["y_center"], frame_shape)
                print(delta_angles)
                if serial:
                    try:
                        uart.send_string(str(delta_angles[0]) + '\r')
                    except:
                        print("uart failed")
        if display:
            image = display_panel_finder(resized_frame, confidence, target, frame_shape, delta_angles)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
                break
            if cv2.waitKey(1) & 0xFF == ord(' '):
                pause_flag = not(pause_flag)
            if save_image:
                cv2.imwrite("images/debug" + str(count) + ".png", image)
                count+=1
            if make_video:
                out.write(image)

        if not pause_flag:
            ret, frame = capture.read()
    if make_video:
        out.release()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', "--platform", default="laptop", help="Options: laptop, nano, pi")
    parser.add_argument('-m', "--mode", default="predict", help="Options: predict, find, rune")
    parser.add_argument('-t', "--transmit", default=False, help="Enable UART conditional")
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

    if args["transmit"]:
        uart = Uart(state={"platform": args["platform"]})
    else:
        uart = False

    if args["input"] == "video" and args["video"]:
        input_stream = cv2.VideoCapture(args["video"])
    else:
        input_stream = cv2.VideoCapture(0)

    if args["mode"] == 'predict':
        predict_panels(panel_predictor, gimbal, uart, input_stream, args["show"])
    elif args["mode"] == 'find':
        find_panels(panel_finder, gimbal, uart, input_stream, args["show"])
