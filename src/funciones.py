
def porcentaje_viviendas_prop():
    import os
    import sys

    #files_path = os.path.abspath("../files")
    #print(f"Adding files path: {files_path}")
    #sys.path.append(files_path)

    path_file = '../files/usu_hogar_T324.txt'
    #--------------------------------------------------------
    #IMPORTANTE el indice de las columnas empieza en 0
        #refeenciar a las colunas correctas lo puedo arreglar accediend al archivo como si fuera un dicc 
    #--------------------------------------------------------
    import csv
    dicc_aglomerado = {}

    #"""
    index_pondera = 8
    index_aglomerado = 7   #AGLOMERADO N2 los codigos varian de 02 a 93
    index_baño = 20    #IV8 N1 1=tiene baño, 2= no tiene baño
    index_cant_miembros = 65    #IXTot N2 cantidad de miembros del hogar
    
    
    with open (path_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        
        encabezado = next(reader)  # Skip header row

        for row in reader:  #itera sobre row, accediendo a cada columna
            
            if int(row[index_cant_miembros]) > 2 and int(row[index_baño]) == 2: #prop del terreno y vivienda
                
                if int(row[index_aglomerado]) in dicc_aglomerado:
                    dicc_aglomerado[int(row[index_aglomerado])] += int(row[index_pondera])
                else:
                    dicc_aglomerado[int(row[index_aglomerado])] = int(row[index_pondera])
    
    
    """
    with open(path_file, encoding="latin1") as archivo: ##Modo r para solo lectura
        reader = csv.DictReader(archivo, delimiter=";") #Cada row es un diccionario con los datos de esa row
        
        for row in reader:
            try:
                aglom = int(row["AGLOMERADO"]) #Aglomerado
                pondera = int(row["PONDERA"])
                baños = int(row["IV8"])
                cant_miembros = int(row["IX_TOhT"])
            except (ValueError, KeyError):  
                continue    # Si hay algún error con los datos, lo saltamos

    #Condicion para contar los aglomerados que tienen 2 baños y mas de 2 miembros
            if cant_miembros > 2 and baños ==2:
                #Acumula los datos de los aglomerados en el diccionario vacio  
                if aglom in dicc_aglomerado:
                    dicc_aglomerado[aglom] += pondera
                else:
                    dicc_aglomerado[aglom] = pondera
    """
    return dicc_aglomerado                

dicc_agl = porcentaje_viviendas_prop()      
print(dicc_agl)

if dicc_agl: #Verifica si el diccionario no esta vacio
    aglom_mayor= max(dicc_agl, key=dicc_agl.get) #Busca el aglomerado con mayor cantidad de personas
    aglom_menor= min(dicc_agl, key=dicc_agl.get) #Busca el aglomerado con menor cantidad de personas
    
    print("El aglomerado con mayor cantidad de personas es:", aglom_mayor, "con", dicc_agl[aglom_mayor], "personas")
    print("El aglomerado con menor cantidad de personas es:", aglom_menor, "con", dicc_agl[aglom_menor], "personas")
    


