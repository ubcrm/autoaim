import cv2

def findTargetCenter(bounds):
    targetcX = int((bounds[0][0] + bounds[1][0]) / 2.0)
    targetcY = int((bounds[0][1] + bounds[1][1]) / 2.0)
    return [targetcX, targetcY]