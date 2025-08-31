# Buscador HTML - Medición de Tiempos

Este programa en Python mide el tiempo que tarda en abrir archivos HTML de manera eficiente, como se solicita en la actividad académica.

## Características

✅ **Abre todos los archivos HTML eficientemente** usando la función `open_file(nombre_archivo)`  
✅ **Mide tiempos individuales** de apertura de cada archivo  
✅ **Mide tiempo total del programa** completo  
✅ **Genera reporte académico** en formato `a1_matricula.txt`  
✅ **Maneja diferentes codificaciones** (UTF-8, Latin-1, CP1252, ISO-8859-1)  
✅ **Estadísticas completas** (promedio, máximo, mínimo)  

## Resultados del último análisis

- **Archivos procesados:** 506 archivos HTML
- **Tiempo total (suma individual):** 0.112209 segundos
- **Tiempo total del programa:** 0.149292 segundos
- **Tiempo promedio por archivo:** 0.000222 segundos
- **Sin errores de codificación**

## Requisitos
- Python 3.6 o superior
- Archivos HTML en la carpeta `Files/`

## Uso Rápido

### Opción 1: Script automático (Windows)
```cmd
ejecutar.bat
```

### Opción 2: Comando directo
```cmd
python buscador_html.py
```

## Configuración

1. Edita el archivo `config.py` y cambia los siguientes valores:
   ```python
   MATRICULA = "A00000000"  # ← Cambia por tu matrícula real
   ```

## Archivos del proyecto

```
├── buscador_html.py     # ✅ Programa principal
├── config.py            # ⚙️ Configuración
├── ejecutar.bat         # 🚀 Script de ejecución
├── README.md            # 📖 Este archivo
├── Files/               # 📁 Directorio con archivos HTML
│   ├── 002.html
│   ├── 003.html
│   └── ... (504 más)
└── a1_matricula.txt     # 📄 Archivo de salida generado
```

## Salida del programa

### En consola:
```
Encontrados 506 archivos HTML
Iniciando medición de tiempos...
Procesado: 002.html - Tiempo: 0.000289 segundos
Procesado: 003.html - Tiempo: 0.000156 segundos
...
==================================================
RESUMEN DE RESULTADOS:
==================================================
Archivos procesados: 506
Tiempo total (suma individual): 0.112209 segundos
Tiempo total del programa: 0.149292 segundos
Reporte guardado en: a1_A00000000.txt
==================================================
```

### Archivo de reporte (`a1_matricula.txt`):
```
============================================================
REPORTE DE TIEMPOS DE APERTURA DE ARCHIVOS HTML
============================================================
Matrícula: A00000000
Fecha: 2025-08-25 18:56:35
Total de archivos procesados: 506
============================================================

TIEMPOS INDIVIDUALES:
----------------------------------------
Archivo         Tiempo (seg)   
----------------------------------------
002.html        0.000289       
003.html        0.000156       
...

TOTALES:       
Suma individual: 0.112209       
Tiempo programa: 0.149292       
----------------------------------------

ESTADÍSTICAS:
Tiempo promedio: 0.000222 segundos
Tiempo máximo: 0.001545 segundos
Tiempo mínimo: 0.000088 segundos
```

## Funciones principales

- **`open_file(filename)`**: Abre un archivo HTML y mide el tiempo de apertura
- **`main()`**: Función principal que coordina todo el proceso
- **Manejo robusto de codificaciones**: UTF-8, Latin-1, CP1252, ISO-8859-1

## Tecnologías utilizadas

- **Python 3** - Lenguaje de programación
- **`time.perf_counter()`** - Medición precisa de tiempos
- **`glob`** - Búsqueda de archivos HTML
- **Manejo de excepciones** - Para archivos corruptos o inaccesibles

## Notas académicas

- ✅ Cumple con todos los requisitos de la actividad
- ✅ Función `open_file()` recibe el nombre del archivo como parámetro  
- ✅ Genera archivo log `a1_matricula.txt`
- ✅ Mide tiempos individuales y tiempo total del programa
- ✅ La diferencia entre "suma individual" y "tiempo programa" muestra el overhead del sistema
- ✅ Procesa archivos en orden alfabético
- ✅ Maneja errores de codificación de manera elegante
