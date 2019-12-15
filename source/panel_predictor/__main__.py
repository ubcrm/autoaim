from source.panel_predictor.panel_predictor import PanelPredictor
import argparse
import cv2


def display_frame(frame, target=None):
    # Display the resulting image
    if target is not None:
        target, confidence = target
        cv2.circle(frame, target, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def run_video(panel_predictor, capture):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)
        target = panel_predictor.process(frame)
        display_frame(frame, target)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        ret, frame = capture.read()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--framework', default="tensorflow",
                        help="Specifies which framework to use as inference, e.g. opencv, tensorflow")
    parser.add_argument('-m', '--mode', default="webcam",
                        help="Sets the mode of the classifier. Options: video, webcam")
    parser.add_argument("-v", "--video", help="Path to video")

    args = vars(parser.parse_args())

    panel_predictor = PanelPredictor(state={"framework": framework})

    if args["mode"] == "video" and args["video"]:
        run_video(panel_predictor, cv2.VideoCapture(args["video"]))
    elif args["mode"] in ["webcam", "camera", "live"]:
        run_video(panel_predictor, cv2.VideoCapture(0))
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
