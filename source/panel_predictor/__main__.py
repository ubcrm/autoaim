from source.panel_predictor.panel_predictor import PanelPredictor
import argparse
import cv2
from imutils.video import VideoStream


def display_frame(frame, target=None):
    # Display the resulting image
    if target is not None:
        target, confidence = target
        cv2.circle(frame, target, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def run_video(video_path, framework):
    panel_predictor = PanelPredictor(state={"framework": framework})
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("video at " + str(video_path) + " not found")
    while ret:
        frame = cv2.pyrDown(frame)
        target = panel_predictor.process(frame)
        display_frame(frame, target)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()


def run_live(framework):
    panel_predictor = PanelPredictor(state={"framework": framework})
    cap = VideoStream(src=0).start()
    frame = cap.read()
    while frame is not None:
        frame = cv2.pyrDown(frame)
        target = panel_predictor.process(frame)
        display_frame(frame, target)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        ret, frame = cap.read()  # get next frame
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
    elif args["mode"] in ["webcam", "camera", "live"]:
        run_live(framework=args["framework"])
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
