#!/usr/bin/env python
#Leer antes de ejecutar
########################################################################################
# Name              : haar_positive_file_creator.py
# Description       : Recorta las imagenes que poseen varior rostros marcados
#                   : Se debe tener una carpeta nombrada 'Recortada', ai se guardan las
#                   : imagenes recortadas
# Compilation       : python haar_positive_creator_varias.py carpetaEntrada outLista.txt
########################################################################################

# module imports

import cv2
import sys
import glob
import os

# global variables

debug = 1
obj_list = []
obj_count = 0
click_count = 0
x1 = 0
y1 = 0
h = 0
w = 0
key = None
frame = None

# mouse callback

def obj_marker(event,x,y,flags,param):
    global click_count
    global debug
    global obj_list
    global obj_count
    global x1
    global y1
    global w
    global h
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        if click_count % 2 == 1:
            x1 = x
            y1 = y
        else:
            w = abs(x1 - x)
            h = abs(y1 - y)
            obj_count += 1
            if x1 > x:
                x1 = x
            if y1 > y:
                y1 = y
            obj_list.append('%d %d %d %d ' % (x1,y1,w,h))
            if debug > 0:
                print obj_list
            cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(255,0,0),5)
            cv2.imshow('frame',frame)


if len(sys.argv) != 4:
    print 'Usage : python haar_positive_creator.py /path/to/location hombre/mujer output_filename.txt'
else:
    if debug > 0:
        print 'Arguments are ok'
        print 'Path is : %s' % sys.argv[1]
        print 'Output file is : %s' % sys.argv[2]
        print 'Click on edges you want to mark as an object'
        print 'Press q to quit'
        print 'Press c to cancel markings'
        print 'Press n to load next image'
    #getting list of jpgs files from
    list = glob.glob('%s/*.jpg' % sys.argv[1])
    if debug > 0:
        print list
    #creating window for frame and setting mouse callback
    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('frame',obj_marker)
    #creating a file handle
    file_name = open(sys.argv[3],"w")
    #loop to traverse through all the files in given path
    for i in list:
        frame = cv2.imread(i)
        frame2 = cv2.imread(i)                                   # reading file
        cv2.imshow('frame',frame)                                               # showing it in frame
        obj_count = 0                                                           #initializing obj_count
        key = cv2.waitKey(100)                                                    # waiting for user key
        while((key & 255 != ord('q')) and (key & 255 != ord('n'))):           # wait till key pressed is q or n
            key = cv2.waitKey(100)                                                # if not, wait for another key press
            if(key & 255 == ord('c')):                                         # if key press is c, cancel previous markings
                obj_count = 0                                                   # initializing obj_count and list
                obj_list = []
                frame = cv2.imread(i)                                           # read original file
                cv2.imshow('frame',frame)                                       # refresh the frame
        if(key & 255 == ord('q')):                                             # if q is pressed
            break                                                               # exit
        elif(key & 255 == ord('n')):                                          # if n is pressed
            destino = os.getcwd()+'/'"SaveRecortada/"+sys.argv[2]+'/'
            #pregunta si la carpeta a sido creada
            if not os.path.exists(destino): 
                os.makedirs(destino)
            ruta_arr = i[:-4].partition("/")
            ruta_arr1 = ruta_arr[2].partition("/")

            ni=1
            if(obj_count > 0):
                if(obj_count == 1):
                    str1 = '%s %d ' % (i,obj_count)                                 # write obj info in file
                    file_name.write(str1)
                    for j in obj_list:
                       file_name.write(j)
                    file_name.write('\n')
                    obj_count = 0
                    obj_list = []
                    cropped = frame2[y1:y1+h, x1:x1+w]
                    ruta = destino+'/'+ruta_arr1[2]
                    print 'Ruta: ',ruta
                    cv2.imwrite(ruta+'_cropped.jpg',cropped)
                else:                                                  # and obj_count > 0
                    str1 = '%s %d ' % (i,obj_count)                                 # write obj info in file
                    file_name.write(str1)
                
                    for j in obj_list:#cada j tiene las cordenadas
                        print'J: ',j
                        list_obj = j.split(" ");
                        frame3 = frame2
                        file_name.write(j)
                        x2=int(list_obj[0])
                        y2=int(list_obj[1])
                        w2=int(list_obj[2])
                        h2=int(list_obj[3])
                        print "x2: ",x2,"--y2: ",y2
                        cropped = frame3[y2:y2+h2, x2:x2+w2]
                        ruta = destino+'/'+ruta_arr1[2]+'_'+str(ni)
                        print 'Ruta: ',ruta
                        cv2.imwrite(ruta+'_cropped.jpg',cropped)
                        ni=ni+1
                file_name.write('\n')
                obj_count = 0
                obj_list = []
    file_name.close()                                                           # end of the program; close the file
cv2.destroyAllWindows()
