import streamlit as st
import sys

sys.path.append("..")
from src.utils.constantes import RUTA_PAGINA_INICIO
#-----------------------------------
st.title("Visualización")


#codigo relacionado a la carga de datos


#---------------------------
#boton para volver al inicio
if st.button("Volver al inicio", key="volver_inicio"):
    st.switch_page(RUTA_PAGINA_INICIO)