import sys
import cv2
from source.rune.preprocess.preprocess import Preprocess
from source.rune.predict_target.predict_target import PredictTarget


def display_target(frame, point):
    # Display the resulting image
    if point is not None:
        cv2.circle(frame, (point[0], point[1]), 3, (0, 0, 255), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(video_path):
    preprocess = Preprocess()
    predict_target = PredictTarget()
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("video at " + str(video_path) + " not found")
    while ret:
        frame = cv2.pyrDown(frame)
        cropped = preprocess.process(frame)
        prediction = predict_target.process(cropped)
        display_target(cropped, prediction)

        if cv2.waitKey(0) & 0xFF == ord('q'):  # press q to quit
            break
        # get next frame
        ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()


def run_webcam(source):
    pass


if __name__ == "__main__":
    if sys.argv[1] == "video":
        run_video(sys.argv[2])
    elif sys.argv[1] in ["webcam", "pi", "camera"]:
        run_webcam()
