import cv2

def gray_to_thresh(image, thresh_val): 
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)
  thresh = cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY)[1]
  return thresh

def saliency_to_thresh(image, threshold):
  saliency = cv2.saliency.StaticSaliencyFineGrained_create()
  _, saliency_map = saliency.computeSaliency(image)
  saliency_map = (saliency_map * 255).astype("uint8")

  thresh = cv2.threshold(saliency_map.astype("uint8"), threshold, 255,
    cv2.THRESH_BINARY)[1]
  return thresh
