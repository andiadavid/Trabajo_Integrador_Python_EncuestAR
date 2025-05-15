import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils.constantes import (
    RUTA_CARGA_DE_DATOS,
    RUTA_BUSQUEDA,
    RUTA_VISUALIZACION
)

# --- Título y descripción ---
st.title("EncuestAR")
st.write("""
Esta aplicación permite explorar información proveniente de la Encuesta Permanente de Hogares (EPH).
La EPH es una encuesta nacional que releva características sociodemográficas, laborales y habitacionales de los hogares argentinos.
""")

# --- Menú de navegación ---
pagina_seleccionada = st.selectbox(
    "Menú de navegación",
    ["Inicio", "Carga de datos 📁", "Búsqueda por temas 🔍", "Visualización 📊"]
)

# --- Redirección ---
if pagina_seleccionada == "Carga de datos 📁":
    st.switch_page(RUTA_CARGA_DE_DATOS)
elif pagina_seleccionada == "Búsqueda por temas 🔍":
    st.switch_page(RUTA_BUSQUEDA)
elif pagina_seleccionada == "Visualización 📊":
    st.switch_page(RUTA_VISUALIZACION)