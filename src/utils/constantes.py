from pathlib import Path
#parent va para atras tres veces, >a utils, >a src >y a la carpeta principal
PROYECT_PATH = Path(__file__).parent.parent.parent
FILES_PATH = PROYECT_PATH / "files"
DATA_OUT_PATH = FILES_PATH / "data_out"
