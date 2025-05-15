from pathlib import Path
#parent va para atras tres veces, >a utils, >a src >y a la carpeta principal
PROYECT_PATH = Path(__file__).parent.parent.parent
FILES_PATH = PROYECT_PATH / "files"
DATA_OUT_PATH = PROYECT_PATH / "data_out"

RUTA_PAGINAS_STREAMLIT = PROYECT_PATH / "Streamlit" / "pages" 
RUTA_PAGINA_INICIO = PROYECT_PATH / "Streamlit" / "Inicio.py"
RUTA_CARGA_DE_DATOS = RUTA_PAGINAS_STREAMLIT / "01_Carga_de_datos.py"
RUTA_BUSQUEDA = RUTA_PAGINAS_STREAMLIT / "02_Busqueda_por_tema.py"
RUTA_VISUALIZACION = RUTA_PAGINAS_STREAMLIT / "03_Visualizacion.py"