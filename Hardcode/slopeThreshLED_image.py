from resource import bitMask, shapeDetector, matchLEDs, findCenter
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("--save", required=True, 
	help="Path to saved image directory")
args = vars(ap.parse_args())

# function for saving image to disk in "save" directory
def saveToDisk(img, imgName): 
	idx = imgName.find('image-')
	if args['image'][len(args['image'])-1] == '/':
		path = args["save"] + imgName[idx:]
	else: 
		path = args["save"] + '/' + imgName[idx:]
	cv2.imwrite(path, img)

# 1. preprocess
width=600
image = cv2.imread(args["image"])
image = imutils.resize(image, width)
cv2.imshow('Resized',image)
cv2.waitKey(0)

# 2. Mask
threshVal = 250
mask = bitMask.grayToThresh(image, threshVal)

# 3. Find quadrilaterals
contours = shapeDetector.findContours(mask)
quads = shapeDetector.findQuads(contours, image)

# 4. Match Quads
targetLEDs = matchLEDs.slopeThresh(quads, width)

# 5. Compute Center
coords = findCenter.findTargetCenter(targetLEDs)
print('Center Coordinates: '+str(coords))

# show coordinate on image
cv2.circle(image, (coords[0], coords[1]), 3, (0, 255, 0), -1)
cv2.putText(image, "center", (coords[0]-25, coords[1]+20), 
	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
cv2.imshow('center', image)
cv2.waitKey(0)
saveToDisk(image, args['image'])
