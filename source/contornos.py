#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
#mpl.use('Qt4Agg')
import numpy as np
import os

def encontrarContornoMayor(vectorContornos):
	"""Encuentra el contorno con la mayor cantidad de puntos"""
	pocContorno=0
	tamContorno=0.
	for i in range(len(vectorContornos)):
		if(cv2.contourArea(vectorContornos[i])>tamContorno):
			pocContorno=i
			tamContorno=cv2.contourArea(vectorContornos[i])
		pass
	return [vectorContornos[pocContorno]]

fs=os.sep
imagen=cv2.imread('.'+fs+'Resources'+fs+'Etapas'+fs+'2.jpg')

#cv2.imshow("Original",imagen)

grises=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
tamMatriz=3#7
gaussiana = cv2.GaussianBlur(grises, (tamMatriz, tamMatriz), 0)


puntoMedio=127#127
desviacion=16#16
canny = cv2.Canny(gaussiana, puntoMedio-desviacion, puntoMedio+desviacion)

(imgModificada, contornos,jerarquia) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Mostramos el número de monedas por consola
print("He encontrado {} objetos".format(len(contornos)))


contornoMayor=encontrarContornoMayor(contornos)
print ("Area",cv2.contourArea(contornoMayor[0]))


#cv2.imshow('Grises',grises)
#cv2.imshow('Gaussiana',gaussiana)
cv2.imshow('Canny',canny)
#cv2.imshow('Contorno mayor',contornoMayor)


cv2.drawContours(imagen,contornoMayor,-1,(128,0,0), 2)
#cv2.drawContours(imagen,contornos,-1,(0,0,0), 2)
cv2.imshow("Contornos", imagen)


cv2.waitKey(0)
cv2.destroyAllWindows()
