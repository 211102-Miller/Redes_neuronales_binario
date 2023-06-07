from tkinter import E
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import csv


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

#Archivo donde se sacan la Y desiasda
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
error = 0 #el margen de error
n= 0.0002 # tasa de aprendisaje o eta
cantidad_iteraciones = 5


#Se une nuestro bias con nuestras x
def union_bias_x (x,bias):
    columna_bias =np.ones((x.shape[0],1)) * bias
    matrix_con_bias = np.hstack((columna_bias,x))
    return matrix_con_bias
resultado_bias_x = union_bias_x(x,bias)
print(resultado_bias_x)

#Se generan los pesos iniciales
def genera_pesos(resultado_bias_x):
    num_columnas = resultado_bias_x.shape[1]
    w = np.random.randint(low=0, high=10, size=(num_columnas, 1))
    return w
resultado_pesos =  genera_pesos(resultado_bias_x)
print(resultado_pesos)


#declaramos nuestros arreglos para guardar los datos
contador = 0 #para saber el numero de generaciones
datos = [] #guardamos todos nuestros datos requeridos
toleranciaError = []

for i in range(cantidad_iteraciones):
    
    #sacamos nuestra U
    def sacar_u(resultado_bias_x,resultado_pesos):
        u = np.dot(resultado_bias_x,resultado_pesos)
        return u
    resultado_u = sacar_u(resultado_bias_x,resultado_pesos)
    print("resultado de U","\n",resultado_u)

    #funcion de activacion f(x) = x
    def activacion(x):
        return x
    resultado_activacion = activacion(resultado_u)
    print("Funcion de activacion","\n",resultado_activacion)

    #Calculamos nuestros errores  
    def calculamos_error(yd,resultado_activacion):
        e = yd - resultado_activacion
        return e
    resultado_error = calculamos_error(yd,resultado_activacion)
    print("error","\n",resultado_error)

    #Sacamos nuestra tolerancia de error
    def torera_error(resultado_error):
        tolerancia = np.sum(np.abs(resultado_error))
        toleranciaError.append(tolerancia)
        return tolerancia
    tolera = torera_error(resultado_error)
    print("tolerancia de error",tolera)

    pesos_requeridos = resultado_pesos.shape[0] # Sacamos la longitud de los pesos

    #ajustamos nuesta longid de nuestro error para nuestros nuevos pesos
    def ajustar_longitud(matriz, longitud_objetivo):
        if matriz.shape[0] > longitud_objetivo:
            matriz = matriz[:longitud_objetivo]
        elif matriz.shape[0] < longitud_objetivo:
            diferencia = longitud_objetivo - matriz.shape[0]
            filas_faltantes = np.zeros((diferencia, matriz.shape[1]))
            matriz = np.concatenate((matriz, filas_faltantes), axis=0)
        return matriz
    resultado_ajuste = ajustar_longitud(resultado_error,pesos_requeridos)
    print("Resultado del ajuste",resultado_ajuste)

    def delta_w (n,resultado_ajuste):
        eta_delta = n * resultado_ajuste
        return eta_delta
    resultado_delta = delta_w(n,resultado_ajuste)
    print("resultado de delta",resultado_delta)

    #Se hace la suma para el nuevo peso
    def nueva_peso(resultado_pesos,resultado_delta):
        nuevo = resultado_pesos + resultado_delta
        return nuevo
    resultado_nuevo_peso = nueva_peso(resultado_pesos,resultado_delta)
    print(resultado_nuevo_peso)

    #Pasmos
    converida_peso = resultado_pesos.tolist()
    convertida_nuevo_peso = resultado_nuevo_peso.tolist()
    datos_iteraciones = contador,converida_peso,n,convertida_nuevo_peso,tolera
    datos.append(datos_iteraciones)

    #Se pasa el nuevo peso para la siguiente iteracion
    resultado_pesos = resultado_nuevo_peso

    contador +=1

print(datos)
print(toleranciaError)


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
    for i, item in enumerate(datos_iteraciones):
        table.insert(parent='', index='end', iid=i, text='', values=(str(item[0]), str(item[1]), str(item[2]),str(item[3]),str(item[4])))

    table.pack()
    # Graficar los datos
    plt.plot(toleranciaError)

    # Mostrar el gráfico
    

    plt.show()
    root.mainloop()

create_table(datos)