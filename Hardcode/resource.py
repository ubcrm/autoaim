import imutils
import cv2


class Mask:

  def grayToThresh(self, image): 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 250, 255, cv2.THRESH_BINARY)[1]
    return thresh
  
  def saliencyToThresh(self, image):
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    _, saliencyMap = saliency.computeSaliency(image)
    saliencyMap = (saliencyMap * 255).astype("uint8")

    thresh = cv2.threshold(saliencyMap.astype("uint8"), 210, 255,
      cv2.THRESH_BINARY)[1]
    return thresh


class Shape:
  
  def findContours(self, thresh):
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts

  def getShape(self,c):
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


  def findQuads(self, cnts, image):
    quads = []

    for c in cnts:
      M = cv2.moments(c)
      if M["m00"] == 0.0:
        cX = int(M["m10"] / 0.00001)
        cY = int(M["m01"] / 0.00001)
      else:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

      shape = self.getShape(c)
    
      if shape == "rectangle" or shape == "pentagon":
        c = c.astype("float")
        c = c.astype("int")
        coord = [cX, cY]
        quads.append(coord)

    return quads


class MatchLEDs:
  
  def slopeThresh(self, quads, width):
    i = 0
    while i < len(quads)-1:
      # determine if two *adjacent* quads exist with a flat slope between them
      dx = abs(quads[i][0] - quads[i+1][0])
      if dx == 0:
        dx = 0.0001
      dy = abs(quads[i][1] - quads[i+1][1])
      if dy == 0: 
        dy = 0.0001

      slope = float(dy/dx)

      # if slope is close to flat, then matching quads found
      if slope < 0.3 and dx<1/11*width: 
        return [quads[i], quads[i+1]]
      i+=1

  def angleComparison(self):
    return


class Target:

  def findCenter(self, quads):
    targetcX = int((quads[0][0] + quads[1][0]) / 2.0)
    targetcY = int((quads[1][1] + quads[1][1]) / 2.0)
    return [targetcX, targetcY]
