import cv2
import sys
import os
import shutil

for filename in os.listdir(sys.argv[1]):
    img_path = os.path.join(sys.argv[1], filename)
    img = cv2.imread(img_path)

    if img is None:
        print ('Cannot open file:', img_path)
        continue

    print ('Redimencionando: ',img_path)
#W,H
    resized = cv2.resize(img, (640,640))
    cv2.imwrite(img_path[:-4]+'.jpg', resized)
    #cv2.imshow("original", img)
    #cv2.waitKey(0)
