import numpy as np
import cv2
from resource import bit_mask, detect_shape, match_leds, find_center
from tensorflow_pipeline.tensorflow_pipeline import TensorflowPipeline
import time


# def predict_leds(ledA, ledB, video_dims, model):
#     first_bound = (ledA['x_center'], ledA['y_center'])
#     second_bound = (ledB['x_center'], ledB['y_center'])
#     center = find_center.find_target_center((first_bound, second_bound))
#
#     res = np.array([TensorflowPipeline.create_nn_input((ledA, ledB), video_dims)])
#     prediction = TensorflowPipeline.model_predict(model, res)[0][1]
#     return prediction
#
#
# def combined_panel(rectA, rectB):
#     center = find_center.find_dict_center([rectA, rectB])
#     width = abs(rectA["x_center"] - rectB["x_center"]) + (rectA["width"] + rectB["width"]) / 2
#     height = abs(rectA["y_center"] - rectB["y_center"]) + (rectA["height"] + rectB["height"]) / 2
#     angle = (rectA["angle"] + rectB["angle"]) / 2
#     new_rect = {"x_center": center[0], "y_center": center[1], "width": width, "height": height, "angle": angle}
#
#     return new_rect


def main():
    vid = "videos/robot3.mp4"  # relative path of downloaded video

    # load video
    cap = cv2.VideoCapture(vid)

    # Capture frame-by-frame
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image in blue, green, red

    model_path = "../assets/tensorflow_pipeline/model/saves/model.hdf5"
    model = TensorflowPipeline.load_model(model_path)
    avg = []
    video_dims = frame.shape[:2]
    past_panel = detect_shape.reformat_cv_rectangle(((video_dims[0] / 2, video_dims[1] / 2), tuple(video_dims), 0))

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    videoOut = cv2.VideoWriter("output.mp4", fourcc, 30, video_dims)

    # loop through frames in video
    while ret:
        start = time.time()

        mask = bit_mask.under_exposed_threshold(frame)
        rectangles = detect_shape.find_rectangles(mask)

        leds = []
        inputs = []

        for r in rectangles:
            reformat = detect_shape.reformat_cv_rectangle(r)
            leds.append(reformat)

        if len(leds) > 1:
            best_pair = (leds[0], leds[1], predict_leds(leds[0], leds[1], video_dims, model))

            for i in range(1, len(leds)):
                for j in range(i + 1, len(leds)):
                    confidence = predict_leds(leds[i], leds[j], video_dims, model)
                    if confidence > best_pair[2]:
                        best_pair = (leds[i], leds[j], confidence)
            print(best_pair[2])
            if best_pair[2] > 0.7:
                panel_rectangle = combined_panel(best_pair[0], best_pair[1])
                past_panel = panel_rectangle
                cv2.circle(frame, (panel_rectangle["x_center"], panel_rectangle["y_center"]), 3, (0, 255, 0), -1)
            else:
                cv2.circle(frame, (past_panel["x_center"], past_panel["y_center"]), 3, (0, 0, 255), -1)

        avg.append(time.time() - start)

        # Display the resulting image
        cv2.imshow('Press q to quit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break

        # save frame
        # videoOut.write(frame)

        # get next frame
        ret, frame = cap.read()
    else:
        print("last frame reached")
    print(1 / (sum(avg) / len(avg)), "fps")
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
