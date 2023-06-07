from tkinter import E
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import csv

#Archivo donde se lee las X
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
# Imprimir la matriz
for row in data_matrix:
    print(row)
data_matrix = np.array(data_matrix)

#Archivo donde se lee la Y esperada
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
# Imprimir la matriz
for row in data_matrixY:
    print(row)
data_matrixY = np.array(data_matrixY)


#Bias o sesgo
bias = 1


#se una nuestro bias con la matriz incial
columna_unos = np.ones((data_matrix.shape[0], 1)) * bias
matriz_con_bias = np.hstack((columna_unos, data_matrix))                   
print("matriz con el bias","\n",matriz_con_bias)

#margen de error
erro = 1

#tasa de aprendizaje o eta
n = 0.000000000001

#longitud de nuestra columnas para sacar el peso
num_columnas = matriz_con_bias.shape[1]
#nuestros pesos por cada caracteristica
w = np.random.randint(low=0, high=10, size=(num_columnas, 1))
print("pesos","\n",w)

cantidad_iteraciones = 200


#arreglos con mis datos
contador = 0
diccionario = []
torerancia_error = []
datos_iteraciones = []
 
for i in range(cantidad_iteraciones):
    
    #sacar nuestra U
    u =np.dot(matriz_con_bias, w)
    print("resultado de nuestra u","\n",u)

    """#Sacamos nuestra y calcuclada
    # Crear una matriz nueva con la misma longitud que seria nuestra y calculada
    yc = np.zeros_like(u)

    # Aplicar la condición para reemplazar los valores mayores a 1 por 1
    yc[u >= 1] = 1

    # Aplicar la condición adicional para reemplazar los valores menores o iguales a 0 por 0
    yc[u < 0] = 0
    print("resultado de nuestra yc","\n",yc)"""

    #Funcion de activacion
    yc = np.maximum(0, u)
    print("Nuestra yc ",yc)

    #sacamos nuestro error
    e = data_matrixY - yc
    print("error","\n",e)

    #sacar nuestra tolerancia de error
    tolerancia = np.sum(np.abs(e))
    torerancia_error.append(tolerancia)
    print("tolerancia de error",torerancia_error)


    #para sacar delta junto w
    # Eliminar la última fila de la matriz
    error_actualizado = np.delete(e, -1, axis=0)



    def ajustar_longitud(matriz, longitud_objetivo):
        if matriz.shape[0] > longitud_objetivo:
            matriz = matriz[:longitud_objetivo]
        elif matriz.shape[0] < longitud_objetivo:
            diferencia = longitud_objetivo - matriz.shape[0]
            filas_faltantes = np.zeros((diferencia, matriz.shape[1]))
            matriz = np.concatenate((matriz, filas_faltantes), axis=0)
        return matriz
    

    #ajustamos la longitud de mi error para poder hacer la multiplicacion
    longitud_w = np.array(w)
    longitud_e = np.array(e)

    longitud_requerida = w.shape[0]
    e_ajustada = ajustar_longitud(e, longitud_requerida)
    
    print(e_ajustada)
    #multiplica tdoas la filasd de la matriz
    triangulo_y_w = e_ajustada * n
    print("resultado de w y delta","\n", triangulo_y_w)

    #sacar nuestra nueva w
    nueva_w= w + triangulo_y_w

    w_convertida = w.tolist()
    nueva_w_convertida = nueva_w.tolist()
    datos_iteracion = contador,w_convertida,n,nueva_w_convertida,tolerancia
    datos_iteraciones.append(datos_iteracion)

    w = nueva_w
    print("Nueva w ","\n",w)

    contador +=1

    if np.all(e == 0):
        cantidad_iteraciones = 0
        print("se acabo")
        break




print(datos_iteraciones)


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
    plt.plot(torerancia_error)

    # Mostrar el gráfico
    

    plt.show()
    root.mainloop()

create_table(datos_iteraciones)








