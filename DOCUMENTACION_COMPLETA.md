# 📁 PROYECTOS DE INGENIERÍA - PROCESAMIENTO HTML

> **Proyecto académico completo** para el procesamiento eficiente de archivos HTML con medición de tiempos y generación de reportes.

## 🎯 **Descripción General**

Este repositorio contiene **tres actividades académicas** relacionadas con el procesamiento de archivos HTML:

1. **🕐 Actividad 1**: Medición de tiempos de apertura de archivos HTML
2. **🧹 Actividad 2**: Eliminación de etiquetas HTML y limpieza de contenido  
3. **📝 Actividad 3**: Extracción y ordenamiento alfabético de palabras

Todas las actividades incluyen medición precisa de tiempos, manejo robusto de errores, y generación automática de reportes académicos.

---

## 🚀 **Inicio Rápido**

### Opción 1: Menú Interactivo (Recomendado)
```cmd
menu_principal.bat
```

### Opción 2: Ejecución Individual
```cmd
# Actividad 1 - Medición de tiempos
ejecutar.bat

# Actividad 2 - Limpieza HTML  
ejecutar_actividad2.bat

# Actividad 3 - Extracción de palabras
ejecutar_actividad3.bat
```

### Opción 3: Comandos Python Directos
```cmd
python buscador_html.py           # Actividad 1
python actividad2_html_cleaner.py # Actividad 2  
python actividad3_word_extractor.py # Actividad 3
```

---

## 📋 **Requisitos**

- **Python 3.6+** (con módulos estándar)
- **Windows** (para scripts .bat)
- **506 archivos HTML** en directorio `Files/`
- **Configuración personalizada** en `config.py`

---

## ⚙️ **Configuración**

**Antes de ejecutar**, edita `config.py`:

```python
# Tu matrícula (OBLIGATORIO)
MATRICULA = "A00000000"  # ← Cambia por tu matrícula real

# Configuración opcional
FILES_DIRECTORY = "Files"
PRECISION_DECIMALS = 6
ENCODING = "utf-8"
```

---

## 📁 **Estructura del Proyecto**

```
📦 PROYECTOS-DE-INGENIERIA/
│
├── 🔧 **Programas Principales**
│   ├── buscador_html.py           # 🕐 Actividad 1
│   ├── actividad2_html_cleaner.py # 🧹 Actividad 2
│   ├── actividad3_word_extractor.py # 📝 Actividad 3
│   └── config.py                  # ⚙️ Configuración
│
├── 🚀 **Scripts de Automatización**
│   ├── ejecutar.bat               # Actividad 1
│   ├── ejecutar_actividad2.bat    # Actividad 2
│   ├── ejecutar_actividad3.bat    # Actividad 3
│   └── menu_principal.bat         # Menú interactivo
│
├── 📖 **Documentación**
│   ├── README.md                  # Actividad 1
│   ├── README_Actividad2.md       # Actividad 2
│   └── README_Actividad3.md       # Actividad 3
│
├── 📂 **Directorios de Datos**
│   ├── Files/                     # Archivos HTML originales
│   ├── Clean_Files/              # Archivos sin etiquetas HTML
│   └── Words_Files/              # Archivos de palabras ordenadas
│
└── 📄 **Reportes Generados**
    ├── a1_matricula.txt          # Reporte Actividad 1
    ├── a2_matricula.txt          # Reporte Actividad 2
    └── a3_matricula.txt          # Reporte Actividad 3
```

---

## 🔍 **Actividades Detalladas**

### 🕐 **Actividad 1: Medición de Tiempos**

**Objetivo**: Medir tiempos de apertura de archivos HTML

**Características**:
- ✅ Función `open_file(filename)` como se requiere
- ✅ Medición individual de cada archivo
- ✅ Medición de tiempo total del programa
- ✅ Manejo robusto de codificaciones múltiples
- ✅ Estadísticas completas (promedio, máximo, mínimo)

**Resultados típicos**:
- **506 archivos procesados** en ~0.15 segundos
- **Tiempo promedio por archivo**: 0.0002 segundos
- **Sin errores de codificación**

---

### 🧹 **Actividad 2: Eliminación de Etiquetas HTML**

**Objetivo**: Limpiar archivos HTML eliminando todas las etiquetas

**Características**:
- ✅ Función `remove_html_tags(filename)` como se requiere  
- ✅ Expresiones regulares para eliminación de etiquetas
- ✅ Limpieza de espacios en blanco excesivos
- ✅ Archivos de salida limpios en `Clean_Files/`
- ✅ Tasa de éxito del 100%

**Resultados típicos**:
- **506 archivos procesados** exitosamente
- **Tiempo total**: ~0.8 segundos
- **Archivos limpios generados**: 506 archivos `.txt`

---

### 📝 **Actividad 3: Extracción de Palabras**

**Objetivo**: Extraer y ordenar palabras de archivos limpios

**Características**:
- ✅ Función `extract_and_sort_words(filename)` como se requiere
- ✅ Expresiones regulares para extracción inteligente
- ✅ Manejo de palabras con guiones y apostrofes
- ✅ Ordenamiento alfabético con `sorted()`
- ✅ Eliminación automática de duplicados

**Tipos de palabras manejadas**:
- Palabras simples: `word`, `example`, `test`
- Con apostrofe: `don't`, `can't`, `it's`
- Con guión: `state-of-the-art`, `automata-based`

---

## 📊 **Reportes Generados**

Cada actividad genera un reporte académico completo:

### 📄 Formato de Reporte (`a1_matricula.txt`, `a2_matricula.txt`, `a3_matricula.txt`)

```
============================================================
REPORTE DE [NOMBRE DE LA ACTIVIDAD]
============================================================
Matrícula: A00000000
Fecha: 2025-08-31 15:30:45
Total de archivos procesados: 506
============================================================

TIEMPOS INDIVIDUALES:
----------------------------------------
Archivo         Tiempo (seg)   Estado
----------------------------------------
002.html        0.000289       Exitoso
003.html        0.000156       Exitoso
...

ESTADÍSTICAS:
Tiempo promedio: 0.000222 segundos
Tiempo máximo: 0.001545 segundos
Tiempo mínimo: 0.000088 segundos
============================================================
```

---

## 🛠️ **Tecnologías Utilizadas**

- **🐍 Python 3** - Lenguaje principal
- **⏱️ `time.perf_counter()`** - Medición precisa de tiempos
- **🔍 `re` (Regex)** - Procesamiento de texto avanzado
- **📁 `glob`** - Búsqueda masiva de archivos
- **🔤 `typing`** - Anotaciones de tipos para código limpio
- **🔧 Manejo de múltiples codificaciones** - UTF-8, Latin-1, CP1252, ISO-8859-1

---

## ✅ **Cumplimiento Académico**

Todas las actividades cumplen **100%** con los requisitos:

### ✅ Actividad 1
- ✅ Función `open_file()` recibe nombre de archivo
- ✅ Medición de tiempos individuales
- ✅ Medición de tiempo total del programa
- ✅ Archivo de salida `a1_matricula.txt`
- ✅ Procesamiento de todos los archivos HTML

### ✅ Actividad 2  
- ✅ Función `remove_html_tags()` recibe nombre de archivo
- ✅ Eliminación de etiquetas HTML
- ✅ Generación de archivos limpios
- ✅ Medición de tiempos individuales y total
- ✅ Archivo de salida `a2_matricula.txt`

### ✅ Actividad 3
- ✅ Función `extract_and_sort_words()` recibe nombre de archivo
- ✅ Extracción de palabras de archivos limpios
- ✅ Ordenamiento alfabético usando `sorted()`
- ✅ Medición de tiempos individuales y total
- ✅ Archivo de salida `a3_matricula.txt`

---

## 🎓 **Valor Académico**

Este proyecto demuestra competencias en:

- **📊 Algoritmos de ordenamiento** - Uso eficiente de `sorted()`
- **🔍 Expresiones regulares** - Procesamiento avanzado de texto
- **⏱️ Medición de rendimiento** - Benchmarking preciso con `perf_counter()`
- **📁 Manejo masivo de archivos** - Procesamiento eficiente de 506+ archivos
- **🔤 Manejo de codificaciones** - Robustez ante diferentes encodings
- **📝 Documentación técnica** - Reportes académicos detallados
- **🧹 Código limpio** - Uso de type hints y buenas prácticas
- **⚡ Optimización** - Diferencia entre tiempo individual vs overhead del sistema

---

## 🔧 **Funciones Clave**

### 🕐 `open_file(filename: str) -> float`
- **Propósito**: Abrir archivo HTML y medir tiempo
- **Retorna**: Tiempo en segundos
- **Maneja**: Múltiples codificaciones automáticamente

### 🧹 `remove_html_tags(filename: str) -> float`
- **Propósito**: Eliminar etiquetas HTML y generar archivo limpio
- **Retorna**: Tiempo de procesamiento
- **Genera**: Archivo `*_clean.txt` en `Clean_Files/`

### 📝 `extract_and_sort_words(filename: str) -> float`
- **Propósito**: Extraer palabras y ordenar alfabéticamente
- **Retorna**: Tiempo de procesamiento
- **Genera**: Archivo `*_words.txt` en `Words_Files/`

---

## 📈 **Métricas de Rendimiento**

| Actividad | Archivos | Tiempo Típico | Tasa Éxito | Salida |
|-----------|----------|---------------|------------|--------|
| **1** | 506 HTML | ~0.15s | 100% | Reportes de tiempo |
| **2** | 506 HTML | ~0.8s  | 100% | 506 archivos limpios |
| **3** | 506 TXT  | ~1.2s  | 100% | 506 archivos de palabras |

---

## 🎯 **Ejecución Recomendada**

1. **📝 Configura tu matrícula** en `config.py`
2. **🚀 Ejecuta el menú principal**: `menu_principal.bat`
3. **📊 Revisa los reportes** generados automáticamente
4. **✅ Verifica los directorios** de salida (`Clean_Files/`, `Words_Files/`)

---

## 📞 **Soporte**

Para cualquier duda o problema:
- **📋 Revisa la documentación** de cada actividad
- **🔍 Verifica la configuración** en `config.py`
- **📁 Asegúrate de tener** el directorio `Files/` con archivos HTML
- **🐍 Confirma la versión** de Python (3.6+)

---

**🎓 Proyecto académico completo - Ingeniería de Software**  
**📅 Agosto 2025**  
**🔗 Repositorio**: [FASIE-1-PROYECTOS-DE-INGENIERIA](https://github.com/RMJ4G27020/FASIE-1-PROYECTOS-DE-INGENIERIA)
