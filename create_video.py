'''
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


import cv2
import numpy as np

img=[]
for i in range(0,5):
    img.append(cv2.imread("images/debug" + str(i)+'.png'))

height,width,layers=img[1].shape

video=cv2.VideoWriter('video.avi',-1,1,(width,height))

for j in range(0,5):
    video.write(img[j])

cv2.destroyAllWindows()
video.release()

'''



while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

# Release everything if job is finished
cap.release()

cv2.destroyAllWindows()