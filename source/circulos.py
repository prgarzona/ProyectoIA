#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def encontrarCirculoMayor(vectorCirculos):
	"""Encuentra el contorno con la mayor cantidad de puntos"""
	pocRadio=0
	tamRadio=0.
	#Iteramos cad circulo en el vector
	for i in range(len(vectorCirculos[0])):
		#El primer radio es la posicion 0 del vector, luego vamos comparando uno a uno hasta encontrar el más grande
		radio=vectorCirculos[0][i][2]
		if(radio>tamRadio):
			pocRadio=i
			tamRadio=radio
	return [[vectorCirculos[0][pocRadio]]]
	
def recortarImagen(imagen, circulo):
	"""Recorta una imágen en base a el circulo donde se encuentra el tomate"""
	#Obtenemos el centro y radio del circulo
	xBase=int(circulo[0][0][0])
	yBase=int(circulo[0][0][1])
	radio=int(circulo[0][0][2])
	
	#Obtenemos las dimensiones de la imágen
	yOriginal=len(imagen)
	xOriginal=len(imagen[0])
	
	#Sumamos en X e Y el radio para obtener los límites del círculo
	xMin=xBase-radio
	xMax=xBase+radio
	yMin=yBase-radio
	yMax=yBase+radio
	#Comprobamos que el circulo no salga de los límites de la imágen, si lo hace ponemos el recorte en el borde de la imágen
	if(xMin<0):
		xMin=0
	if(yMin<0):
		yMin=0
	if(xMax>xOriginal):
		xMax=xOriginal
	if(yMax>yOriginal):
		yMax=yOriginal
	
	#Al estar como array de numpy la imágen, solo recortamos la matriz	
	return imagen[yMin:yMax,xMin:xMax]

def ejecutar(imagen, salida):
	try:
		#Ruta de salida de la imágen 
		rutaRecorte=salida
		#Abrimos la imágen
		img=cv2.imread(imagen)
		#Le aplicamos un median blur con un suavizado de 11px
		src = cv2.medianBlur(img,11)
		#Transformamos la imagen a escala de grises
		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		#Buscamos los círculos en la imágen, param1 y param2 son los umbrales del filtro Canny
		circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=19, minRadius=0, maxRadius=0)
		#Encontramos el círculo más grande
		mayor=encontrarCirculoMayor(circles)
		#Redondeamos todos los píxeles del círculo a enteros
		circulo = np.uint16(np.around(mayor))
		#Recortamos la imágen conforme el círculo
		recorte=recortarImagen(img,circulo)
		#Guardamos la imágen recortada
		cv2.imwrite(rutaRecorte,recorte)
		return recorte
	except cv2.error:
		#Devolvemos error en caso de error en cv2, que es generalmente por que la ruta de la imágen no existe
		raise Exception('El archivo '+str(imagen)+' no existe')
