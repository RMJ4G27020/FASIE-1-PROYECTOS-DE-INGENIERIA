# Backlog Inicial del Proyecto

Este documento define el backlog inicial para el proyecto de procesamiento de archivos HTML y extracción de palabras. Se trabajará con un equipo Scrum durante todo el proyecto.

## Visión del Producto
Construir una herramienta académica que procese masivamente archivos HTML para: (1) medir tiempos de apertura, (2) limpiar etiquetas HTML, (3) extraer y ordenar palabras, y (4) generar un archivo consolidado con todas las palabras en minúsculas, ordenadas alfabéticamente.

## Equipo Scrum (propuesto)
- Cliente: Profesor del curso
- Product Owner (PO): JOSE GPE RICO MORENO
- Scrum Master (SM): Melanie Esmeralda Garza Guajardo
- Equipo de Desarrollo: Hilary Vanessa Camacho Alvarez, Eduardo Luis Macouzet Calles

Nota: El equipo se mantendrá constante durante el proyecto.

---

## Historias de Usuario

Documento relacionado: ver "Cronología y Línea del Tiempo" en `CRONOLOGIA_FASE_DESARROLLO.md`.

### HU-01: Medir tiempos de apertura de archivos HTML (Actividad 1)
Como estudiante, quiero medir el tiempo de apertura de cada archivo HTML y del programa completo, para generar un reporte académico con estadísticas.

**Criterios de Aceptación**
- Se procesa el directorio `Files/` y se listan los `.html` en orden alfabético.
- Se genera `a1_<matrícula>.txt` con: tiempos individuales, total del programa, suma individual, promedio, máximo, mínimo, fecha y matrícula.
- Se muestran resultados en consola.

**Tareas**
- Implementar `open_file(filename)` con manejo de codificaciones y cronometraje.
- Recorrer archivos, acumular métricas y generar reporte.
- Validar con 10 archivos de muestra y con el set completo.

**Estado**: Completada ✅

---

### HU-02: Limpiar etiquetas HTML (Actividad 2)
Como estudiante, quiero eliminar etiquetas HTML de todos los archivos y generar textos limpios, para preparar los datos para análisis posterior.

**Criterios de Aceptación**
- Se genera `Clean_Files/` con un `*_clean.txt` por cada `.html`.
- Se genera `a2_<matrícula>.txt` con tiempos individuales y totales, estadísticas y tasa de éxito.
- Se manejan múltiples codificaciones y errores de lectura/escritura.

**Tareas**
- Implementar `remove_html_tags(filename)` con regex y limpieza de espacios.
- Crear carpeta de salida y escribir archivos limpios en UTF-8.
- Reportar métricas y estados (Exitoso/Error).

**Estado**: Completada ✅

---

### HU-03: Extraer y ordenar palabras (Actividad 3)
Como estudiante, quiero extraer palabras únicas de los archivos limpios y ordenarlas alfabéticamente, para disponer de listas por documento.

**Criterios de Aceptación**
- Se genera `Words_Files/` con `*_words.txt` (una palabra por línea, minúsculas, ordenadas).
- Se genera `a3_<matrícula>.txt` con tiempos, conteos por archivo y estadísticas.
- Se manejan palabras con guiones y apóstrofes según patrón definido.

**Tareas**
- Implementar `extract_and_sort_words(filename)` con regex y normalización a minúsculas.
- Contabilizar palabras por archivo y reportar.
- Manejo de codificaciones de respaldo.

**Estado**: Completada ✅

---

### HU-04: Consolidar palabras en un único archivo (Nueva)
Como estudiante, quiero crear un archivo consolidado que contenga todas las palabras (en minúsculas) de todos los archivos, ordenadas alfabéticamente, para facilitar la búsqueda y análisis global.

**Criterios de Aceptación**
- Entrada: Archivos `*_words.txt` desde `Words_Files/` (generados en HU-03).
- Salida: `consolidado_palabras.txt` en la raíz del proyecto o en `Words_Files/`.
- Contenido: Cada palabra en minúsculas, una por línea, sin duplicados, orden alfabéticamente.
- Reporte: `a4_<matrícula>.txt` con total de palabras únicas, tiempo individual por archivo, tiempo total y estadísticas.
- Manejo de errores: Directorios/archivos faltantes, codificaciones, archivos vacíos.

**Tareas**
- Recorrer `Words_Files/`, leer y agregar palabras a un `set` global.
- Ordenar y escribir `consolidado_palabras.txt` en UTF-8.
- Medir tiempos y generar `a4_<matrícula>.txt`.
- Agregar opción al `menu_principal.bat`.

**Estado**: Pendiente ⏳

---

## Definición de Hecho (DoD)
- Código con anotaciones de tipo y sin errores de linters (Pylance).
- Manejo robusto de errores y codificaciones.
- Reportes generados con formato y métricas definidas.
- Scripts .bat actualizados para ejecución.
- Documentación en README actualizada por actividad.
- Pruebas manuales con set de muestra y con set completo.

## Definición de Listo (DoR)
- Historia con criterios de aceptación claros y tareas definidas.
- Entradas, salidas y rutas de archivos especificadas.
- Dependencias con otras historias explicitadas.

---

## Plan de Sprint (Siguiente Sprint)
- Objetivo: Implementar HU-04 (consolidado de palabras) y actualizar menú/documentación.
- Capacidad estimada: 1-2 devs, 1 sprint.
- Tareas priorizadas: Implementación, pruebas, documentación, automatización.

## Revisión de Sprint (Pasado)
- HU-01, HU-02, HU-03 completadas y revisadas con el "cliente".
- Retroalimentación: Mantener manejo de codificaciones, claridad en reportes y tiempos.
- Bases para el siguiente sprint: Consolidado global (HU-04) y validaciones adicionales.
