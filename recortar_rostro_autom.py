import cv2
import sys
import os
import shutil

cascade_dir = sys.argv[2]
rostroCascade = cv2.CascadeClassifier(cascade_dir)

for filename in os.listdir(sys.argv[1]):
    rostroCascade = cv2.CascadeClassifier(cascade_dir)
    img_path = os.path.join(sys.argv[1], filename)
    img = cv2.imread(img_path)
    filtro = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img is None:
        print ('Cannot open file:', img_path)
        continue
    rostros = rostroCascade.detectMultiScale(
		filtro,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize= (30,30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)
    cropped = img
    print ('Processing: ',img_path)
    for (x, y, w, h) in rostros:
        cropped = img[y:500, x:500]
        #cv2.imshow("cropped", cropped)
        nombre = img_path[:-4]+'_recorte.jpg'
        cv2.imwrite(nombre, cropped)
    #cv2.waitKey(0)
    shutil.move(nombre, "RostrosM")
