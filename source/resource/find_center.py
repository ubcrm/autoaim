def find_target_center(bounds):
    targetcX = int((bounds[0][0] + bounds[1][0]) / 2.0)
    targetcY = int((bounds[0][1] + bounds[1][1]) / 2.0)
    return [targetcX, targetcY]

#pairs is an array of tuples: boxPairs
#boxPairs, a tuple containing 2 boxes
#box1 and box2 contains coordinates of 4 corners of each box
def center_panel(frame, pairs):
    for boxPair in pairs:
        box1 = boxPair[0]
        box2 = boxPair[1]

        #box number one
        xa1 = box1[0, 0]
        ya1 = box1[0, 1]
        xb1 = box1[1, 0]
        yb1 = box1[1, 1]
        xc1 = box1[2, 0]
        yc1 = box1[2, 1]
        xd1 = box1[3, 0]
        yd1 = box1[3, 1]

        #box number two
        xa2 = box2[0, 0]
        ya2 = box2[0, 1]
        xb2 = box2[1, 0]
        yb2 = box2[1, 1]
        xc2 = box2[2, 0]
        yc2 = box2[2, 1]
        xd2 = box2[3, 0]
        yd2 = box2[3, 1]

        #centerCoordinates
        cX = int((xa1 + xb1 + xc1 + xd1 + xa2 + xb2 + xc2 + xd2)/8)
        cY = int((ya1 + yb1 + yc1 + yd1 + ya2 + yb2 + yc2 + yd2)/8)

        cv2.circle(frame, (cX,cY), 3, (0,0,255), thickness=4, lineType=8, shift=0)

