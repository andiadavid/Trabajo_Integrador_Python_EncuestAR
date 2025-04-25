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


#-------------------------

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
        row["NIVEL_ED_str"] = "otro"
    return lista_diccionarios
