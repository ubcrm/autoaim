def slope_thresh(quads, width):
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


def angle_comparison():
    return

'''
Param: frame
Param: rectangles - an array of rectangle objects
In its current form, it does not return, nor does center_panel, it outputs to frame video.
Can be modified to return coordinates of center of panel using center_panel function.
'''
def get_panels(frame, rectangles):
    #boxes = []
    pairs = []
    for rect in rectangles:
        if (2*rect[1][0] < rect[1][1]) or (rect[1][0] > 2*rect[1][1]):
            if 2*rect[1][0] < rect[1][1]:
                longDim1 = 0
            elif rect[1][0] > 2*rect[1][1]:
                longDim1 = 1
            box = cv2.boxPoints(rect)
            box2 = []
            minAngle = 10;
            for rect2 in rectangles:
                if 2*rect[1][0] < rect[1][1]:
                    longDim2 = 0
                elif rect[1][0] > 2*rect[1][1]:
                    longDim2 = 1
                if (rect2 != rect) and (abs(rect[2]-rect2[2]) < minAngle) and (longDim1 == 1 and  longDim2 == 1):
                    box2 = cv2.boxPoints(rect2)
                    minAngle = abs(rect[2]-rect2[2])

            if len(box2) != 0:
                boxPair = (box, box2)
                pairs.append(boxPair)

            #boxes.append(box)

    #function to get center of panel (located in find Center file)
    center_panel(frame, pairs)
