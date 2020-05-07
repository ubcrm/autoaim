import numpy as np
import glob
import cv2

img_array = []
size = (0,0)

for filename in glob.glob('images/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 40, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
