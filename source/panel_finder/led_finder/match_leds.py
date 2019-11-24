import cv2


def get_panels(rectangles):
    """
    pairs rectangles the belong to the same panel

    :param: rectangles - an array of openCV
    :return: a list of pairs of rectangles in the form [(r1,r2),(r3,r4),...]
    """

    pairs = []
    for rect in rectangles:
        if (2 * rect[1][0] < rect[1][1]) or (rect[1][0] > 2 * rect[1][1]):
            if 2 * rect[1][0] < rect[1][1]:
                long_dim1 = 0
            elif rect[1][0] > 2 * rect[1][1]:
                long_dim1 = 1

            box = cv2.boxPoints(rect)
            box2 = []
            min_angle = 10
            for rect2 in rectangles:
                if 2 * rect[1][0] < rect[1][1]:
                    long_dim2 = 0
                elif rect[1][0] > 2 * rect[1][1]:
                    long_dim2 = 1
                if (rect2 != rect) and (abs(rect[2] - rect2[2]) < min_angle) and (long_dim1 == 1 and long_dim2 == 1):
                    box2 = cv2.boxPoints(rect2)
                    min_angle = abs(rect[2] - rect2[2])

            if len(box2) != 0:
                box_pair = (box, box2)
                pairs.append(box_pair)

    return pairs
