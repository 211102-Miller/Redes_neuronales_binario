from tkinter import E
import numpy as np

#Bias o sesgo
bias = 1

#Nuestra matriz x1,x2 y yd donde yd es nuestra yd
matriz = np.array([[0, 0],
                   [1, 1],
                   [0, 1],
                   [1, 1]])
print("matriz inicial","\n",matriz)


#se una nuestro bias con la matriz incial
columna_unos = np.ones((matriz.shape[0], 1)) * bias
matriz_con_bias = np.hstack((columna_unos, matriz))                   
print("matriz con el bias","\n",matriz_con_bias)

#nuestra ye deciada
yd = np.array([[0],
                   [1],
                   [1],
                   [1]])

#margen de error
erro = 0

#tasa de aprendizaje o eta
n = 0.5

#longitud de nuestra columnas para sacar el peso
num_columnas = matriz_con_bias.shape[1]
#nuestros pesos por cada caracteristica
w = np.random.randint(low=0, high=10, size=(num_columnas, 1))
print("pesos","\n",w)

cantidad_iteraciones = 300


#arreglos con mis datos
contador = 0
diccionario = {}

datos_iteraciones = []
 
for i in range(cantidad_iteraciones):
    
    #sacar nuestra U
    u =np.dot(matriz_con_bias, w)
    print("resultado de nuestra u","\n",u)

    #Sacamos nuestra y calcuclada
    # Crear una matriz nueva con la misma longitud que seria nuestra y calculada
    yc = np.zeros_like(u)

    # Aplicar la condición para reemplazar los valores mayores a 1 por 1
    yc[u >= 1] = 1

    # Aplicar la condición adicional para reemplazar los valores menores o iguales a 0 por 0
    yc[u < 0] = 0
    print("resultado de nuestra yc","\n",yc)

    #sacamos nuestro error
    e = yd - yc
    print("error","\n",e)


    #para sacar delta junto w
    # Eliminar la última fila de la matriz
    error_actualizado = np.delete(e, -1, axis=0)
    #multiplica tdoas la filasd de la matriz
    triangulo_y_w = error_actualizado * n
    print("resultado de w y delta","\n", triangulo_y_w)

    #sacar nuestra nueva w
    nueva_w= w + triangulo_y_w

    w = nueva_w
    print("Nueva w ","\n",w)

    w_convertida = w.tolist()
    nueva_w_convertida = nueva_w.tolist()
    datos_iteracion = [w_convertida,n,nueva_w_convertida,"aa"]
    datos_iteraciones.append(datos_iteracion)

    contador +=1

    if np.all(e == 0):
        cantidad_iteraciones = 0
        print("se acabo")
        break



diccionario ={
    str(contador) : datos_iteraciones
}

print(diccionario)








