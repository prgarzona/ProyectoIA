#!/usr/bin/env python
# -*- coding: utf-8 -*-



from PIL import Image #biblioteca para abrir y escalar imagenes, manipular y guardar muchos formatos de archivo de imagen diferentes
from glob import glob #bibilioteca utilizada para iterar entre los archivos de una biblioteca
from numpy import array 
from fann2 import libfann # biblioteca para entrenar la RNA, Enlaces de Python para redes neuronales artificiales rápidas
import time

imagenes = [] #almacena las iamgenes de entrada, por defecto esta vacio y se va llenando conforme la red aprende
esperados = [] #almacena los resultados esperados,por defecto esta vacio y se va llenando conforme la red aprende

#Funcion que calcula en cuanto tiempo se entrena la red segun el numero de iteraciones que coloquemos
#se deja especificado todas las conversiones correspondientes
def calcularTiempo(tiempoEnSegundos):
	segundos=int(tiempoEnSegundos)
	minutos=0
	horas=0
	dias=0
	if(tiempoEnSegundos>59):
		minutos=segundos//60
		segundos=segundos%60
		if(minutos>59):
			horas=minutos//60
			minutos=minutos%60
			if(horas>23):
				dias=horas//24
				horas=horas%24
	return [dias,horas,minutos,segundos]

#Esta funcion lo que obtiene  es la informacion de las fotogracias que se encuentran en la carpeta Resources/recortadas la cual 
#incluye fotografias de distintos angulos y distintos tomates para que vaya aprendiendo el reconocimiento
def getdata():
	"""Funcion encargada de obtenes los datos para el entrenamientos ubicados en ./Resources/recortadas"""
	#importamos las variables globales
	global imagenes 
	global esperados
	#Primero obtenemos los errores y esperamos que nos regrese todas o la mayoria de banderas levantadas
	for imagen in glob("./Resources/recortadas/error/*.jpg"):
		nueva  = Image.open(imagen) #abrimos la imagen que se estara utilizando para entrenar la red
		#la escalamos a conveniencia, para no perder resolucion y obtener suficiente informacion
		#como comentario se escala a 50,50 para que no se demore demasiado en cada epoca/iteracion de la red
		nueva = nueva.resize((50,50)) 
		#creamos una lista por ser RGB la lista contine arreglos de pixeles con valores RGB por lo caual los separamos
		#se pasan a blanco y negro para poder optimizar el aprendizaje de la red
		arreglo = list(nueva.getdata()) 
		esperados.append([1,1,1]) #agregamos los esperados, de lo que necesitamos para que aprenda a red
		tmep = []
		for x in arreglo:
			tmep.append(x[0])
			tmep.append(x[1])
			tmep.append(x[2])
			pass
		tmep.append(50)
		imagenes.append(tmep) # lo agregamos a la lista de imagenes 
		pass
	#luego el mismo procedimiento para las etapas 1,2 y 3
	for imagen in glob("./Resources/recortadas/1/*.jpg"):
		nueva  = Image.open(imagen)
		nueva = nueva.resize((50,50))
		arreglo = list(nueva.getdata())
		esperados.append([0,0,1])
		tmep = []
		for x in arreglo:
			tmep.append(x[0])
			tmep.append(x[1])
			tmep.append(x[2])
			pass
		tmep.append(50)
		imagenes.append(tmep)
		pass
	for imagen in glob("./Resources/recortadas/2/*.jpg"):
		nueva  = Image.open(imagen)
		nueva = nueva.resize((50,50))
		arreglo = list(nueva.getdata())
		esperados.append([0,1,0])
		tmep = []
		for x in arreglo:
			tmep.append(x[0])
			tmep.append(x[1])
			tmep.append(x[2])
			pass
		tmep.append(50)
		imagenes.append(tmep)
		pass
	for imagen in glob("./Resources/recortadas/3/*.jpg"):
		nueva  = Image.open(imagen)
		nueva = nueva.resize((50,50))
		arreglo = list(nueva.getdata())
		esperados.append([1,0,0])
		tmep = []
		for x in arreglo:
			tmep.append(x[0])
			tmep.append(x[1])
			tmep.append(x[2])
			pass
		tmep.append(50)
		imagenes.append(tmep)
		pass


getdata() #ejecutamos lo funcion para obtener los datos




rango_de_conexion = 1 #nos dice que tipo de red se usa y esta es multi capa
variable_entrenamiento = .01 #constante de aprendizaje de la RNA

error_minimo = 0.0001 #definimos el error minimo al que se quiere llegar
iteraciones_maximas = 5 #las iteraciones maximas al entrenar
iteraciones_reporte = 1 #numero de iteraciones por reporte, muestra el listado cada cuanto aparece en consola

red = libfann.neural_net() # creamos la red FANN
red.create_sparse_array(rango_de_conexion, (7501, 2500,3))#le decimos que tipo de red y las neuronas por capa 
red.set_learning_rate(variable_entrenamiento) #le decimos que variable de entrenamiento se desea
red.set_activation_function_output(libfann.SIGMOID_SYMMETRIC) #la funcion a utilizar
datos = libfann.training_data() #creamos la variable para los datos

	
datos.set_train_data(imagenes,esperados) #cargamos los datos de entrenamiento y los esperados

inicio = time.time()
red.train_on_data(datos, iteraciones_maximas, iteraciones_reporte, error_minimo) # entrenamos la red
fin = time.time()

tiempoTotal=fin-inicio
tiempo=calcularTiempo(tiempoTotal)
print ("Se ha entrenado en", tiempo[0], "días",tiempo[1], "horas",tiempo[2],"minutos y",tiempo[3], "segundos")

red.save("RedNeuronalEntrenada") # se guardan los resultados
#Fin de archivo
