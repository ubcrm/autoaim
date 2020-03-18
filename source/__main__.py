from source.panel_predictor.panel_predictor import PanelPredictor
from source.gimbal.gimbal import Gimbal
from imutils.video import VideoStream
from source.uart.uart import Uart
import argparse
import cv2


#def display_frame(frame, distance, confidence, angle, target):
    # Display the resulting image
    #if target is not None:
        #cv2.circle(frame, target, 3, (0, 255, 0), -1)
        #cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
        #cv2.putText(frame, str(int(distance * 100)) + "m", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
        #cv2.putText(frame, str(int(angle * 100)) + "degrees", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    #cv2.imshow('Press q to quit', frame)

def display_frame(frame, target=None):
    # Display the resulting image
    if target is not None:
        target, distance, confidence = target
        cv2.circle(frame, target, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(int(confidence * 100)) + "%", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
        #cv2.putText(frame, str(int(distance * 100)) + "m", target, cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))
    cv2.imshow('Press q to quit', frame)

#def run(panel_predictor, gimbal, uart, capture, display=True):
def run(panel_predictor, capture):
    ret, frame = capture.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red
    if not ret:
        raise FileNotFoundError("input not found")
    while ret:
        frame = cv2.pyrDown(frame)

        #frame_shape = frame.shape[:2]
        
        #target, distance, cumulative_confidence = panel_predictor.process(frame)
        target = panel_predictor.process(frame)
        print(target)
        #current_angle = uart.read_hex()
        #next_angle = current_angle + gimbal.process(target[0], target[1], frame_shape)
        try:
            delta_angle = gimbal.process(target[0], target[1], frame_shape)
            #uart.send_hex(delta_angle)
        except:
            print("delta angle failure")
            #print("target0: "+ target[0])
            #print("target1: " + target[1])
        
        #if display:  #TO-DO
        #display_frame(frame, distance, cumulative_confidence, delta_angle, target)
        display_frame(frame,target)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
        ret, frame = capture.read()  # get next frame
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--camera", default="webcam", help="Which camera to use, e.g. raspberry, webcam")
    parser.add_argument('-i', '--framework', default="opencv",
                        help="Specifies which framework to use as inference, e.g. opencv, tensorflow")
    parser.add_argument('-s', '--show', type=bool, help='Conditonal for displaying frame', default=True)
    args = vars(parser.parse_args())

    #if args["camera"] == "webcam":
        #video_stream = VideoStream(src=0).start()
    #else:
        #video_stream = VideoStream(usePiCamera=True).start()

    panel_predictor = PanelPredictor(state={"framework": args["framework"]})
    #gimbal = Gimbal()
    #uart = Uart()
    #run(panel_predictor, gimbal, uart, cv2.VideoCapture(0), args["show"])
    run(panel_predictor, cv2.VideoCapture(0))
