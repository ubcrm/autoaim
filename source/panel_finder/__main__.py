from source.panel_finder.panel_finder import PanelFinder
from imutils.video import VideoStream
import argparse
import cv2


def display_frame(frame, panel=None):
    # Display the resulting image
    if panel is not None:
        cv2.circle(frame, (panel["x_center"], panel["y_center"]), 3, (0, 255, 0), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(video_path, framework):
    panel_finder = PanelFinder(state={"framework": framework})  # this panel finder needs no additional properties
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("video at " + str(video_path) + " not found")
    while ret:
        panel = panel_finder.process(frame)
        display_frame(frame, panel)

        if cv2.waitKey(0) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()


def run_live(framework):
    panel_finder = PanelFinder(state={"framework": framework})
    cap = VideoStream(src=0).start()
    frame = cap.read()

    while True:
        panel = panel_finder.process(frame)
        display_frame(frame, panel)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--framework', default="tensorflow",
                        help="Specifies which framework to use as inference, e.g. opencv, tensorflow")
    parser.add_argument('-m', '--mode', default="webcam",
                        help="Sets the mode of the classifier. Options: video, webcam")
    parser.add_argument("-v", "--video", help="Path to video")

    args = vars(parser.parse_args())

    if args["mode"] == "video" and args["video"]:
        run_video(video_path=args["video"], framework=args["framework"])
    elif args["mode"] in ["webcam", "camera"]:
        run_live(framework=args["framework"])
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
