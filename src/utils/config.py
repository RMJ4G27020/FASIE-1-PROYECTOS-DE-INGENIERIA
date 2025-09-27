"""
Configuración centralizada para el proyecto de análisis de archivos HTML
FASIE-1-PROYECTOS-DE-INGENIERIA
"""
import os

# Configuración del estudiante
MATRICULA = "A00000000"  # Cambia por tu matrícula

# Configuración de directorios - Rutas automáticas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

# Directorios específicos
FILES_DIRECTORY = os.path.join(INPUT_DIR, "Files")
CLEAN_FILES_DIR = os.path.join(OUTPUT_DIR, "clean_files")
WORDS_FILES_DIR = os.path.join(OUTPUT_DIR, "words_files")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

# Configuración de procesamiento
ENCODING = 'utf-8'
FALLBACK_ENCODINGS = ['latin-1', 'cp1252', 'iso-8859-1']
PRECISION_DECIMALS = 6

def ensure_directories():
    """Crea los directorios necesarios si no existen"""
    directories = [
        FILES_DIRECTORY,
        CLEAN_FILES_DIR,
        WORDS_FILES_DIR,
        REPORTS_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Llamar automáticamente al importar
ensure_directories()
