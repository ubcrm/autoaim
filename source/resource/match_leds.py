from resource.find_center import center_panel
import cv2

def slope_thresh(quads, width):
    """
    returns a pair rectangles based on the slope between them

    :param quads: the centers of rectangles in the form [x,y]
    :param width: the width of the rectangles
    :return: a pair of centers in the form [[x1,y1],[x2,y2]]
    """
    i = 0
    while i < len(quads) - 1:
        # determine if two *adjacent* quads exist with a flat slope between them
        dx = abs(quads[i][0] - quads[i + 1][0])
        if dx == 0:
            dx = 0.0001
        dy = abs(quads[i][1] - quads[i + 1][1])
        if dy == 0:
            dy = 0.0001

        slope = float(dy / dx)

        # if slope is close to flat, then matching quads found
        if slope < 0.3 and dx < 1 / 11 * width:
            return [quads[i], quads[i + 1]]
        i += 1


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
            min_angle = 10;
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
