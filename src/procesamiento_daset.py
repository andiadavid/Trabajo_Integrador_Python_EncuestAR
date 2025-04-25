from pathlib import Path
import csv


def escribir_encabezado(file, salida, encabezado_escrito: bool) -> bool:
    """Escribe el encabezado en el archivo de salida si aún no se ha escrito."""
    encabezado = file.readline()
    if not encabezado_escrito:
        salida.write(encabezado)
        return True
    return encabezado_escrito

def generar_archivo_individuos(files_path: Path, archivo_salida: Path):
    encabezado_escrito = False
    with open (archivo_salida, "w") as salida:
        for trimestre in files_path.iterdir():
            #print(trimestre)
            for archivo in trimestre.glob("usu_individual*"):
                with open(archivo) as file:
                    encabezado_escrito = escribir_encabezado(file, salida, encabezado_escrito)
                    for linea in file:
                        salida.write(linea)
                
                print("fin archivo")    


#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------


def leer_individuos_como_dicc(archivo_csv):
    """Lee el archivo CSV y lo devuelve como una lista de diccionarios."""
    with open(archivo_csv, newline='', encoding='utf-8') as entrada:
        #en estaparte es importante el delimitador, ya que el archivo original tiene ; como delimitador
        lector = csv.DictReader(entrada, delimiter=';')
        return [row for row in lector]  # Devuelve todas las filas como diccionarios


#-------------------------
"""
#modifico esta funcion para que sea mas generica
def reorganizar_encabezados(lista_diccionarios):
    # Reorganizar las columnas para que CH04_str quede junto a CH04
    encabezado = list(lista_diccionarios[0].keys())  # Obtener las claves actuales
    if "CH04" in encabezado and "CH04_str" in encabezado:
        # Mover CH04_str al lado de CH04
        encabezado.remove("CH04_str")
        indice_edad = encabezado.index("CH04")
        encabezado.insert(indice_edad + 1, "CH04_str")
    return encabezado
"""
def reorganizar_encabezados(lista_diccionarios,columna_base:str, columna_nueva:str):
    # Reorganizar las columnas para que columna_nueva quede junto a columna_base
    encabezado = list(lista_diccionarios[0].keys())  # Obtener las claves actuales
    if columna_base in encabezado and columna_nueva in encabezado:
        # Mover columna_nueva al lado de columna_base
        encabezado.remove(columna_nueva)
        indice_base = encabezado.index(columna_base)
        encabezado.insert(indice_base + 1, columna_nueva)
    return encabezado


#-------------------------

def escribir_lista_como_csv(lista_diccionarios, encabezado, archivo_csv):
    """Escribe una lista de diccionarios en un archivo CSV."""
    if not lista_diccionarios:
        raise ValueError("La lista de diccionarios está vacía, no se puede escribir el archivo.")
    with open(archivo_csv, "w", newline='', encoding='utf-8') as salida:
        escritor = csv.DictWriter(salida, fieldnames=encabezado, delimiter=';')
        escritor.writeheader()
        escritor.writerows(lista_diccionarios)


#-----------------------------------------------------------------------

def convertir_ch04_a_str_genero(lista_diccionarios):
    """Convierte la columna CH04 en 'masculino' o 'femenino' en cada diccionario."""
    for row in lista_diccionarios:
        row["CH04_str"] = "otro"  # Valor por defecto si CH04 no está presente
        if "CH04" in row:
            row["CH04_str"] = "masculino" if row["CH04"] == "1" else "femenino" if row["CH04"] == "2" else "otro"
    return lista_diccionarios


#-------------------------

def convertir_NIVEL_ED_a_str(lista_diccionarios):
    """Convierte la columna NIVEL_ED a str en cada diccionario."""
    for row in lista_diccionarios:
        # Verificar si NIVEL_ED existe en la row
        if "NIVEL_ED" in row:
            try:
                nivel = int(row["NIVEL_ED"])  # Convertir a entero
                if nivel == 1:
                    row["NIVEL_ED_str"] = "Primario incompleto"
                elif nivel == 2:
                    row["NIVEL_ED_str"] = "Primario completo"
                elif nivel == 3:
                    row["NIVEL_ED_str"] = "Secundario incompleto"
                elif nivel == 4:
                    row["NIVEL_ED_str"] = "Secundario completo"
                elif nivel in [5, 6]:
                    row["NIVEL_ED_str"] = "Superior o universitario"
                elif nivel in [7, 9]:
                    row["NIVEL_ED_str"] = "Sin información"
                else:
                    row["NIVEL_ED_str"] = "Nivel no especificado"
            except ValueError:
                row["NIVEL_ED_str"] = "Valor no válido"

    return lista_diccionarios

#-------------------------

def transformar_condicion_laboral(lista_diccionarios):
    """
    Agrega la columna CONDICION_LABORAL a cada diccionario en la lista con base
    en las reglas de transformación para ESTADO y CAT_OCUP.
    """
    for row in lista_diccionarios:
        # Verificar que las claves ESTADO y CAT_OCUP existan
        if "ESTADO" in row and "CAT_OCUP" in row:
            try:
                estado = int(row["ESTADO"])  # Convertir ESTADO a entero
                cat_ocup = int(row["CAT_OCUP"])  # Convertir CAT_OCUP a entero

                # Aplicar las reglas de transformación
                if estado == 1 and cat_ocup in [1, 2]:
                    row["CONDICION_LABORAL"] = "Ocupado autónomo"
                elif estado == 1 and cat_ocup in [3, 4, 9]:
                    row["CONDICION_LABORAL"] = "Ocupado dependiente"
                elif estado == 2:
                    row["CONDICION_LABORAL"] = "Desocupado"
                elif estado == 3:
                    row["CONDICION_LABORAL"] = "Inactivo"
                elif estado == 4:
                    row["CONDICION_LABORAL"] = "Fuera de categoría/sin información"
                else:
                    row["CONDICION_LABORAL"] = "Información no válida"
            except ValueError:
                row["CONDICION_LABORAL"] = "Valor no válido"  # Manejar valores no numéricos
        else:
            row["CONDICION_LABORAL"] = "Información incompleta"  # Faltan claves
    return lista_diccionarios

#-------------------------

from datetime import datetime

def generar_mayores_con_titulo(lista_diccionarios):
    hoy = datetime.now()  # Fecha actual

    for row in lista_diccionarios:
        if "CH05" in row and "NIVEL_ED" in row:
            try:
                # Dividir CH05 en día, mes, año
                dia, mes, anio = map(int, row["CH05"].split("/"))  # Ejemplo: "15/05/1985"
                fecha_nacimiento = datetime(anio, mes, dia)

                # Calcular la edad
                edad = hoy.year - fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
                )

                # Evaluar el nivel educativo
                nivel_ed = int(row["NIVEL_ED"])

                if edad < 18:
                    row["UNIVERSITARIO"] = 2  # No aplica (menor de edad)
                elif nivel_ed == 6:  # Superior universitario completo
                    row["UNIVERSITARIO"] = 1  # Sí
                elif nivel_ed in [1, 2, 3, 4, 5, 7, 9]:  # Otros niveles
                    row["UNIVERSITARIO"] = 0  # No
                else:
                    row["UNIVERSITARIO"] = -1  # Nivel educativo no válido
            except (ValueError, KeyError):
                row["UNIVERSITARIO"] = -1  # Error en el formato o valores inválidos
        else:
            row["UNIVERSITARIO"] = -1  # Información incompleta
    return lista_diccionarios