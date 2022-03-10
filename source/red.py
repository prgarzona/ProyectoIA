from fann2 import libfann # biblioteca para entrenar la RNA, Enlaces de Python para redes neuronales artificiales rápidas
from glob import glob #bibilioteca utilizada para iterar entre los archivos de una biblioteca
from PIL import Image #biblioteca para abrir y escalar imagenes, manipular y guardar muchos formatos de archivo de imagen diferentes

#Funcion para comparar las fotografias "nuevas" que se carguen, con lo aprendido en la neurona que seria el archivo
#RedNeuronalEntrenada

def evaluar(imagen):
	#Cargamos la red neuronal ya entrenada
	ann = libfann.neural_net()
	ann.create_from_file("RedNeuronalEntrenada")
	#Abrimos la imágen
	nueva  = Image.open(imagen)
	#Redimensionamos la imágen a 50x50px y lo pasamos a una lista, donde cada elemto es un píxel [r,g,b]
	#el tamaño 50,50 es para que el proceso de comparacion sea mas rapido 
	nueva = nueva.resize((50,50))
	arreglo = list(nueva.getdata())
	tmep = []
	#Vectorizamos completamente el arreglo de la imágen
	for x in arreglo:
		tmep.append(x[0])
		tmep.append(x[1])
		tmep.append(x[2])
	tmep.append(50)#Indica que la imágen es de 50x50px, para que la red vaya obteniendo los valores de 50 en 50
	return ann.run(tmep)
