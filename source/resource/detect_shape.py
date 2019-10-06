import imutils
import cv2
import numpy as np


def find_contours(thresh):
    """
    gets areas of color from image

    :param thresh: a binary image
    :return: an array of openCV contours
    """
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts


def get_shape(c):
    """
    finds shape of a contour

    :param c: an openCV contour
    :return: a string of the name of the shape
    """
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 1:
        shape = "line"

    if len(approx) == 3:
        shape = "triangle"

    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

    elif len(approx) == 5:
        shape = "pentagon"

    else:
        shape = "circle"

    return shape


def find_quad_centers(contours):
    """
    finds centers of contours that have 4 sides

    :param contours: a list of openCV contours
    :return: a list of coordinates in the form [x,y]
    """
    quads = []

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0.0:
            cX = int(M["m10"] / 0.00001)
            cY = int(M["m01"] / 0.00001)
        else:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

        shape = get_shape(c)

        if shape == "rectangle" or shape == "pentagon":
            c = c.astype("float")
            c = c.astype("int")
            coord = [cX, cY]
            quads.append(coord)

    return quads


def find_rectangles(filtered):
    """
    finds rectangles around leds

    :param filtered: a binary image of suspected leds
    :return: a list of rectangles in the format ((centerX,centerY),(width,height),(rotation))
    """
    # puts rectangles on blobs
    contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rectangles = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        if min(rect[1]) > 10:
            rectangles.append(rect)
    return rectangles
