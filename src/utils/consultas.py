import csv 

mapeo_aglomerados = {
    '2': 'Gran La Plata',
    '3': 'Bahía Blanca-Cerri',
    '4': 'Gran Rosario',
    '5': 'Gran Santa Fe',
    '6': 'Gran Paraná',
    '7': 'Posadas',
    '8': 'Gran Resistencia',
    '9': 'Comodoro Rivadavia-Rada Tilly',
    '10': 'Gran Mendoza',
    '12': 'Corrientes',
    '13': 'Gran Córdoba',
    '14': 'Concordia',
    '15': 'Formosa',
    '17': 'Neuquén-Plottier',
    '18': 'Santiago del Estero-La Banda',
    '19': 'Jujuy-Palpalá',
    '20': 'Río Gallegos',
    '22': 'Gran Catamarca',
    '23': 'Gran Salta',
    '25': 'La Rioja',
    '26': 'Gran San Luis',
    '27': 'Gran San Juan',
    '29': 'Gran Tucumán-Tafí Viejo',
    '30': 'Santa Rosa-Toay',
    '31': 'Ushuaia-Río Grande',
    '32': 'Ciudad Autónoma de Buenos Aires',
    '33': 'Partidos del Gran Buenos Aires',
    '34': 'Mar del Plata',
    '36': 'Río Cuarto',
    '38': 'San Nicolás-Villa Constitución',
    '91': 'Rawson-Trelew',
    '93': 'Viedma-Carmen de Patagones'
}




def obtener_nombre_aglomerado(codigo):
    """Devuelve el nombre del aglomerado dado su código"""

    return mapeo_aglomerados.get(str(codigo), f"Desconocido ({codigo})")

def leer_archivos(archivo_csv):
    """Lee el archivo CSV y lo devuelve como una lista de diccionarios."""

    with open(archivo_csv, newline='', encoding='utf-8') as entrada:
        #
        lector = csv.DictReader(entrada, delimiter=';')
        return [fila for fila in lector]  # Devuelve todas las filas como diccionarios
 
##---------------------------------------------------------Inciso 1---------------------------------------------------------------------------
   
def analizar_alfabetizacion(datos_csv):
    " ""Calcula el porcentaje de alfabetización por año."""
    conteo_anual = {}
    lector = leer_archivos(datos_csv)
          
    for fila in lector:
        try:
    # Obtener y convertir valores
            edad = int(fila['CH06'])
            ano = int(fila['ANO4'])
            trimestre = int(fila['TRIMESTRE'])
            alfabetizacion = int(fila['CH09'])
            pondera = int(fila['PONDERA'])
                
           # Solo considerar mayores de 6 años y último trimestre (4)
            if edad > 6 and trimestre == 4:      
           # Inicializar año si no existe
                if ano not in conteo_anual:
                    conteo_anual[ano] = {
                        'alfabetizados': 0,
                        'no_alfabetizados': 0,
                        'total': 0
                    }
                    
                    # Contar según condición de alfabetización (usando ponderación)
                if alfabetizacion == 1:  # Sabe leer y escribir
                    conteo_anual[ano]['alfabetizados'] += pondera
                elif alfabetizacion == 2:  # No sabe leer y escribir
                    conteo_anual[ano]['no_alfabetizados'] += pondera
                    
                conteo_anual[ano]['total'] += pondera
                    
        except (ValueError, KeyError):
            continue

    # Calcular porcentajes y preparar resultados
    resultados = []
    for ano in sorted(conteo_anual.keys()):
        datos = conteo_anual[ano]
        total = datos['total']
        
        if total > 0:
            porc_alfab = (datos['alfabetizados'] / total) * 100
            porc_no_alfab = (datos['no_alfabetizados'] / total) * 100
        else:
            porc_alfab = porc_no_alfab = 0.0
        
        resultados.append({
            'Año': ano,
            'Alfabetizado (%)': round(porc_alfab, 2),
            'No Alfabetizado (%)': round(porc_no_alfab, 2),
            'Total Ponderado': datos['total']
        })
    
    return resultados

def mostrar_resultados(resultados):
    """Muestra los resultados de alfabetización en formato tabular."""

    print("\nResultados de Alfabetización (Mayores de 6 años, último trimestre de cada año):")
    print("-" * 85)
    print(f"{'Año':<10} | {'Alfabetizado (%)':<18} | {'No Alfabetizado (%)':<18} |")
    print("-" * 85)
    
    for res in resultados:
        print(f"{res['Año']:<10} | {res['Alfabetizado (%)']:<18.2f} | {res['No Alfabetizado (%)']:<18.2f} |")


##---------------------------------------------------------Inciso 2 ---------------------------------------------------------------------------
def solicitar_ano():
    while True:
        try:
            ano = int(input("Ingresá el año (mayor a 2003): "))
            if ano > 2003:
                return ano
            else:
                print("El año debe ser mayor a 2003.")
        except ValueError:
            print("Por favor, ingresá un número válido.")

def solicitar_trimestre():
    while True:
        try:
            trimestre = int(input("Ingresá el trimestre (1 a 4): "))
            if trimestre in [1, 2, 3, 4]:
                return trimestre
            else:
                print("El trimestre debe ser 1, 2, 3 o 4.")
        except ValueError:
            print("Por favor, ingresá un número válido.")

def analizar_extranjero_universitarios (datos_csv, ano_elegido, trimestre_elegido):
    """Calcula el porcentaje de personas no nacidas en Argentina con nivel universitario o superior para un año y trimestre igresados."""
   
    total_extranjeros = 0
    universitarios_extranjeros = 0
    lector = leer_archivos(datos_csv)
    for fila in lector:
        try:
            if (int(fila['CH15']) in [4, 5] and 
                int(fila['ANO4']) == ano_elegido and 
                int(fila['TRIMESTRE']) == trimestre_elegido):
                    total_extranjeros += int(fila['PONDERA'])
                    if fila['NIVEL_ED_str'] == "Superior o universitario":
                        universitarios_extranjeros += int(fila['PONDERA'])
        except (ValueError, KeyError) as e:
            continue

    if total_extranjeros > 0:
        porcentaje = (universitarios_extranjeros / total_extranjeros) * 100
        print(f"\n[Resultado {ano_elegido}-T{trimestre_elegido}]")
        print(f"El {porcentaje:.2f}% de personas no nacidas en Argentina ({ano_elegido}-T{trimestre_elegido}) han cursado el nivel Universitario o Superior.")
        print(f"• Total: {total_extranjeros:,} extranjeros")
        print(f"• Universitarios: {universitarios_extranjeros:,}")
    else:
        print(f"\nNo hay datos de extranjeros para {ano_elegido}-T{trimestre_elegido}")


##---------------------------------------------------------Inciso 3---------------------------------------------------------------------------

def analizar_desocupacion(datos_csv):
    """Calcula tasas de desocupación por año y trimestre sobre la PEA (ESTADO 1 y 2)."""
    try:
        lector = leer_archivos(datos_csv)
        desocupados = {}
        poblacion_pea = {}
        
        for fila in lector:
            try:
                ano = int(fila['ANO4'])
                trimestre = int(fila['TRIMESTRE'])
                estado = fila.get('ESTADO')
                periodo = (ano, trimestre)

                # Considerar solo población económicamente activa (ESTADO 1 u 2)
                if estado in ['1', '2']:
                    pondera = int(fila['PONDERA'])
                    poblacion_pea[periodo] = poblacion_pea.get(periodo, 0) + pondera

                    # Si además está desocupado, sumar al contador de desocupados
                    if fila['CONDICION_LABORAL'].strip().lower() == 'desocupado':
                        desocupados[periodo] = desocupados.get(periodo, 0) + pondera

            except (ValueError, KeyError):
                print(f"Error procesando fila: {fila}")
                continue
        
        resultados = {}
        for periodo in poblacion_pea:
            if periodo in desocupados and poblacion_pea[periodo] > 0:
                tasa = (desocupados[periodo] / poblacion_pea[periodo]) * 100
                resultados[f"{periodo[0]}-T{periodo[1]}"] = round(tasa, 2)
            else:
                print(f"Advertencia: Datos insuficientes para {periodo[0]}-T{periodo[1]}")
        
        # Encontrar período con menor tasa
        periodo_min, tasa_min = min(resultados.items(), key=lambda x: x[1])
        
        return {
            'resultados': {
                'minimo': {
                    'periodo': periodo_min,
                    'tasa_desocupacion': tasa_min
                },
                'todos_periodos': resultados
            }
        }

    except (FileNotFoundError, KeyError) as e:
        print(f"Error al procesar el archivo: {e}")

        
def mostrar_resultados_desocupacion(resultados):
    """Muestra los resultados de desocupación en formato tabular."""

    if resultados.get('error'):
        print(f"\nError: {resultados['mensaje']}")
        return
    
    try:
        periodo_minimo = resultados['resultados']['minimo']
        todos_periodos = resultados['resultados']['todos_periodos']
        
        print(f"\nPeríodo con menor desocupación: {periodo_minimo['periodo']}")
        print(f"Tasa: {periodo_minimo['tasa_desocupacion']:.2f}%")
        
        print("\nTasas de desocupación por período:")
        for periodo, tasa in todos_periodos.items():
            print(f"{periodo}: {tasa:.2f}%")

    except KeyError as e:
        print(f"\nError mostrando resultados: {e}")


  

##---------------------------------------------------------Inciso 4 ---------------------------------------------------------------------------

def obtener_ultimo_periodo (datos_csv):
    """Obtiene el año y trimestre más reciente del archivo"""

    max_ano = 0
    max_trimestre = 0
    lector = leer_archivos(datos_csv)
    for fila in lector:
            ano = int(fila['ANO4'])
            trimestre = int(fila['TRIMESTRE'])
            if ano > max_ano or (ano == max_ano and trimestre > max_trimestre):
                max_ano = ano
                max_trimestre = trimestre
    return max_ano, max_trimestre

def hogares_cumplen_profesionales(datos_csv, ultimo_ano, ultimo_trimestre):
    """Devuelve una lista de códigos de hogares con 2 o más personas con estudios universitarios."""
      
    universitarios_por_hogar = {} 
    lector = leer_archivos(datos_csv)
    for fila in lector:
            try:
                # Filtrar por el período más reciente
                if int(fila['ANO4']) == ultimo_ano and int(fila['TRIMESTRE']) == ultimo_trimestre:
                    # Verificar estudios universitarios
                    if (fila['UNIVERSITARIO']) == '1':
                        codusu = fila['CODUSU']
                        # Contar universitarios por hogar
                        if codusu not in universitarios_por_hogar:
                            universitarios_por_hogar[codusu] = 0
                        universitarios_por_hogar[codusu] += 1
            except (ValueError, KeyError) as e:
                print(f"Error procesando fila: {e}")
                continue

    # Filtrar hogares con 2+ universitarios
    hogares_con_2plus = [codusu for codusu, count in universitarios_por_hogar.items() if count >= 2]
    return(hogares_con_2plus) 

#Consulta a base hogares
def ranking_5_aglomerados(hogares_csv, hogares_con_2plus, ultimo_ano, ultimo_trimestre):
    """Devuelve el ranking de los 5 aglomerados con mayor % ponderado de hogares con 2+ universitarios"""
    total_ponderado_por_aglo = {}
    ponderado_filtrado_por_aglo = {}

    lector = leer_archivos(hogares_csv)
    for fila in lector:
            try:
                if int(fila['ANO4']) == ultimo_ano and int(fila['TRIMESTRE']) == ultimo_trimestre:
                    codusu = fila['CODUSU']
                    aglomerado = fila['AGLOMERADO']
                    pondera = int(fila['PONDERA'])

                    # Sumar ponderadores totales por aglomerado
                    total_ponderado_por_aglo[aglomerado] = total_ponderado_por_aglo.get(aglomerado, 0) + pondera

                    # Sumar ponderadores de hogares con 2+ universitarios
                    if codusu in hogares_con_2plus:
                        ponderado_filtrado_por_aglo[aglomerado] = ponderado_filtrado_por_aglo.get(aglomerado, 0) + pondera
            except (ValueError, KeyError) as e:
                print(f"Error procesando fila: {e}")
                continue


    porcentaje_por_aglo = {}
    for aglo in ponderado_filtrado_por_aglo:
        total = total_ponderado_por_aglo.get(aglo, 0)
        if total > 0:
            porcentaje = ponderado_filtrado_por_aglo[aglo] / total * 100
            porcentaje_por_aglo[aglo] = porcentaje
    
    # Obtener top 5
    top_5 = sorted(porcentaje_por_aglo.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print("Top 5 aglomerados con mayor % de hogares con 2+ universitarios (ponderado):")
    for aglo, porcentaje in top_5:
        print(f" {obtener_nombre_aglomerado(aglo)}: {porcentaje:.2f}%")  # Reemplaza con obtener_nombre_aglomerado si está disponible            

 ##---------------------------------------------------------Inciso 5 ---------------------------------------------------------------------------
def porcentaje_propietarios_por_aglomerado(hogares_csv):
    """Calcula el % ponderado de viviendas ocupadas por propietarios en cada aglomerado"""

    total_ponderado_por_aglo = {}
    propietarios_ponderado_por_aglo = {}
    lector =leer_archivos(hogares_csv)
    for fila in lector:
            try: 
                aglomerado = fila['AGLOMERADO']
                ii7 = fila['II7']  # Condición de tenencia
                pondera = int(fila['PONDERA'])

                # Inicializar acumuladores
                if aglomerado not in total_ponderado_por_aglo:
                    total_ponderado_por_aglo[aglomerado] = 0
                    propietarios_ponderado_por_aglo[aglomerado] = 0

                total_ponderado_por_aglo[aglomerado] += pondera

                if ii7 in ['1', '2']:
                    propietarios_ponderado_por_aglo[aglomerado] += pondera
            except (ValueError, KeyError) as e:
                continue

    # Calcular porcentaje por aglomerado
    porcentaje_por_aglo = {}
    for aglo in total_ponderado_por_aglo:
        total = total_ponderado_por_aglo[aglo]
        propietarios = propietarios_ponderado_por_aglo.get(aglo, 0)
        if total > 0:
            porcentaje = propietarios / total * 100
            porcentaje_por_aglo[aglo] = porcentaje

    print("Porcentaje de viviendas ocupadas por propietarios por aglomerado:")
    for aglo, porcentaje in sorted(porcentaje_por_aglo.items(), key=lambda x: x[0]):
        print(f"{obtener_nombre_aglomerado(aglo)}: {porcentaje:.2f}%")


##---------------------------------------------------------Inciso 6 ---------------------------------------------------------------------------
def aglomerado_con_mas_hogares_sin_banio(hogares_csv):
    """
    Informa el aglomerado con mayor cantidad ponderada de viviendas con más de dos ocupantes y sin baño.
    """
    conteo_ponderado_por_aglo = {}

    lector = leer_archivos(hogares_csv)
    for fila in lector:
            try:
                aglomerado = fila['AGLOMERADO']
                ocupantes = int(fila['IX_TOT'])
                tiene_banio = int(fila['IV8'])
                pondera = int(fila['PONDERA'])
            except (ValueError, KeyError):
                continue  # Salteamos registros con errores

            if ocupantes >= 3 and tiene_banio == 2:  # Más de dos ocupantes y sin baño
                if aglomerado not in conteo_ponderado_por_aglo:
                    conteo_ponderado_por_aglo[aglomerado] = 0
                conteo_ponderado_por_aglo[aglomerado] += pondera

    if not conteo_ponderado_por_aglo:
        print("No se encontraron hogares que cumplan ambas condiciones.")
        return

    # Encontrar el aglomerado con la mayor cantidad
    aglo_max = max(conteo_ponderado_por_aglo.items(), key=lambda x: x[1])
    print(f"Aglomerado con mayor cantidad de viviendas con más de 2 ocupantes y sin baño:")
    print(f"{obtener_nombre_aglomerado(aglo_max[0])}: {aglo_max[1]:,.0f} hogares (ponderado)")

##---------------------------------------------------------Inciso 7 ---------------------------------------------------------------------------
def universitarios_por_aglomerado(datos_csv):
    """Devuelve un diccionario con el porcentaje de universitarios por aglomerado."""
    total_por_aglo = {}
    universitarios_por_aglo = {}
    
    lector = leer_archivos(datos_csv)
    for fila in lector:
            try:
                aglomerado = fila['AGLOMERADO']
                nivel_educativo = fila['NIVEL_ED_str']
                pondera = int(fila['PONDERA'])

                # Contamos el total de personas por aglomerado
                if aglomerado not in total_por_aglo:
                    total_por_aglo[aglomerado] = 0
                total_por_aglo[aglomerado] += pondera

                # Contamos solo universitarios
                if nivel_educativo == 'Superior o universitario':
                    if aglomerado not in universitarios_por_aglo:
                        universitarios_por_aglo[aglomerado] = 0
                    universitarios_por_aglo[aglomerado] += pondera
            except (ValueError, KeyError) as e:
                continue

    # Calculamos porcentajes
    porcentajes = {}
    for aglo in total_por_aglo:
        total_personas = total_por_aglo[aglo]
        univ = universitarios_por_aglo.get(aglo, 0)
        porcentaje = (univ / total_personas) * 100 if total_personas > 0 else 0
        porcentajes[aglo] = round(porcentaje, 2)  # Redondeamos a 2 decimales
    # Imprimir resultados
    print("\nPorcentaje de personas con nivel universitario o superior por aglomerado:")
    for aglo, porcentaje in porcentajes.items():
        nombre_aglo = obtener_nombre_aglomerado(aglo)
        print(f"{nombre_aglo}: {porcentaje}%")

##---------------------------------------------------------Inciso 8 ---------------------------------------------------------------------------

def inquilinos_por_region(hogares_csv):
    """Calcula el % ponderado de inquilinos por región y devuelve ordenado descendente."""
    regiones = {
        '01': 'Gran Buenos Aires',
        '40': 'Noroeste',
        '41': 'Noreste',
        '42': 'Cuyo',
        '43': 'Pampeana',
        '44': 'Patagonia'
    }

    total_ponderado_por_region = {region: 0 for region in regiones}
    inquilinos_ponderado_por_region = {region: 0 for region in regiones}

    lector = leer_archivos(hogares_csv)
    for fila in lector:
            try:
                region = fila['REGION']
                ii7 = fila['II7']  # Condición de tenencia
                pondera = float(fila['PONDERA'])  # Usamos float para mayor precisión

                # Sumar ponderadores totales por región
                if region in total_ponderado_por_region:
                    total_ponderado_por_region[region] += pondera

                    # Sumar ponderadores de inquilinos
                    if ii7 == '3':
                        inquilinos_ponderado_por_region[region] += pondera
            except (ValueError, KeyError) as e:
                continue

    # Calcular porcentaje por región
    porcentaje_por_region = {}
    for codigo, nombre in regiones.items():
        total = total_ponderado_por_region[codigo]
        inquilinos = inquilinos_ponderado_por_region[codigo]
        if total > 0:
            porcentaje = (inquilinos / total) * 100
            porcentaje_por_region[nombre] = porcentaje

    # Ordenar descendente por porcentaje
    resultados_ordenados = sorted(porcentaje_por_region.items(), key=lambda x: x[1],reverse=True)

    # Imprimir resultados
    print("\nPORCENTAJE DE INQUILINOS POR REGIÓN (Orden descendente)")
    print("=" * 45)
    for region, porcentaje in resultados_ordenados:
        print(f"{region:<20} {porcentaje:>6.2f}%")
    

##---------------------------------------------------------Inciso 9 ---------------------------------------------------------------------------

def mayores_edad_nivel_estudios (datos_csv, aglomerado_elegido):
    """""Calcula el total ponderado de personas mayores de 18 años por nivel educativo en un aglomerado, elegido por el usuario."""
    
    datos_aglomerado = {}
    lector = leer_archivos(datos_csv)

    # Filtramos y procesamos solo las filas relevantes

    filas_filtradas = filter(
            lambda fila: (
                fila['AGLOMERADO'] == aglomerado_elegido and 
                int(fila['CH06']) >= 18
            ),
            lector
        )

    for fila in filas_filtradas:
        anio=int(fila['ANO4'])
        trimestre=int(fila['TRIMESTRE'])
        nivel=(fila['NIVEL_ED_str'])
        pondera=int(fila['PONDERA'])
            

        clave = (anio, trimestre)
            
        if clave not in datos_aglomerado:
            datos_aglomerado[clave] = {
                    'Primario incompleto': 0,
                    'Primario completo': 0,
                    'Secundario incompleto': 0,
                    'Secundario completo': 0,
                    'Superior o universitario': 0
                }
        if nivel in datos_aglomerado[clave]:
            datos_aglomerado[clave][nivel] += pondera
                    
    print("\nNombre de Aglomerado:", obtener_nombre_aglomerado (aglomerado_elegido))
    print("-" * 105)
    encabezados = [
        'Año', 'Trimestre', 'Primario incompleto', 'Primario completo',
        'Secundario incompleto', 'Secundario completo', 'Superior o universitario'
    ]
    print("{:<6} | {:<9} | {:<18} | {:<16} | {:<18} | {:<16} | {:<20}".format(*encabezados))
    print("-" * 120)
   
    for (anio, trimestre), valores in sorted(datos_aglomerado.items()):
        print(
            f"{anio:<6} | {trimestre:<9} | "
            f"{valores['Primario incompleto']:<20} | "
            f"{valores['Primario completo']:<18} | "
            f"{valores['Secundario incompleto']:<20} | "
            f"{valores['Secundario completo']:<18} | "
            f"{valores['Superior o universitario']:<22}"
        )



##---------------------------------------------------------Inciso 10 ---------------------------------------------------------------------------

def mayores_secundario_incompleto (datos_csv, aglomerado_uno, aglomerado_dos):
    """Calcula el porcentaje de personas mayores de 18 años con secundario incompleto para dos aglomerados elegidos por el usuario."""

    datos = {}
    nombre_aglom_uno = obtener_nombre_aglomerado(aglomerado_uno)
    nombre_aglom_dos = obtener_nombre_aglomerado(aglomerado_dos)

    lector = leer_archivos(datos_csv)

    filas_filtradas = filter(
            lambda fila: (
                fila['AGLOMERADO'] in (aglomerado_uno, aglomerado_dos) and 
                int(fila['CH06']) > 18
            ),
            lector
        )
    for fila in filas_filtradas:
        aglomerado = fila['AGLOMERADO']                 
        anio=int(fila['ANO4'])
        trimestre=int(fila['TRIMESTRE'])
        nivel=(fila['NIVEL_ED_str'])
        pondera=int(fila['PONDERA'])
                
        clave=(anio, trimestre, aglomerado)
        if clave not in datos:
            datos[clave]= {
                'total':0,
                'Secundario incompleto':0
            }
        datos[clave]['total'] += pondera
        if nivel == 'Secundario incompleto':
            datos[clave]['Secundario incompleto'] += pondera

       
    proporcion= {}
    for (anio, trimestre, aglomerado), valores in datos.items():
        clave = (anio, trimestre)
        if clave not in proporcion:
            proporcion[clave] = {
                nombre_aglom_uno: 0.0,
                nombre_aglom_dos: 0.0
            }
        total = valores['total']
        secundario_incompleto = valores['Secundario incompleto']
        porcentaje = (secundario_incompleto / total * 100) if total > 0 else 0.0
        
        if aglomerado == aglomerado_uno:
            proporcion[clave][nombre_aglom_uno] = porcentaje
        elif aglomerado == aglomerado_dos:
            proporcion[clave][nombre_aglom_dos] = porcentaje

    print(f"\nComparación de porcentaje de Secundario incompleto (mayores de 18 años)")
    print("-" * 105)
    print(f"{'Año':<6} | {'Trimestre':<8} | {nombre_aglom_uno:<40} | {nombre_aglom_dos:<40}")
    print("-" * 105)

    for (anio, trimestre), valores in sorted(proporcion.items()):
        print(f"{anio:<6} | {trimestre:<8} | {valores[nombre_aglom_uno]:<40.2f} | {valores[nombre_aglom_dos]:<40.2f}")
        
##---------------------------------------------------------Inciso 11 ---------------------------------------------------------------------------

def aglomerados_por_techo_precario(hogares_csv):
    """Pide año al usuario, busca último trimestre de ese año y muestra aglomerados con mayor y menor % de techos precarios"""
    
    anio_usuario = input("Ingrese el año (por ejemplo, 2023): ")
    try:
        anio_usuario = int(anio_usuario)
    except ValueError:
        print("Año inválido.")
        return

    # Buscar el último trimestre disponible para ese año
    ultimo_trimestre = 0
    with open(hogares_csv, newline='', encoding='utf-8') as archivo_csv:
        reader = csv.DictReader(archivo_csv, delimiter=';')
        for row in reader:
            try:
                ano = int(row['ANO4'])
                trimestre = int(row['TRIMESTRE'])
            except ValueError:
                continue
            if ano == anio_usuario and trimestre > ultimo_trimestre:
                ultimo_trimestre = trimestre

    if ultimo_trimestre == 0:
        print(f"No se encontraron datos para el año {anio_usuario}.")
        return

    # Contadores ponderados
    total_ponderado = {}
    precario_ponderado = {}

    with open(hogares_csv, newline='', encoding='utf-8') as archivo_csv:
        reader = csv.DictReader(archivo_csv, delimiter=';')
        for row in reader:
            try:
                ano = int(row['ANO4'])
                trimestre = int(row['TRIMESTRE'])
                aglomerado = str(int(row['AGLOMERADO']))  # normalizar código
                material = row['MATERIAL_TECHUMBRE'].strip()
                pondera = int(row['PONDERA'])
            except (ValueError, KeyError):
                continue

            if ano == anio_usuario and trimestre == ultimo_trimestre:
                if aglomerado not in total_ponderado:
                    total_ponderado[aglomerado] = 0
                    precario_ponderado[aglomerado] = 0
                total_ponderado[aglomerado] += pondera
                if material == "Material precario":
                    precario_ponderado[aglomerado] += pondera

    # Calcular porcentajes
    porcentajes = {}
    for aglo in total_ponderado:
        total = total_ponderado[aglo]
        precarios = precario_ponderado.get(aglo, 0)
        if total > 0:
            porcentajes[aglo] = precarios / total * 100

    # Filtrar solo aglomerados con porcentaje > 0
    porcentajes_con_precarios = {k: v for k, v in porcentajes.items() if v > 0}
    
    if not porcentajes_con_precarios:
        print(f"No se encontraron viviendas con techo precario en el año {anio_usuario}, trimestre {ultimo_trimestre}.")
        return

    # Buscar aglomerado con mayor y menor % de techo precario
    aglo_max = max(porcentajes_con_precarios.items(), key=lambda x: x[1])
    aglo_min = min(porcentajes_con_precarios.items(), key=lambda x: x[1])

    print(f"Año: {anio_usuario} - Trimestre: {ultimo_trimestre}")
    print(f"Aglomerado con mayor % de techo precario: {obtener_nombre_aglomerado(aglo_max[0])} ({aglo_max[1]:.2f}%)")
    print(f"Aglomerado con menor % de techo precario: {obtener_nombre_aglomerado(aglo_min[0])} ({aglo_min[1]:.2f}%)")

##---------------------------------------------------------Inciso 12 ---------------------------------------------------------------------------

def jubilados_hogar (datos_csv, hogares_csv, anio_max, trim_max):
    """Calcula el porcentaje de jubilados en hogares con condición de habitabilidad insuficiente."""

    hogar = {}

    lector = leer_archivos(datos_csv)

    # Filtramos en una sola línea con lambda y filter y tenemos en cuenta la condición de jubilados, el año y el trimestre
    jubilados_filtrados = filter(
        lambda fila: int(fila['ANO4']) == anio_max 
                    and int(fila['TRIMESTRE']) == trim_max 
                and fila.get('CAT_INAC') == '1',
            lector
        )   

    for fila in jubilados_filtrados:
        codigo_hogar = fila['CODUSU']
        if codigo_hogar not in hogar:
            hogar[codigo_hogar] = {
                'jubilados ponderados':0,
                'aglomerado': 0,
                'condición': 0
            }
        hogar[codigo_hogar]['jubilados ponderados'] += int(fila['PONDERA'])
        hogar[codigo_hogar]['aglomerado'] = fila['AGLOMERADO']

              
    lector_hogares = leer_archivos(hogares_csv)

    hogares_filtrados = filter(
        lambda fila: int(fila['ANO4']) == anio_max 
                    and int(fila['TRIMESTRE']) == trim_max 
                    and fila.get('CONDICION_DE_HABITABILIDAD') == 'Insuficiente', 
            lector_hogares
        )
    
    for fila in hogares_filtrados:
            codigo_hogar = fila['CODUSU']
            if codigo_hogar in hogar:
                hogar[codigo_hogar]['condición'] = 'Insuficiente'
            
    aglomerados = {}
    for datos in hogar.values():
        aglo = datos['aglomerado']
        if aglo not in aglomerados:
            aglomerados[aglo] = {'jubilados': 0, 'total': 0}
        aglomerados[aglo]['total'] += datos['jubilados ponderados']
        if datos['condición'] == 'Insuficiente':
            aglomerados[aglo]['jubilados'] += datos['jubilados ponderados']

    print(f"{'Aglomerado':<45} | {'% Jubilados':>10}")
    print("-" * 60)

    for aglo, valores in sorted(aglomerados.items()):
        porcentaje = (valores['jubilados'] / valores['total'] * 100) if valores['total'] > 0 else 0.0
        print(f"{obtener_nombre_aglomerado(aglo):<45} | {porcentaje:>10.2f}%")
        
##---------------------------------------------------------Inciso 13 ---------------------------------------------------------------------------

def personas_universitarias_en_viviendas_insuficientes(individuos_csv, hogares_csv):
    """Calcula la cantidad de personas con estudios universitarios que viven en viviendas con habitabilidad insuficiente."""

    try:
        anio = int(input("Ingrese el año a consultar (por ejemplo, 2023): "))
    except ValueError:
        print("Año inválido.")
        return
    max_trimestre = 0
    lector = leer_archivos(individuos_csv)
    for fila in lector:
        try:
            if int(fila['ANO4']) == anio:
                trimestre = int(fila['TRIMESTRE'])
                if trimestre > max_trimestre:
                    max_trimestre = trimestre
        except (KeyError, ValueError):
            continue
    if max_trimestre == 0:
        print(f"No hay datos para el año {anio}")
        return
    
    hogares_insuf = set()
    lector_hogares = leer_archivos(hogares_csv)
    hogares_insuf = set(
            map(lambda fila: fila['CODUSU'],
                filter(lambda fila: (
                    fila['ANO4'] == str(anio) and
                    fila['TRIMESTRE'] == str(max_trimestre) and
                    fila.get('CONDICION_DE_HABITABILIDAD', '').strip().lower() == 'insuficiente'
                ), lector_hogares)
            )
        )
    
    lector_individuos = leer_archivos(individuos_csv)
    universitarios = filter(lambda fila: (
            fila['ANO4'] == str(anio) and
            fila['TRIMESTRE'] == str(max_trimestre) and
            fila.get('NIVEL_ED_str', '').strip() == 'Superior o universitario' and
            fila['CODUSU'] in hogares_insuf
        ), lector_individuos)
    
    total_ponderado = sum(map(lambda fila: int(fila['PONDERA']), universitarios))

    print(f"Cantidad de personas con estudios universitarios o superiores que viven en viviendas con habitabilidad insuficiente en {anio} T{max_trimestre}: {total_ponderado}")