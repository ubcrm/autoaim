from imutils.video import VideoStream
from source.panel_finder.panel_finder import PanelFinder
import cv2
import sys


def display_panel(frame, panel):
    # Display the resulting image
    cv2.circle(frame, (panel["x_center"], panel["y_center"]), 3, (0, 255, 0), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(video_path):
    panel_finder = PanelFinder()  # this panel finder needs no additional properties
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    while ret:
        panel = panel_finder.process(frame)
        display_panel(frame, panel)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        ret, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


def run_webcam():
    panel_finder = PanelFinder()  # this panel finder needs no additional properties
    cap = VideoStream(src=0).start()
    frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    while True:
        panel = panel_finder.process(frame)
        if panel:
            display_panel(frame, panel)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if sys.argv[1] == "video":
        run_video(sys.argv[2])
    elif sys.argv[1] in ["webcam", "pi", "camera"]:
        run_webcam()
