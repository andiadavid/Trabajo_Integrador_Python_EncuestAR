# Encuest.AR 📊

Proyecto de procesamiento y análisis de datos de la Encuesta Permanente de Hogares (EPH) para generar ***insights*** sobre individuos y hogares en Argentina.

---

1. **Preparación del entorno**: instalar dependencias 

   Es recomendable instalar un entorno virtual para instalar las dependencias del proyecto. Ejecuta: 
   
   ```bash
   python - m venv venv
 
   venv/scripts/activate #En Windows

   source venv/bin/activate #En Linux

   pip install -r requirements.txt  

## **Primera Etapa: Generación del Dataset Principal**

### **Objetivo**  

Procesar los datos crudos de la EPH para construir un dataset con datos de individuos y otro con datos de hogares.

### **Pasos para ejecutar** 

**Procesamiento de datos**:

- Se debe ejecutar los ***cell*** de los jupyter "recorrer_EPH_hogares.ipynb" y "recorrer_EPH_individuos.ipynb" ubicado en la carpeta Notebook.

    notebooks/recorrer_EPH_hogares.ipynb (procesa datos de hogares).
    notebooks/recorrer_EPH_individuos.ipynb (procesa datos de individuos).

- Salidas

    Datasets procesados en formato CSV, ubicados en la carpeta "data_out".

## **Segunda Etapa:  Consultas y Visualización**

### **Objetivo**

Realizar consultas específicas a los dataset principales (hogares e individuos) y diseñar una interfaz interactiva.

### **Pasos para ejecutar** 

### **1. Consultas:**

- Ejecutar notebooks/consultas.ipynb, que utiliza las funciones definidas en src/utils/consultas.py.

    notebooks/consultas.ipynb

- Las 13 consultas incluyen distintos análisis socioeconómicos.

### **2. Interfaz de usuario:**

- Aplicación Streamlit para visualización interactiva:

    ```bash

    streamlit run Stremlit/inicio.py  # Inicia la interfaz


## **Estructura del proyecto**
.
.
├── data_out/                            # Datos procesados (ignorados en Git con .gitignore)
│   ├── salida_hogares.csv                           
│   └── salida_individuos.csv
│
├── files/                               # Datos crudos (EPH originales)
│   
│
├── notebooks/                           # Jupyter Notebooks
│   ├── 01_recorrer_EPH.ipynb            # Notebook de procesamiento
│   └── 02_consultas.ipynb               # Notebook de análisis de consultas 
│
├── src/                                 # Código fuente 
│   └── utils/                           # Funciones auxiliares
│       └── constantes.py                 
│       └── consultas.py 
│       └── procesamiento_dataset.py                               
│
├── streamlit/                           # App de Streamlit 
│   ├── pages/                           # Páginas adicionales
│   └── Inicio.py                        # Archivo principal (streamlit run Inicio.py)
│
├── .gitignore                           # Ignora data/, __pycache__, etc.
├── requirements.txt                     # Dependencias 
├── LICENSE                              # Licencia
└── README.md                            # Documentación



## **Equipo** 👥

- Andia, David

- Cabandie, Camila

- Coccaro, Rocío Celina

- Gutiérrez, María Felicitas

- Martínez Pastur, Lucrecia
