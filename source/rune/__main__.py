import sys
import cv2
import argparse

from source.rune.rune import Rune


def display_target(frame, point):
    # Display the resulting image
    if point is not None:
        cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(capture):
    rune = Rune()
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame_bw is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        prediction = rune.process(frame)
        display_target(frame, prediction)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        ret, frame = capture.read()  # get next frame
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default="camera",
                        help="Sets the mode of the classifier. Options: video, webcam")
    parser.add_argument("-v", "--video", help="Path to video")

    args = vars(parser.parse_args())

    if args["mode"] == "video" and args["video"]:
        run_video(cv2.VideoCapture(args["video"]))
    elif args["mode"] in ["webcam", "camera", "live"]:
        run_video(cv2.VideoCapture(0))
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
