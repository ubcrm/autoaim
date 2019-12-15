from source.panel_predictor.panel_finder.panel_finder import PanelFinder
import argparse
import cv2


def display_frame(frame, panel=None):
    # Display the resulting image
    if panel is not None:
        cv2.circle(frame, (panel[0]["x_center"], panel[0]["y_center"]), 3, (0, 255, 0), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(framework, capture):
    ret, frame = capture.read()
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        panel = panel_finder.process(frame)
        display_frame(frame, panel)

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

    panel_finder = PanelFinder(state={"framework": args["framework"]})

    if args["mode"] == "video" and args["video"]:
        run_video(panel_finder, cv2.VideoCapture(args["video"]))
    elif args["mode"] in ["webcam", "camera", "live"]:
        run_video(panel_finder, cv2.VideoCapture(0))
    else:
        print("No valid mode specified, Exiting.")
        exit(1)
