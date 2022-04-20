import os
fs=os.sep
import circulos as finder
import red as rn
import tkinter as tk
from tkinter import filedialog, messagebox
from glob import glob
import numpy as np

global rutaAbrir
class Ventana(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()

	#Creamos lo objetos en la ventana, usamos grid para posicionar los objetos en ella
	def create_widgets(self):
		#Creamos un label
		self.hi_there = tk.Label(self)
		self.hi_there["text"] = "Seleccione una Imagen"
		self.hi_there.grid(row=1, column=1)
		#Creamos un botón
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Seleccionar Imagen"
		self.hi_there["command"] = self.selImg
		self.hi_there.grid(row=1, column=3)
		#Creamos el botón de salir
		self.quit = tk.Button(self, text="Cerrar", bg="red", command=root.destroy)
		self.quit.grid(row=3, column=2)
	
	####### Métodos para los botones ######
	def selImg(self):
		#Mostramos un dialogo para seleccionar la fotografía a analizar
		rutaAbrir =  filedialog.askopenfilename(initialdir = "./",title = "Seleccione una Imágen a Analizar",filetypes = (("Imágenes JPG",("*.jpg","*.jpeg")),("Imágenes PNG","*.png"),("Todos los archivos","*.*")))
		#Analizamos la imágen buscando la fruta, y guardamos el resultado en la carpeta desde donde se ejecuta el programa como 'temporal.jpg'
		finder.ejecutar(rutaAbrir,'./temporal.jpg')
		#Analizamos en la RNA la fotografía
		resultado=rn.evaluar('./temporal.jpg')
		#Redondeamos a enteros los resultados de la RNA y la dividimos en 3 variables (el resultado es un arreglo de 3 posiciones)
		resultado=np.around(resultado)
		x1=int(resultado[0])
		x2=int(resultado[1])
		x3=int(resultado[2])
		#Comprobamos los resultados
		if(x1!=1 and x2!=1 and x3==1):
			messagebox.showinfo("Resultado", "Es de Etapa 1, aprox. 2 semanas restantes")
		elif(x1!=1 and x2==1 and x3!=1):
			messagebox.showinfo("Resultado", "Es de Etapa 2, aprox. 1 semana restante")
		elif(x1==1 and x2!=1 and x3!=1):
			messagebox.showinfo("Resultado", "Es de Etapa 3, aprox. 3 dias restantes")
		else:
			messagebox.showinfo("Resultado", "ERROR Encontrado")
#Declaramos la ventana y le ponemos titulo		
root = tk.Tk()
root.title("Analizador de Imágenes de Tomates")
#Ponemos la ventana 200 píxeles desplazada en ambos ejes para que no quede pegada al marco de la pantalla
root.geometry("+200+200")
#Creamos la ventana como un objeto
app = Ventana(master=root)
#Mostramos la ventana
app.mainloop()
