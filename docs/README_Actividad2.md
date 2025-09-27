# Actividad 2 - Eliminación de Etiquetas HTML

Este programa elimina las etiquetas HTML de archivos HTML y genera archivos de texto limpio, midiendo los tiempos de procesamiento como se requiere en la actividad académica.

## 🎯 **Características principales**

✅ **Función `remove_html_tags(filename)`** - Recibe el nombre del archivo como parámetro  
✅ **Eliminación completa de etiquetas HTML** usando expresiones regulares  
✅ **Archivos de salida limpios** en directorio `Clean_Files/`  
✅ **Medición de tiempos individuales** de cada archivo procesado  
✅ **Medición de tiempo total del programa** completo  
✅ **Reporte académico** en formato `a2_matricula.txt`  
✅ **Manejo robusto de codificaciones** (UTF-8, Latin-1, CP1252, ISO-8859-1)  
✅ **Limpieza de espacios en blanco** y líneas vacías excesivas  

## 📊 **Resultados del último procesamiento**

- **Archivos HTML procesados:** 506 archivos  
- **Tasa de éxito:** 100.0% (506/506 archivos exitosos)  
- **Tiempo total (suma individual):** 0.753037 segundos  
- **Tiempo total del programa:** 0.809621 segundos  
- **Tiempo promedio por archivo:** 0.001488 segundos  
- **Archivo más lento:** 0.020866 segundos  
- **Archivo más rápido:** 0.000516 segundos  

## 🚀 **Uso rápido**

### Opción 1: Script automático (Windows)
```cmd
ejecutar_actividad2.bat
```

### Opción 2: Comando directo
```cmd
python actividad2_html_cleaner.py
```

## ⚙️ **Configuración**

Edita `config.py` para cambiar tu matrícula:
```python
MATRICULA = "A00000000"  # ← Cambia por tu matrícula real
```

## 📁 **Estructura de archivos**

```
├── actividad2_html_cleaner.py  # 🔧 Programa principal
├── config.py                   # ⚙️ Configuración
├── ejecutar_actividad2.bat     # 🚀 Script de ejecución
├── Files/                      # 📂 Archivos HTML originales
│   ├── 002.html
│   ├── 003.html
│   └── ... (506 archivos)
├── Clean_Files/                # 📂 Archivos sin etiquetas HTML
│   ├── 002_clean.txt
│   ├── 003_clean.txt
│   └── ... (506 archivos)
└── a2_matricula.txt            # 📄 Reporte de resultados
```

## 🔍 **Ejemplo de procesamiento**

### Archivo original (`002.html`):
```html
<HTML>
<HEAD>
    <TITLE>CDT Testimony - Med Privacy (6/14/96)</TITLE>
</HEAD>
<BODY BGCOLOR="#ffffff">
<CENTER><A HREF="/index.html">
<H2>Statement of<BR>
Janlori Goldman<BR>
Deputy Director<BR>
```

### Archivo limpio (`002_clean.txt`):
```
CDT Testimony - Med Privacy (6/14/96)

Statement of

Janlori Goldman
Deputy Director
```

## 📈 **Salida del programa**

### En consola:
```
Encontrados 506 archivos HTML
Iniciando eliminación de etiquetas HTML...
Los archivos limpios se guardarán en el directorio 'Clean_Files'
------------------------------------------------------------
✓ Procesado: 002.html             - Tiempo: 0.002514 segundos
✓ Procesado: 003.html             - Tiempo: 0.000912 segundos
...
============================================================
RESUMEN DE RESULTADOS:
============================================================
Archivos HTML encontrados: 506
Archivos procesados exitosamente: 506
Tasa de éxito: 100.0%
Tiempo total (suma individual): 0.753037 segundos
Tiempo total del programa: 0.809621 segundos
Directorio de salida: Clean_Files/
Reporte guardado en: a2_A00000000.txt
============================================================
```

### Archivo de reporte (`a2_matricula.txt`):
```
======================================================================
REPORTE DE ELIMINACIÓN DE ETIQUETAS HTML
======================================================================
Matrícula: A00000000
Fecha: 2025-08-25 19:05:31
Total de archivos procesados: 506
Archivos procesados exitosamente: 506
Directorio de salida: Clean_Files/
======================================================================

TIEMPOS DE PROCESAMIENTO INDIVIDUAL:
--------------------------------------------------
Archivo                   Tiempo (seg)    Estado    
--------------------------------------------------
002.html                  0.002514        Exitoso   
003.html                  0.000912        Exitoso   
...

TOTALES:                 
Suma individual:          0.753037       
Tiempo programa:          0.809621       
--------------------------------------------------

ESTADÍSTICAS (archivos exitosos):
Tiempo promedio: 0.001488 segundos
Tiempo máximo: 0.020866 segundos
Tiempo mínimo: 0.000516 segundos
Archivos procesados: 506 de 506
Tasa de éxito: 100.0%

======================================================================
DESCRIPCIÓN DEL PROCESO:
======================================================================
1. Lectura de archivos HTML con manejo de múltiples codificaciones
2. Eliminación de etiquetas HTML usando expresiones regulares
3. Limpieza de espacios en blanco y líneas vacías excesivas
4. Guardado de archivos limpios en directorio 'Clean_Files/'
5. Medición precisa de tiempos de procesamiento
======================================================================
```

## 🔧 **Funciones principales**

### `remove_html_tags(filename)`
- **Parámetro:** Nombre del archivo HTML
- **Retorno:** Tiempo de procesamiento en segundos
- **Función:** Elimina etiquetas HTML y genera archivo limpio

### **Expresiones regulares utilizadas:**
- **Eliminación de etiquetas:** `r'<[^>]+>'` 
- **Limpieza de espacios:** `r'[ \t]+'` → un espacio
- **Limpieza de líneas vacías:** `r'\n\s*\n'` → doble salto

## 💡 **Tecnologías utilizadas**

- **Python 3** - Lenguaje de programación  
- **`re` (regex)** - Expresiones regulares para eliminar etiquetas  
- **`time.perf_counter()`** - Medición precisa de tiempos  
- **`glob`** - Búsqueda masiva de archivos HTML  
- **Manejo de codificaciones múltiples** - UTF-8, Latin-1, CP1252, ISO-8859-1  

## ✅ **Cumplimiento académico**

- ✅ Función `remove_html_tags()` recibe nombre de archivo como parámetro  
- ✅ Elimina etiquetas HTML usando expresiones regulares  
- ✅ Genera archivos nuevos sin etiquetas HTML  
- ✅ Mide tiempo individual de procesamiento de cada archivo  
- ✅ Mide tiempo total del programa completo  
- ✅ Genera archivo log `a2_matricula.txt` con todos los datos  
- ✅ Procesa todos los archivos HTML del directorio  
- ✅ La diferencia entre suma individual y tiempo total muestra el overhead  

## 🎓 **Notas académicas**

Este programa demuestra el uso efectivo de:
- **Expresiones regulares** para procesamiento de texto
- **Manejo de archivos** con diferentes codificaciones
- **Medición precisa de rendimiento** con `time.perf_counter()`
- **Procesamiento masivo** de archivos de manera eficiente
- **Generación de reportes** académicos detallados
