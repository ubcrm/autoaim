from source.gimbal_angle_finder.gimbal_angle_finder import GimbalAngleFinder
from source.distance_predictor.distance_predictor import DistancePredictor
from source.panel_predictor.panel_predictor import PanelPredictor
from pivideostream import PiVideoStream
from source.uart_driver import uart
import argparse
import cv2


def display_frame(frame, distance, angle, target=None):
    # Display the resulting image
    if target is not None:
        target, confidence = target
        cv2.circle(frame, target, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
        #cv2.putText(frame, str(int(distance * 100)) + "m", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
        #cv2.putText(frame, str(int(angle * 100)) + "degrees", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)


def run(panel_predictor, distance_predictor, gimbal_angle_finder, capture, display):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)
        target = panel_predictor.process(frame)
        #distance = distance_predictor.process(target)
        distance = 0
        #current_angle = uart.listen()
        current_angle = 0
        #next_angle = gimbal_angle_finder.calculate(current_angle)
        next_angle = 0
        if display:
            display_frame(frame, distance, next_angle, target)
        #uart.send(next_angle)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        ret, frame = capture.read()  # get next frame
    capture.release()
    cv2.destroyAllWindows()


class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32):
		if usePiCamera:
			# initialize the picamera stream and allow the camera sensor to warmup
			self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
		# otherwise, we are using OpenCV so initialize the webcam stream
		else:
			self.stream = cv2.VideoCapture(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--framework', default="tensorflow",
                        help="Specifies which framework to use as inference, e.g. opencv, tensorflow")
    parser.add_argument('-s', '--show', type=bool, help='Conditonal for displaying frame', default=False)
    args = vars(parser.parse_args())
    video_stream = VideoStream(usePiCamera=True)
    panel_predictor = PanelPredictor(state={"framework": args["framework"]})
    distance_predictor = DistancePredictor()
    gimbal_angle_finder = GimbalAngleFinder()
    run(panel_predictor, distance_predictor, gimbal_angle_finder, video_stream, args["show"])
