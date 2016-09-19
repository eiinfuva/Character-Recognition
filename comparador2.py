# coding: utf-8                                                                        
#!usr/bin/python
import math
import cv
from sys import argv
from numpy import *
import Image
import pylab

#nuestro
#compara los puntos de la letra con el fichero con la fuente
def leer_letra(centros_buscado):

    if(len(centros_buscado)==0):
        return "O"

    fich = open("abecedario.txt")
    centros_letras = []
    for k in range(26):

        puntos = fich.readline()
        punto = puntos[3:-1].split('(')
        centros_letras.append([])

        for i in punto:

            centros_letras[k].append(i[:-1].split(','))

    centros_A = centros_letras[0]

    letra_encontrada = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    return letra_encontrada[buscar(centros_letras,centros_buscado)]
                
#distancia entre 2 puntos
def modulo((x1,y1),(x2,y2)):
    
    x11 = int(x1);
    x21 = int(x2)
    y11 = int(y1)
    y21 = int(y2)
    return math.sqrt((math.pow(x11-x21,2))+(math.pow(y21-y11,2)))

#compara los puntos de dos letras
def comparar(i,letra):

    v=modulo(i[0],i[1])
    v2=modulo(letra[0],letra[1])
    vv=modulo(i[0],i[2])
    vv2=modulo(letra[0],letra[2])
    if(abs((v/vv)-(v2/vv2))<=0.001):

        return True
    else:
        return False


def buscar(centros,letra):
    j=0
    for i in centros:
        
        if(len(i)==len(letra)):

            if (comparar(i,letra)):
                return j
        j+=1

def centro(apuntos):
    
    x=0
    y=0

    for i in apuntos:

        x += i[0]
        y += i[1]

    x=x/len(apuntos)
    y=y/len(apuntos)
    
    return (x,y)

def add(punto,esquinas,distancia):

    dentro = 0
    for i in esquinas:
        
        if((modulo(centro(esquinas[i]),punto))<distancia):
            esquinas[i].append(punto)
            dentro=1
            break
    if(dentro==0): 
        
        esquinas[len(esquinas)]=[punto]
#Esta funcion calcula las esquinas que tiene la imagen utilizando una funcion 
#de opencv que hace el algoritmo de Harris Corner Detection, el cual lo que 
#localiza los puntos de interes en los alrededores analizando cambios de intensidad 
 #que se producen en cada píxel para un tamaño determinado de ventana. 
def guardar_esquinas(cent,let):

    
    f = open ("abecedario.txt", "a")
    f.write(let+" ")

    for i in range(len(cent)):
        f.write(str(cent[i]))
    f.write("\n")
    f.close()


def print_esquinas(esqu1,image,distancia):



    img_or = cv.LoadImage(image)
    img = cv.LoadImage(image, cv.CV_LOAD_IMAGE_GRAYSCALE)
    w = img.width
    h = img.height
    for i in range(len(esqu1)):

        cv.Circle(img_or,esqu1[i],distancia,cv.RGB(155, 25, 25))
    cv.ShowImage('Harris', img_or)
    cv.SaveImage('Harris2.jpg', img_or)
    cv.WaitKey()

#carmensrz
def corner_detection(image):
    img_or = cv.LoadImage(image)
    img = cv.LoadImage(image, cv.CV_LOAD_IMAGE_GRAYSCALE)
    w = img.width
    h = img.height
    #print w,h
    cornerMap = cv.CreateMat(h,w,cv.CV_32FC1)
    print cornerMap
    #Harris Corner Detection
    cv.CornerHarris(img,cornerMap,2)

    corners = []
    #Recorriendo toda la imagen
    for x in range(0, h):
        for y in range(0, w):
            harris = cv.Get2D(cornerMap, x, y)
            #Validar la respuesta de deteccion de esquinas 
            if harris[0] > 10e-06:
                #Dibujar un circulo en la imagen original
                cv.Circle(img_or,(y,x),2,cv.RGB(155, 155, 25))
                corners.append([y,x])
                
    #Muestra la imagen y la guarda
    cv.ShowImage('Harris', img_or)
    cv.SaveImage('harris.jpg', img_or)
    cv.WaitKey()                

    return corners, img


#Ya teniendo los puntos de interes en cada una de las imagenes el paso que sigue
#es obtener los descriptores de cada uno de estos puntos, los descriptores
#son vectores que describen la apariencia de la imagen en un punto dado, esto
#sirve para obtener los puntos semejantes de las diferentes imagenes
def get_descriptors_(image,corners,wid=6):
 
    des = []
    
    for coords in corners:
        data = image[coords[0]-wid:coords[0]+wid+1,
                      coords[1]-wid:coords[1]+wid+1].flatten()
        des.append(data)

    return des

#Ahora se necesita obtener los puntos en comun de una imagen y otra con ayuda de 
#los descriptores, para cada punto descriptor de la primera imagen se selecciona 
#un punto description de la segunda imagen
def match(des1, des2, threshold=0.4):
    l = len(des1[0])
    match = -ones((len(des1),len(des2)))
    for i in range(len(des1)):
        for j in range(len(des2)):
            m1 = (des1[i] - mean(des1[i])) / std(des1[i])
            m2 = (des2[j] - mean(des2[j])) / std(des2[j])
            value = sum(m1 * m2) / (num-1)
            if value > threshold:
                match[i,j] = value
    idx = argsort(-match)
    matches = idx[:,0]
    return matches

    
#Esta funcion une los puntos que se obtuvieron en la funcion match para
#asi unir estas semejanzas por medio de lineas con ayuda de la libreria pylab 
def plot_matches(img1,img2,coords1,coords2,matches):
    nwim = appendimages(img1,img2)
    nwim = vstack((nwim,nwim))
    pylab.imshow(im3)
    y = im1.shape[1]
    for i,m in enumerate(matchscores):
        if m>0:
            pylab.plot([coords1[i][1],coords2[m][1]+y],[coords1[i][0],coords2[m][0]],'b')
    pylab.axis('off')
    pylab.show()
def main():

    for z in range(1):
        letra = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        #img = "letras/"+letra[z]+".png"
        img = argv[1]
        #print("1"+letra[z])
        #img_ = argv[2]
        wid = 5
        threshold=0.4
        im = array(Image.open(img).convert('L'))
        #im1 = array(Image.open(img_).convert('L'))
        corners, imagen1 = corner_detection(img)
        #corners_, imagen2 = corner_detection(img_)

        esquinas = {}

        #print corners[0]

        distancia = 5

        for x in range(0,len(corners)):

            add(corners[x],esquinas,distancia)
        
        if(len(esquinas)>0):
            centros = [centro(esquinas[0])]
            for k in range(1,len(esquinas)):
                centros.append(centro(esquinas[k]))
        else:
            centros = [(1,1),(1,2),(2,2)]

        print_esquinas(centros,img,distancia)

        #guardar_esquinas(centros,letra[z])

        print leer_letra(centros)

        #des1 = get_descriptors_(im,corners,wid+1)

        #des2 = get_descriptors_(im1,corners_,wid+1)

        #matches = match(esquinas,esquinas,threshold)
        #plot_matches(img1,img2,corners,corners_,matches)
      

if __name__ == '__main__':
    main()
