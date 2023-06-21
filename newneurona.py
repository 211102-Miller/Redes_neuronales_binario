from tkinter import E
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import csv
import math as m


#Archivo donde se sacan las X y se ponen en una matriz
def valoresX(filename):
    matrix = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Saltar la primera fila de encabezados
        for row in reader:
            data = [float(row[i]) for i in range(1, 4)]
            matrix.append(data)  # Ignorar la columna de ID
    return matrix
# Nombre del archivo CSV
filename = '211102.csv'
# Leer los datos del archivo y almacenarlos en una matriz
data_matrix = valoresX(filename)
x = np.array(data_matrix)

#Archivo donde se sacan la Y desiada
def valoresY(filename):
    matrix = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Saltar la primera fila de encabezados
        for row in reader:
            data = [float(row[4])]
            matrix.append(data)  # Ignorar la columna de ID
    return matrix
# Nombre del archivo CSV
filename = '211102.csv'
# Leer los datos del archivo y almacenarlos en una matriz
data_matrixY = valoresY(filename)
yd = np.array(data_matrixY)


#se declaran las variables que se usaran
bias = 1 #nuestro bias o sesgo
error = 1 #el margen de error
n= 0.0000001
#0.00000002 # tasa de aprendisaje o eta
cantidad_iteraciones = 100000000000


#Se une nuestro bias con nuestras x
def union_bias_x (x,bias):
    columna_bias =np.ones((x.shape[0],1)) * bias
    matrix_con_bias = np.hstack((columna_bias,x))
    return matrix_con_bias
resultado_bias_x = union_bias_x(x,bias)
#print(resultado_bias_x)

#Se generan los pesos iniciales
def genera_pesos(resultado_bias_x):
    num_columnas = resultado_bias_x.shape[1]
    w = np.random.randint(low=-5, high=5, size=(num_columnas, 1))
    return w
resultado_pesos =  genera_pesos(resultado_bias_x)
#print(resultado_pesos)


#declaramos nuestros arreglos para guardar los datos
contador = 0 #para saber el numero de generaciones
datos = [] #guardamos todos nuestros datos requeridos
toleranciaError = []

    

for i in range(cantidad_iteraciones):
    
    #sacamos nuestra U
    def sacar_u(resultado_bias_x,resultado_pesos):
        u = np.linalg.multi_dot([resultado_bias_x,resultado_pesos])
        return u
    resultado_u = sacar_u(resultado_bias_x,resultado_pesos)
    #print("resultado de U","\n",resultado_u)

    #funcion de activacion f(x) = x
    def activacion(x):
        return x
    resultado_activacion = activacion(resultado_u)
    #print("Funcion de activacion","\n",resultado_activacion)

    #Calculamos nuestros errores  
    def calculamos_error(yd,resultado_activacion):
        e = yd - resultado_activacion
        return e
    resultado_error = calculamos_error(yd,resultado_activacion)
    #print("error","\n",resultado_error)

    #Sacamos nuestra tolerancia de error
    def torera_error(resultado_error):

        aux = 0

        long= len(resultado_error)
        for i in range(len(resultado_error)):
            aux = aux + resultado_error[i]**2
        mse = aux / long
        rmse = m.sqrt(mse)

        tolerancia = np.sum(np.abs(resultado_error))
        toleranciaError.append(tolerancia)
        return rmse
    tolera = torera_error(resultado_error)
    print("tolerancia de error",tolera)

    #traspuesta de error - investigar 

    def delta_w (n,resultado_error,resultado_bias_x,resultado_pesos):
        error = np.transpose(resultado_error)
        for i in range(len(resultado_pesos)):
            error_por_x = np.linalg.multi_dot([error,resultado_bias_x])
        multi = n * error_por_x   
        return multi
    resultado_delta = delta_w(n,resultado_error,resultado_bias_x,resultado_pesos)

    #Se hace la suma para el nuevo peso
    def nueva_peso(resultado_pesos,resultado_delta):
        pesos = np.reshape(resultado_pesos, (1, -1))
        nuevo =pesos + resultado_delta
        nuevo_nuevo = np.reshape(nuevo, (-1, 1))
        return nuevo_nuevo
    resultado_nuevo_peso = nueva_peso(resultado_pesos,resultado_delta)
    #print("nuevos pesos",resultado_nuevo_peso)

    #Pasmos
    converida_peso = resultado_pesos.tolist()
    convertida_nuevo_peso = resultado_nuevo_peso.tolist()
    datos_iteraciones = contador,converida_peso,n,convertida_nuevo_peso,tolera
    datos.append(datos_iteraciones)

    #Se pasa el nuevo peso para la siguiente iteracion
    resultado_pesos = resultado_nuevo_peso

    contador +=1

    if tolera <= error:
        break

print(toleranciaError[-1])

def create_table(datos_iteraciones):
    
    root = tk.Tk()

    table = ttk.Treeview(root)

    # Definir las columnas
    table['columns'] = ('Columna 1', 'Columna 2', 'Columna 3','Columna 4','Columna 5')

    # Formato de las columnas
    table.column('#0', width=0, stretch=tk.NO)
    table.column('Columna 1', anchor=tk.CENTER, width=50)
    table.column('Columna 2', anchor=tk.CENTER, width=500)
    table.column('Columna 3', anchor=tk.CENTER, width=50)
    table.column('Columna 4', anchor=tk.CENTER, width=500)
    table.column('Columna 5', anchor=tk.CENTER, width=200)

    # Encabezados de las columnas
    table.heading('#0', text='', anchor=tk.CENTER)
    table.heading('Columna 1', text='Iteracion', anchor=tk.CENTER)
    table.heading('Columna 2', text='Peso inicial', anchor=tk.CENTER)
    table.heading('Columna 3', text='Eta', anchor=tk.CENTER)
    table.heading('Columna 4', text='Peso final', anchor=tk.CENTER)
    table.heading('Columna 5', text='Tolerancia de error', anchor=tk.CENTER)


    # Agregar filas a la tabla
    for i, item in enumerate(datos_iteraciones[-100:]):
        table.insert(parent='', index='end', iid=i, text='', values=(str(item[0]), str(item[1]), str(item[2]),str(item[3]),str(item[4])))

    
    # Graficar los datos
    plt.plot(toleranciaError)

    # Mostrar el gráfico
    table.pack()
    plt.show()
    root.mainloop()
    

    
create_table(datos)