from source.panel_predictor.panel_finder.panel_finder import PanelFinder
import argparse
import cv2


def display_frame(frame, confidence=None, target=None):
    # Display the resulting image
    if target is not None:
        cv2.circle(frame, (target["x_center"], target["y_center"]), 6, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", (target["x_center"], target["y_center"]), 
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def run_video(framework, capture):
    ret, frame = capture.read()
    pause_flag = False
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)
        panel = panel_finder.process(frame)
        if panel is not None:
            confidence, target, _ = panel
            display_frame(frame, confidence, target)
        else:
            display_frame(frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            pause_flag = not(pause_flag)

        if not pause_flag:
            ret, frame = capture.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--framework', default="opencv",
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
