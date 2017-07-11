import numpy as np
import cv2
import sys


N_DIV_X = 5 # La imagen se divide en N_DIV_X x N_DIV_Y celdas
N_DIV_Y = 9 # La imagen se divide en N_DIV_X x N_DIV_Y celdas

RESIZE_FACTOR = 1.0 # Factor de re-escalamiento de imagen de entrada. Solo para marcar. Mascara se guarda en tamano original de la imagen

mask = np.zeros((N_DIV_Y, N_DIV_X, 1), np.uint8) # matriz que guarda las celdas con oclusion. 0: normal, 1: ocluido

# Archivo de lista de imagenes de entrada
FILE_INPUT = 'lista_recortada.txt'
# Archivo de salida con nombre imagen y razon de oclusion.
# Las mascara (imagenes) se guardan en la misma ruta quye las imagenes originales agregando "_mask.jpg"
FILE_OUTPUT = 'lista_caras_mask.txt'

############ FUNCIONES ########################3


def grid_select(event, x, y, flags, img):

	(rows, cols, kk) = img.shape

	DIV_SIZE_X = cols / N_DIV_X
	DIV_SIZE_Y = rows / N_DIV_Y

	if event == cv2.EVENT_LBUTTONDOWN:
		x_grid = int(round(x / DIV_SIZE_X))
		y_grid = int(round(y / DIV_SIZE_Y))
		if mask[y_grid, x_grid] == 0:
			img[y_grid * DIV_SIZE_Y: DIV_SIZE_Y * (y_grid + 1), x_grid * DIV_SIZE_X: (x_grid + 1) * DIV_SIZE_X] *= 0.5
			mask[y_grid, x_grid] = 1
		else:
			img[y_grid * DIV_SIZE_Y: DIV_SIZE_Y * (y_grid + 1), x_grid * DIV_SIZE_X: (x_grid + 1) * DIV_SIZE_X] *= 2
			mask[y_grid, x_grid] = 0

		draw_lines(img)


def draw_lines(img):
	(rows, cols, kk) = img.shape
	DIV_SIZE_X = cols / N_DIV_X
	DIV_SIZE_Y = rows / N_DIV_Y

	for i in range(0, cols, DIV_SIZE_X):
		cv2.line(img, (i, 0), (i, rows), (0, 0, 255), 1)

	for j in range(0, rows, DIV_SIZE_Y):
		cv2.line(img, (0, j), (cols, j), (0, 0, 255), 1)


def save_mask(img, img_path, mask, file_out):
	(rows, cols, kk) = img.shape
	mask_img = img * 0
	counter = 0
	DIV_SIZE_X = cols / N_DIV_X
	DIV_SIZE_Y = rows / N_DIV_Y

	for x in range(0, N_DIV_X):
		for y in range(0, N_DIV_Y):
			if mask[y, x] == 1:
				mask_img[y * DIV_SIZE_Y: DIV_SIZE_Y * (y + 1), x * DIV_SIZE_X: (x + 1) * DIV_SIZE_X] = 255
				counter += 1

	# save image_mask
	img_path = img_path.partition("/")
	img_path = img_path[2][:-4]
	#print("imgp: ",img_path)
	save_path ="Mask/" + img_path + "_mask.png"
	#print("savep: ",save_path)
	mask_save = cv2.resize(mask_img, None, fx = 1/RESIZE_FACTOR, fy = 1/RESIZE_FACTOR, interpolation = cv2.INTER_LINEAR)

	cv2.imwrite(save_path, mask_save)

	# print output
	if counter == 0:
		#print img_path + " " + 	str(0)
		file_out.write(img_path + " " + str(0)+"\n")
	else:
		print img_path + " " + str(counter*1.0 / (N_DIV_X*N_DIV_Y))
		file_out.write(img_path + " " + str(counter*1.0 / (N_DIV_X*N_DIV_Y))+"\n")

	file_out.flush()








################## MAIN ################################3


f_i = open(FILE_INPUT, 'r')
f_o = open(FILE_OUTPUT, 'w')

# show normalized image and set callback
cv2.namedWindow('image')

img_list = []
# load
for line in f_i:
	img_path = line.split()
	img_path = img_path[0]
	img_list.append(img_path)

index = 0
f_i.close()


while True:
	img_path ='Recortada/'+img_list[index]
	# Load color image
	img_orig = cv2.imread(img_path)
	img = cv2.resize(img_orig, None, fx = RESIZE_FACTOR, fy = RESIZE_FACTOR, interpolation = cv2.INTER_CUBIC)
	img = np.float_(img/255.0)
	draw_lines(img)
	cv2.setMouseCallback('image', grid_select, img)

	# Reset Model and mask
	mask *= 0


	while True:
		cv2.imshow('image', img)
		key = cv2.waitKey(100)
		if chr(key & 255) == 'z':  # next image without saving
			#print "Next image"
			index += 1
			if index == len(img_list):
				index = index - 1
			break
		if chr(key & 255) == 'a': # previous image without saving
			#print "Prev image"
			index -= 1
			if index <= 0:
				index = 0
			break
		elif chr(key & 255) == 'e': # exit (without saving current iamge)
			# print "Exiting"
			f_o.close()
			sys.exit(0)
		elif chr(key & 255) == 'g': # save mask and ad
			save_mask(img, img_path, mask, f_o)
			index += 1
			if index == len(img_list):
				index = index - 1
			break
