import sys
import cv2

from source.rune.rune import Rune


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


def run_webcam(source):
    pass


if __name__ == "__main__":
    if sys.argv[1] == "video":
        run_video(sys.argv[2])
    elif sys.argv[1] in ["webcam", "pi", "camera"]:
        run_webcam()
