
import csv
from datetime import datetime

#-----------------------------------------------------------------------

def convertir_ch04_a_str_genero(lista_diccionarios):
    """Convierte la columna CH04 en 'masculino' o 'femenino' en cada diccionario."""
    for fila in lista_diccionarios:
        fila["CH04_str"] = "otro"  # Valor por defecto si CH04 no está presente
        if "CH04" in fila:
            fila["CH04_str"] = "masculino" if fila["CH04"] == "1" else "femenino" if fila["CH04"] == "2" else "otro"
    return lista_diccionarios


#-------------------------

def convertir_NIVEL_ED_a_str(lista_diccionarios):
    """Convierte la columna NIVEL_ED a str en cada diccionario."""
    for fila in lista_diccionarios:
        # Verificar si NIVEL_ED existe en la fila
        if "NIVEL_ED" in fila:
            try:
                nivel = int(fila["NIVEL_ED"])  # Convertir a entero
                if nivel == 1:
                    fila["NIVEL_ED_str"] = "Primario incompleto"
                elif nivel == 2:
                    fila["NIVEL_ED_str"] = "Primario completo"
                elif nivel == 3:
                    fila["NIVEL_ED_str"] = "Secundario incompleto"
                elif nivel == 4:
                    fila["NIVEL_ED_str"] = "Secundario completo"
                elif nivel in [5, 6]:
                    fila["NIVEL_ED_str"] = "Superior o universitario"
                elif nivel in [7, 9]:
                    fila["NIVEL_ED_str"] = "Sin información"
                else:
                    fila["NIVEL_ED_str"] = "Nivel no especificado"
            except ValueError:
                fila["NIVEL_ED_str"] = "Valor no válido"

    return lista_diccionarios

#-------------------------

def transformar_condicion_laboral(lista_diccionarios):
    """
    Agrega la columna CONDICION_LABORAL a cada diccionario en la lista con base
    en las reglas de transformación para ESTADO y CAT_OCUP.
    """
    for fila in lista_diccionarios:
        # Verificar que las claves ESTADO y CAT_OCUP existan
        if "ESTADO" in fila and "CAT_OCUP" in fila:
            try:
                estado = int(fila["ESTADO"])  # Convertir ESTADO a entero
                cat_ocup = int(fila["CAT_OCUP"])  # Convertir CAT_OCUP a entero

                # Aplicar las reglas de transformación
                if estado == 1 and cat_ocup in [1, 2]:
                    fila["CONDICION_LABORAL"] = "Ocupado autónomo"
                elif estado == 1 and cat_ocup in [3, 4, 9]:
                    fila["CONDICION_LABORAL"] = "Ocupado dependiente"
                elif estado == 2:
                    fila["CONDICION_LABORAL"] = "Desocupado"
                elif estado == 3:
                    fila["CONDICION_LABORAL"] = "Inactivo"
                elif estado == 4:
                    fila["CONDICION_LABORAL"] = "Fuera de categoría/sin información"
                else:
                    fila["CONDICION_LABORAL"] = "Información no válida"
            except ValueError:
                fila["CONDICION_LABORAL"] = "Valor no válido"  # Manejar valores no numéricos
        else:
            fila["CONDICION_LABORAL"] = "Información incompleta"  # Faltan claves
    return lista_diccionarios

#-------------------------

def generar_mayores_con_titulo(lista_diccionarios):
    """Crea la columna 'UNIVERSITARIO' en cada diccionario de la lista."""
    hoy = datetime.now()  # Fecha actual

    for fila in lista_diccionarios:
        if "CH05" in fila and "NIVEL_ED" in fila:
            try:
                # Dividir CH05 en día, mes, año
                #map(int, ...) aplica la función int() a cada elemento de la lista.
                dia, mes, anio = map(int, fila["CH05"].split("/"))  # Ejemplo: "15/05/1985"
                fecha_nacimiento = datetime(anio, mes, dia)

                # Calcular la edad
                #Calcula la diferencia entre el año actual (hoy.year) y el año de nacimiento (fecha_nacimiento.year).
                #Pero esto por sí solo no siempre es correcto, porque si la persona aún no ha cumplido años este año, habría que restar 1.
                
                edad = hoy.year - fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
                )

                # Evaluar el nivel educativo
                nivel_ed = int(fila["NIVEL_ED"])

                if edad < 18:
                    fila["UNIVERSITARIO"] = 2  # No aplica (menor de edad)
                elif nivel_ed == 6:  # Superior universitario completo
                    fila["UNIVERSITARIO"] = 1  # Sí
                elif nivel_ed in [1, 2, 3, 4, 5, 7, 9]:  # Otros niveles
                    fila["UNIVERSITARIO"] = 0  # No
                else:
                    fila["UNIVERSITARIO"] = -1  # Nivel educativo no válido
            except (ValueError, KeyError):
                fila["UNIVERSITARIO"] = -1  # Error en el formato o valores inválidos
        else:
            fila["UNIVERSITARIO"] = -1  # Información incompleta
    return lista_diccionarios

#--------------------------funciones para dataset hogares------------------
def obtener_entero(valor):
    """Convierte un valor a entero, eliminando espacios y verificando si es un número."""
    valor = valor.strip()
    if valor.isdigit():
        return int(valor)
    return None 

#-------------------------
def procesar_tipo_hogar(fila, ix_tot_idx):
    """determina el tipo de hogar según la cantidad de personas"""
    
    personas = obtener_entero(fila[ix_tot_idx])
    if personas is None or personas == 0:
        return None, personas
    
    if personas == 1:
        return "Unipersonal"
    elif 2 <= personas <= 4:
        return "Nuclear"
    elif personas >= 5:
        return "Extendido"
    
    return None, personas
#-------------------------
def procesar_material_techumbre (fila, iv4_idx):
    """determina el material de techumbre"""
        
    techo = obtener_entero(fila[iv4_idx])
    
    if techo is None or techo == 0:
        return None
            
    if techo in (1, 2, 3, 4):
        return "Material durable"
    elif techo in (5, 6, 7):
        return "Material precario"
    elif techo == 9:
        return "No aplica"
    
    return None
#-------------------------
def procesar_densidad_hogar(fila, iv2_idx, ix_tot_idx):
    """determina la densidad del hogar"""
    
    cant_habitaciones = obtener_entero(fila[iv2_idx])
    personas = obtener_entero(fila[ix_tot_idx])
    
    if cant_habitaciones is None or cant_habitaciones == 0 or personas is None or personas == 0:
        return None
    
    densidad = cant_habitaciones / personas
    
    if densidad < 1:
        return "Bajo"
    elif 1 <= densidad <= 2:
        return "Medio"
    elif densidad > 2:
        return "Alto"
    
    return None
#-------------------------
def procesar_condicion_habitabilidad (filas, iv6_idx, iv7_idx, iv8_idx, iv9_idx, iv10_idx, iv11_idx):
    """determina la condicion de habitabilidad del hogar"""
    
    
    tiene_agua = obtener_entero(filas[iv6_idx])
    origen_agua = obtener_entero(filas[iv7_idx])
    tiene_baño = obtener_entero(filas[iv8_idx])
    ubicacion_baño = obtener_entero(filas[iv9_idx])
    tipo_baño = obtener_entero(filas[iv10_idx])
    tipo_desague = obtener_entero(filas[iv11_idx])
    
    
    if (tiene_agua is None) or (origen_agua is None) or (tiene_baño is None) or (ubicacion_baño is None) or (tipo_baño is None) or (tipo_desague is None):
        return None

    
    if (tiene_agua == 1) and (origen_agua == 1) and (tiene_baño == 1) and (ubicacion_baño == 1) and (tipo_baño == 1) and \
        (tipo_desague == 1):
            return "Buena"
    elif (tiene_baño == 1) and (ubicacion_baño == 1) and (tipo_baño == 1) and (tipo_desague in [1,2]) and (tiene_agua == 1) and (origen_agua in [1,2]):
        return "Saludable"
    elif ((tiene_agua in [1,2]) and (tiene_baño == 1) and (tipo_desague in [1,2,3]) ) and ((origen_agua in [1,2,3,4]) or (ubicacion_baño ==3 )): 
        return "Regular"
    elif (tiene_agua == 3) or (tiene_baño == 2) or (tipo_desague ==4):
        return "Insuficiente"
#--------------------------
