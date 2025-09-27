# Actividad 3 - Extracción y Ordenamiento de Palabras

## Descripción
Este script procesa los archivos HTML limpios (generados en la Actividad 2) para extraer todas las palabras únicas, ordenarlas alfabéticamente y guardarlas en archivos individuales.

## Funcionalidades

### Extracción de Palabras
- **Entrada**: Archivos limpios (sin etiquetas HTML) del directorio `Clean_Files/`
- **Salida**: Archivos de palabras en el directorio `Words_Files/`
- **Formato de salida**: Una palabra por línea, ordenadas alfabéticamente

### Manejo de Caracteres Especiales
El script maneja inteligentemente diferentes tipos de palabras:
- **Palabras simples**: `word`, `example`, `test`
- **Palabras con apostrofe**: `don't`, `can't`, `it's`
- **Palabras con guión**: `state-of-the-art`, `automata-based`, `programming`
- **Todas se convierten a minúsculas** para mantener consistencia

### Ordenamiento
- Utiliza la función `sorted()` integrada de Python
- Ordenamiento alfabético estricto
- Eliminación automática de palabras duplicadas
- Preserva palabras con caracteres especiales válidos

## Archivos Generados

### 1. Archivos de Palabras (`Words_Files/`)
```
002_words.txt
003_words.txt
004_words.txt
...
```

### 2. Reporte de Actividad (`a3_matricula.txt`)
Contiene:
- **Información general**: matrícula, fecha, archivos procesados
- **Tiempos individuales**: por cada archivo procesado
- **Estadísticas**: tiempo total, promedio, máximo, mínimo
- **Conteo de palabras**: total de palabras únicas extraídas
- **Tasa de éxito**: archivos procesados exitosamente
- **Descripción del proceso**: algoritmos utilizados

## Ejecución

### Opción 1: Script Individual
```bash
python actividad3_word_extractor.py
```

### Opción 2: Script Batch
```bash
ejecutar_actividad3.bat
```

### Opción 3: Menú Principal
```bash
menu_principal_actualizado.bat
# Seleccionar opción 3
```

## Requisitos Previos

1. **Actividad 2 completada**: Debe existir el directorio `Clean_Files/` con archivos limpios
2. **Python 3.x**: Con módulos estándar (`os`, `time`, `glob`, `re`)
3. **Archivo config.py**: Con configuración de matrícula y precisión

## Proceso Detallado

### 1. Detección de Archivos
- Busca archivos `*_clean.txt` en `Clean_Files/`
- Los ordena alfabéticamente para procesamiento consistente

### 2. Extracción de Palabras
```python
# Expresión regular utilizada
word_pattern = re.compile(r'\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b')
```
- Encuentra palabras completas
- Incluye palabras con guiones internos
- Incluye palabras con apostrofes internos
- Excluye números y símbolos

### 3. Procesamiento
- Conversión a minúsculas
- Eliminación de duplicados usando `set()`
- Ordenamiento alfabético con `sorted()`

### 4. Guardado
- Cada archivo genera un archivo `*_words.txt`
- Una palabra por línea
- Codificación UTF-8

### 5. Medición de Tiempos
- **Tiempo individual**: Por cada archivo procesado
- **Tiempo total**: Del programa completo
- **Precisión configurable**: Según `config.py`

## Ejemplos de Uso

### Entrada (archivo limpio):
```
World Wide Web Access Statistics for COSMIR

Last update Fri 11 Oct 1996 00 00 00 GMT 0500

Hi World Wide Web Access Statistics for COSMIR

Last update Fri 11 Oct 1996 00 00 00
```

### Salida (archivo de palabras):
```
access
cosmir
for
fri
gmt
hi
last
oct
statistics
update
web
wide
world
www
```

## Configuración

### config.py
```python
MATRICULA = "tu_matricula"
PRECISION_DECIMALS = 3
FALLBACK_ENCODINGS = ['latin-1', 'cp1252', 'iso-8859-1']
```

## Manejo de Errores

- **Archivos faltantes**: Verifica existencia de `Clean_Files/`
- **Errores de codificación**: Múltiples encodings de respaldo
- **Errores de escritura**: Crea directorios automáticamente
- **Archivos vacíos**: Manejo graceful con conteo de palabras = 0

## Estadísticas del Reporte

El reporte incluye métricas detalladas:
- Tiempo promedio por archivo
- Archivo más rápido/lento de procesar
- Promedio de palabras por archivo
- Archivo con más/menos palabras únicas
- Tasa de éxito del procesamiento

## Notas Técnicas

1. **Expresión Regular**: Diseñada para capturar palabras del inglés académico
2. **Memoria Eficiente**: Usa `set()` para eliminación de duplicados
3. **Codificación Robusta**: Múltiples intentos de decodificación
4. **Ordenamiento Estable**: Resultados consistentes entre ejecuciones
