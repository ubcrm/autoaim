import cv2
import numpy as np


def gray_to_thresh(image, thresh_val):
    """
    finds panel leds in an image using a black and white threshold

    :param image: BGR image to find leds from
    :param thresh_val: integer between 0 and 255 used as threshold value
    :return: a binary image highlighting leds
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY)[1]
    return thresh


def saliency_to_thresh(image, threshold):
    """
    finds panel leds in an image using a saliency map

    :param image: BGR image to find leds from
    :param threshold: integer between 0 and 255 used as threshold value
    :return: a binary image highlighting leds
    """
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    _, saliency_map = saliency.computeSaliency(image)
    saliency_map = (saliency_map * 255).astype("uint8")

    thresh = cv2.threshold(saliency_map.astype("uint8"), threshold, 255,
                           cv2.THRESH_BINARY)[1]
    return thresh


def over_exposed_threshold(frame):
    """
    finds panel leds in an image using 3 thresholds assuming the leds are washed out

    :param frame: the BGR image to find leds from
    :return: a binary image highlighting leds
    """

    # layer 1: Only high hue pixels using hsv color format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    layer1 = cv2.inRange(hsv, (179 * 0, 0, 250), (179 * 0.5, 60, 255))
    kernel = np.ones((2, 2), np.uint8)
    layer1 = cv2.dilate(layer1, kernel, iterations=7)

    # layer 2: Everything near bright red
    layer2 = cv2.inRange(frame, (100, 0, 230), (200, 130, 255))
    kernel = np.ones((4, 4), np.uint8)
    layer2 = cv2.dilate(layer2, kernel, iterations=10)

    # layer 3: only bright pixels
    layer3 = cv2.inRange(frame, (200, 200, 253), (255, 255, 255))
    kernel = np.ones((3, 3), np.uint8)
    layer3 = cv2.dilate(layer3, kernel, iterations=2)

    # final image: only the overlap of all 3 layers
    result = cv2.bitwise_and(layer1, layer2)
    result = cv2.bitwise_and(result, layer3)
    return layer1


def under_exposed_threshold(frame):
    #     print(round(frame.shape[1] / 384), round(frame.shape[0] / 54))
    blurred = cv2.blur(frame, (round(frame.shape[1] / 384), round(frame.shape[0] / 54)))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, (0, 0, 240), (255, 255, 255))
    return thresh
