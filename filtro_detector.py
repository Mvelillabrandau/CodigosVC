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
    reconoce = 0

    print ('Processing: ',img_path)

    for (x, y, w, h) in rostros:
        reconoce = 1
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if reconoce == 1:
        print('Rostro detectado')

    if reconoce == 0:
        print('Rostro NO detectado')
        shutil.move(img_path, "NoRostro")
    ##cv2.waitKey(0)
