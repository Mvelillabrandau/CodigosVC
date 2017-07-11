#$python ClasificadorRostros.py haarcascade...xml nombre-carpeta-fotos
import cv2
import sys
import os


cascade_dir = sys.argv[1]
rostroCascade = cv2.CascadeClassifier(cascade_dir)

factor = 5

for filename in os.listdir(sys.argv[2]):
	img_path = os.path.join(sys.argv[2], filename)
	img = cv2.imread(img_path)
	img1 = cv2.imread(img_path)
	if img is None:
		print (' Cannot open file: ',img_path)
		continue

	ruta_img = img_path[:-4].partition("/")
	ruta_img1 = ruta_img[2].partition("/")
#	print("ruta_img: ",ruta_img)
#	print("ruta_img1: ",ruta_img1)

	#Obtener alto y ancho de la imagen
	height, width = img.shape[:2]

#	img = cv2.resize(img,None,fx=factor,fy=factor,interpolation = cv2.INTER_CUBIC)
#	img1 = cv2.resize(img1,None,fx=factor,fy=factor,interpolation = cv2.INTER_CUBIC)


	filtro = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	rostros = rostroCascade.detectMultiScale(
		filtro,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize= (30,30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)
	for (x, y, w, h) in rostros:
		cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.imshow("Image", img1)
	print ("IMG: ",img_path)

#	print("Espera boton")
	while True:

		key = cv2.waitKey(100)
		#En caso de no detectar rostros o detecte mal lo rostros
		if chr(key & 255 ) == 'n':
			print("Not Face")
			destino = os.getcwd()+'/'"Not_Face"
			if not os.path.exists(destino):
				os.makedirs(destino)
			ruta = destino+'/'+ruta_img1[0]
			print("ruta: ",ruta)
			cv2.imwrite(ruta+'.jpg',img)
			break
		if chr(key & 255) == 'm':
			print("mujer")
			destino = os.getcwd()+'/'"mujer"
			if not os.path.exists(destino):
				os.makedirs(destino)
			ruta = destino+'/'+ruta_img1[0]
			print("Ruta: ",ruta)
			cv2.imwrite(ruta+'.jpg',img)
			break
		if chr(key & 255) == 'h':
			print("hombre")
			destino = os.getcwd()+'/'"hombre"
			if not os.path.exists(destino):
				os.makedirs(destino)
			ruta = destino+'/'+ruta_img1[0]
			print("Ruta: ",ruta)
			cv2.imwrite(ruta+'.jpg',img)
			break
		if chr(key & 255) == 'v':
			print("hombre")
			destino = os.getcwd()+'/'"vario"
			if not os.path.exists(destino):
				os.makedirs(destino)
			ruta = destino+'/'+ruta_img1[0]
			print("Ruta: ",ruta)
			cv2.imwrite(ruta+'.jpg',img)
			break
		
		if chr(key & 255) == 'e':# exit
			print("Adios")
			sys.exit(0)