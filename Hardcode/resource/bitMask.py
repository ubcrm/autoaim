import cv2

def grayToThresh(image, threshVal): 
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)
  thresh = cv2.threshold(blurred, threshVal, 255, cv2.THRESH_BINARY)[1]
  return thresh

def saliencyToThresh(image, threshold):
  saliency = cv2.saliency.StaticSaliencyFineGrained_create()
  _, saliencyMap = saliency.computeSaliency(image)
  saliencyMap = (saliencyMap * 255).astype("uint8")

  thresh = cv2.threshold(saliencyMap.astype("uint8"), threshold, 255,
    cv2.THRESH_BINARY)[1]
  return thresh
