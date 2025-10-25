# Proyecto de Procesamiento HTML - Estructura Reorganizada

## Estructura del Proyecto

```
proyecto/
├── src/                     # Código fuente
│   ├── activities/          # Módulos principales de actividades
│   │   ├── actividad4_consolidate_words.py
│   │   ├── actividad5_tokenize.py
│   │   └── actividad6_dictionary.py
│   ├── config/             # Configuración del proyecto
│   │   ├── config.py
│   │   └── project_config.py
│   └── utils/              # Utilidades y scripts
├── data/                   # Datos del proyecto
│   ├── input/             # Archivos de entrada
│   │   └── Files/         # Archivos HTML
│   └── output/            # Resultados procesados
├── docs/                  # Documentación
├── logs/                  # Archivos de registro
├── launcher.py            # Script principal de ejecución
└── run_project.bat       # Script batch para Windows
```

## Cómo Ejecutar

### Opción 1: Launcher Interactivo (Recomendado)
```bash
python launcher.py
```

### Opción 2: Script Batch (Windows)
```cmd
run_project.bat
```

### Opción 3: Ejecución Directa
```bash
# Desde el directorio raíz del proyecto
python src/activities/actividad4_consolidate_words.py
python src/activities/actividad5_tokenize.py
python src/activities/actividad6_dictionary.py
```

## Actividades

### Actividad 4: Consolidación de Palabras
- **Archivo**: `src/activities/actividad4_consolidate_words.py`
- **Función**: Consolida palabras de múltiples archivos HTML
- **Salida**: Archivo consolidado con conteo de frecuencias

### Actividad 5: Tokenización
- **Archivo**: `src/activities/actividad5_tokenize.py`
- **Función**: Tokeniza texto HTML y realiza análisis
- **Salida**: Tokens clasificados y estadísticas

### Actividad 6: Análisis de Diccionario
- **Archivo**: `src/activities/actividad6_dictionary.py`
- **Función**: Crea diccionario y análisis de frecuencias
- **Salida**: Diccionario completo con estadísticas

## Configuración

La configuración del proyecto se encuentra en:
- `src/config/config.py`: Configuración básica
- `src/config/project_config.py`: Configuración avanzada y rutas

## Resolución de Problemas

### Error: "ModuleNotFoundError: No module named 'config'"
Este error se resuelve usando el launcher.py que configura correctamente los paths:
```bash
python launcher.py
```

### Estructura de Directorios
Si falta algún directorio, ejecute:
```bash
# Windows PowerShell
New-Item -ItemType Directory -Path "data\input", "data\output", "logs" -Force
```

## Logs

Los archivos de registro se guardan en el directorio `logs/` y contienen:
- Información de procesamiento
- Errores y advertencias
- Métricas de rendimiento

## Desarrollo

Para desarrollo y pruebas:
1. Asegúrese de que todos los directorios existen
2. Use el launcher.py para ejecución
3. Revise los logs para debugging
4. Mantenga la estructura de directorios organizada

## Mejoras Implementadas

1. **Separación de Responsabilidades**: Código organizado por funcionalidad
2. **Gestión de Configuración**: Centralizada en `/config`
3. **Manejo de Datos**: Separación clara entre entrada y salida
4. **Logging**: Sistema unificado de registros
5. **Launcher**: Script central para ejecución fácil