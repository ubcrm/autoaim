import sys
import cv2
from imutils.video import VideoStream
import argparse

from rune.rune import Rune


def display_target(frame, point):
    # Display the resulting image
    if point is not None:
        cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(video_path):
    rune = Rune()
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame_bw is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("video at " + str(video_path) + " not found")
    while ret:
        prediction = rune.process(frame)
        display_target(frame, prediction)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        ret, frame = cap.read()  # get next frame
    cap.release()
    cv2.destroyAllWindows()


def run_live():
    rune = Rune()
    cap = VideoStream(src=0).start()
    frame = cap.read()

    while frame is not None:
        prediction = rune.process(frame)
        display_target(frame, prediction)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        frame = cap.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default="camera",
                        help="Sets the mode of the classifier. Options: video, camera")
    parser.add_argument("-v", "--video", help="Path to video")

    args = vars(parser.parse_args())

    if args["mode"] == "video" and args["video"]:
        run_video(video_path=args["video"])
    elif args["mode"] in ["webcam", "pi", "camera", "live"]:
        run_live()
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
