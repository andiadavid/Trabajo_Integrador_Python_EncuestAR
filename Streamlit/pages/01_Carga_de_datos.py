import streamlit as st
import sys
from pathlib import Path
import csv

# Agregar el path a la carpeta src
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils.constantes import RUTA_PAGINA_INICIO, DATA_OUT_PATH

st.title("Carga de datos")

carpeta = Path(DATA_OUT_PATH)

def obtener_rango_temporal(carpeta: Path):
    archivos = sorted(carpeta.glob("*.csv"))
    periodos = set()

    for archivo in archivos:
        with open(archivo, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                try:
                    anio = int(row["ANO4"])
                    trimestre = int(row["TRIMESTRE"])
                    periodos.add((anio, trimestre))
                except:
                    continue

    if periodos:
        desde_anio, desde_trim = min(periodos)
        hasta_anio, hasta_trim = max(periodos)
        desde = f"{desde_trim:02d}/{desde_anio}"
        hasta = f"{hasta_trim:02d}/{hasta_anio}"    
        return desde, hasta, sorted(periodos)
    else:
        return None, None, []

# Botón para actualizar dataset (simulado)
if st.button("Actualizar dataset"):
    desde, hasta, periodos = obtener_rango_temporal(carpeta)
    if desde and hasta:
        st.success(f"Dataset actualizado. El sistema contiene información desde el {desde} hasta el {hasta}.")
        st.write("Períodos disponibles:")
        for anio, trim in periodos:
            st.write(f"- {trim:02d}/{anio}")
    else:
        st.warning("No se encontraron archivos válidos al actualizar.")
else:
    # Mostrar datos existentes aunque no se actualice
    desde, hasta, periodos = obtener_rango_temporal(carpeta)
    if desde and hasta:
        st.info(f"El sistema contiene información desde el {desde} hasta el {hasta}.")
        st.write("Períodos disponibles:")
        for anio, trim in periodos:
            st.write(f"- {trim:02d}/{anio}")
    else:
        st.warning("No se encontraron archivos válidos.")

# Botón para volver al inicio
if st.button("Volver al inicio", key="volver_inicio"):
    st.switch_page(RUTA_PAGINA_INICIO)