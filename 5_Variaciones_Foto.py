import cv2
import shutil
import sys
import os
import imutils
import numpy as np
from matplotlib import pyplot as plt

for filename in os.listdir(sys.argv[1]):
    img_path = os.path.join(sys.argv[1], filename)
    img = cv2.imread(img_path,0)
    cv2.imwrite(img_path[:-4]+'_gray.jpg', img) # 1

    if img is None:
        print ('Cannot open file:', img_path)
        continue

    print ('Processing: ',img_path)

    for angle in xrange(5, 15, 5):
    	# rotate the image and display it
    	rotated = imutils.rotate(img, angle=angle)
    	#cv2.imshow("Angle=%d" % (angle), rotated)
        cv2.imwrite(img_path[:-4]+'_gray_rotated'+str(angle)+'.jpg', rotated) # 2 y 3

    for angle in xrange(350, 360, 5):
    	# rotate the image and display it
    	rotated = imutils.rotate(img, angle=angle)
    	#cv2.imshow("Angle=%d" % (angle), rotated)
        cv2.imwrite(img_path[:-4]+'_gray_rotated'+str(angle)+'.jpg', rotated) # 4 y 5

    #cv2.waitKey(0)
