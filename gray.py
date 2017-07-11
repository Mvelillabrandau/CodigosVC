import cv2
import sys
import os
import shutil

for filename in os.listdir(sys.argv[1]):
    img_path = os.path.join(sys.argv[1], filename)
    img = cv2.imread(img_path,0)

    if img is None:
        print ('Cannot open file:', img_path)
        continue

    print ('Processing: ',img_path)
    cv2.imwrite(img_path[:-4]+'_.jpg', img)
    #cv2.imshow("original", img)
    #cv2.waitKey(0)
