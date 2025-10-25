"""
Configuración global del proyecto de procesamiento HTML.
"""

import os
from pathlib import Path

# Rutas base del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / 'src'
DATA_DIR = PROJECT_ROOT / 'data'
LOGS_DIR = PROJECT_ROOT / 'logs'

# Rutas específicas
ACTIVITIES_DIR = SRC_DIR / 'activities'
UTILS_DIR = SRC_DIR / 'utils'
CONFIG_DIR = SRC_DIR / 'config'
TESTS_DIR = SRC_DIR / 'tests'

# Rutas de datos
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'
HTML_FILES_DIR = INPUT_DIR / 'Files'

# Configuración de logging
LOG_FILE = LOGS_DIR / 'processing.log'

# Configuración de procesamiento
PROCESSING_CONFIG = {
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'batch_size': 1000,
    'encoding': 'utf-8',
    'threads': 4,
    'timeout': 300,
    'retry_attempts': 3
}

# Asegurar que las carpetas necesarias existen
for directory in [LOGS_DIR, INPUT_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

# Extensiones de archivo permitidas
ALLOWED_EXTENSIONS = {'.html', '.htm'}

# Patrones regex para tokenización
TOKEN_PATTERNS = {
    'tag': r'<[^>]+>',
    'word': r'\b[a-zA-Z]+\b',
    'number': r'\b\d+\b',
    'special_char': r'[^\w\s]',
    'attribute': r'\s(\w+)="([^"]*)"'
}