import imutils
import cv2

def slope_thresh(quads, width):
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

def angle_comparison():
  return
