import os
import sys

#sys.path.append(os.path.abspath("../files"))

# Obtener el directorio actual de ejecución
current_directory = os.getcwd()
print("El directorio actual es:", current_directory)

#uno de las primeras pruebas de manejo de paths y abrir archivos csv

path_file = 'files/usu_hogar_T324.txt'
index_pondera = 9
index_tenencia = 37

import csv
print(path_file)

with open (path_file, encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    encabezado = next(reader)  # Skip header row
    suma_propietarios = 0
    suma_total = 0

    for row in reader:  #itera sobre fila, accediendo a cada columna
        if int(row[index_tenencia]) == 1: #prop del terreno y vivienda
            suma_propietarios += int(row[index_pondera])
        suma_total += int(row[index_pondera])

        

porcentaje = (suma_propietarios / suma_total) * 100
print('suma total de encuestados: ',suma_total)
print('suma de propietaios vivienda y terreno: ',suma_propietarios)

print('porcentaje de prop: ',porcentaje)

