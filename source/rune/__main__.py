import sys
import cv2
from source.rune.preprocess.preprocess import Preprocess
from source.rune.predict_target.predict_target import PredictTarget


def display_target(frame, point):
    # Display the resulting image
    if point is not None:
        cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    cv2.imshow('Press q to quit', frame)


def run_video(video_path):
    preprocess = Preprocess()
    predict_target = PredictTarget()
    cap = cv2.VideoCapture(video_path)  # load video
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    rune_center = [0.5, 0.5]  # shooting should update the center. Assumes video starts centered
    if not ret:
        raise FileNotFoundError("video at " + str(video_path) + " not found")
    while ret:
        frame = cv2.pyrDown(frame)
        cropped = preprocess.process(frame, rune_center)
        prediction = predict_target.process(cropped)
        display_target(cropped, prediction)
        # shoot(prediction)

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
