@startwbs
title Proyecto: Procesamiento masivo de HTML (Fase Desarrollo)

legend right
| Clave | Integrante                              | Rol           |
| [PO]  | JOSE GPE RICO MORENO                    | Product Owner |
| [SM]  | Melanie Esmeralda Garza Guajardo        | Scrum Master  |
| [H]   | Hilary Vanessa Camacho Alvarez          | Dev           |
| [E]   | Eduardo Luis Macouzet Calles            | Dev           |
endlegend

* Proyecto: Procesamiento masivo de HTML (Fase Desarrollo)
** Sprint 0 (Setup / Preparación)
*** Contexto/Objetivo
**** Preparar entorno, datos y configuración para ejecutar actividades 1-3 y habilitar HU-04 posterior. [SM]
*** Entradas
**** Windows + Python 3.x [SM]
**** Carpeta `Files/` con .html de entrada [E]
*** Salidas
**** Estructura de carpetas: `Files/`, `Clean_Files/`, `Words_Files/` [E]
**** Configuración: `config.py` (MATRICULA, FILES_DIRECTORY, ENCODING, PRECISION_DECIMALS) [E]
**** Scripts base `.bat` (plantillas) [H]
*** Pasos
**** Crear carpetas según convención [E]
**** Verificar Python 3.x y módulos estándar [H]
**** Definir valores en `config.py` [E]
*** Criterios de aceptación
**** Estructura de carpetas creada y accesible [SM]
**** `config.py` parametrizado y sin errores [SM]
*** Pruebas
**** Verificación de lectura/escritura en carpetas [H+E]
*** Evidencias
**** Árbol de carpetas y `config.py` en repositorio [SM]
*** No incluido
**** No se procesan aún HTML ni se generan reportes [PO]

** Sprint 1 — HU-01: Medición de tiempos (Actividad 1)
*** Contexto/Objetivo
**** Medir tiempos individuales de apertura de .html y tiempo total del programa, generar reporte académico. [H]
*** Entradas
**** `Files/*.html` [H]
**** `config.py` (codificaciones, precisión) [H]
*** Salidas
**** Script: `buscador_html.py` [H]
**** Reporte: `a1_<matrícula>.txt` [H]
**** Doc: `README.md` (Actividad 1) [SM]
*** Pasos (Qué se hizo)
**** Implementar `open_file(filename: str) -> float` con `time.perf_counter()` y codificaciones de respaldo (utf-8, latin-1, cp1252, iso-8859-1) [H]
**** Recorrer `Files/*.html`, acumular tiempos, ordenar alfabéticamente [H]
**** Generar `a1_<matrícula>.txt` con totales y estadísticas (promedio, máx, mín) [H]
**** Automatizar ejecución con `ejecutar.bat` [E]
*** Criterios de aceptación
**** Procesa todos los `.html` y muestra en consola los tiempos [PO]
**** Genera `a1_<matrícula>.txt` con métricas y fecha [PO]
**** Orden alfabético garantizado [PO]
*** Pruebas
**** Lote pequeño (≈10 archivos) y lote completo [H+E]
**** Validar contenido del reporte y diferencias entre suma individual vs tiempo total [SM]
*** Evidencias
**** `buscador_html.py`, `a1_<matrícula>.txt`, `README.md`, `ejecutar.bat` [SM]
*** No incluido
**** Paralelismo, UI, exportes extra [PO]
*** Responsables
**** Implementación/Pruebas: [H], Automatización: [E], Doc/Review: [SM], Aceptación: [PO]

** Sprint 2 — HU-02: Limpieza HTML (Actividad 2)
*** Contexto/Objetivo
**** Eliminar etiquetas HTML para dejar texto limpio y medible/analizable. [E]
*** Entradas
**** `Files/*.html` [E]
**** `config.py` [E]
*** Salidas
**** Script: `actividad2_html_cleaner.py` [E]
**** Carpeta: `Clean_Files/` con `*_clean.txt` [E]
**** Reporte: `a2_<matrícula>.txt` [E]
**** Doc: `README_Actividad2.md` [SM]
**** Automatización: `ejecutar_actividad2.bat` [H]
*** Pasos (Qué se hizo)
**** Implementar regex `<[^>]+>` para quitar etiquetas [E]
**** Normalizar espacios y líneas vacías; guardar UTF-8 [E]
**** Medir tiempos por archivo y total; reportar tasa de éxito [E]
**** Automatizar y validar outputs [H]
*** Criterios de aceptación
**** Se genera `*_clean.txt` por cada `.html` en `Clean_Files/` [PO]
**** Reporte con tiempos, totales, tasa de éxito, estadísticas [PO]
**** Manejo robusto de codificaciones/errores E/S [PO]
*** Pruebas
**** Comparar entrada/salida visualmente (muestra) [H+E]
**** Validar conteo de archivos en `Clean_Files/` [SM]
*** Evidencias
**** `actividad2_html_cleaner.py`, `Clean_Files/*_clean.txt`, `a2_<matrícula>.txt`, `README_Actividad2.md`, `ejecutar_actividad2.bat` [SM]
*** No incluido
**** NLP avanzado, idiomas múltiples, deduplicación semántica [PO]
*** Responsables
**** Implementación: [E], Automatización: [H], Doc/Review: [SM], Aceptación: [PO]

** Sprint 3 — HU-03: Palabras ordenadas (Actividad 3)
*** Contexto/Objetivo
**** Extraer palabras únicas de archivos limpios, normalizar y ordenar alfabéticamente. [H]
*** Entradas
**** `Clean_Files/*_clean.txt` [H]
*** Salidas
**** Script: `actividad3_word_extractor.py` [H]
**** Carpeta: `Words_Files/` con `*_words.txt` (una palabra por línea) [H]
**** Reporte: `a3_<matrícula>.txt` [H]
**** Automatización: `ejecutar_actividad3.bat`, `menu_principal.bat` (HU-01/02/03) [E]
**** Doc consolidada: `DOCUMENTACION_COMPLETA.md` [SM]
*** Pasos (Qué se hizo)
**** Regex palabras `\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b`, minúsculas, set y `sorted()` [H]
**** Medición de tiempos por archivo y total; conteo de palabras [H]
**** Integración en menú principal y validación [E]
*** Criterios de aceptación
**** Genera `*_words.txt` en `Words_Files/` (ordenado, sin duplicados, minúsculas) [PO]
**** Reporte con tiempos y estadísticas por archivo [PO]
*** Pruebas
**** Muestreo de contenidos; verificación de orden alfabético [H+E]
**** Conteo de líneas y unicidad [SM]
*** Evidencias
**** `actividad3_word_extractor.py`, `Words_Files/*_words.txt`, `a3_<matrícula>.txt`, `menu_principal.bat`, `DOCUMENTACION_COMPLETA.md` [SM]
*** No incluido
**** Stopwords, stemming/lemmatización, unicode extendido [PO]
*** Responsables
**** Implementación: [H], Menú/Automatización: [E], Doc/Review: [SM], Aceptación: [PO]

** Sprint 4 — Documentación Scrum y Planificación
*** Contexto/Objetivo
**** Formalizar backlog, equipo, cronología y preparar HU-04. [PO+SM]
*** Entradas
**** Entregables de HU-01/02/03 [SM]
*** Salidas
**** `BACKLOG.md` (HU-01..HU-04, DoR/DoD, plan sprint) [PO]
**** `CRONOLOGIA_FASE_DESARROLLO.md` (línea del tiempo y mapeo a Scrum) [SM]
**** Diagramas PlantUML (WBS, Gantt, Timeline) [SM]
*** Pasos
**** Completar equipo: PO, SM, Devs [PO]
**** Emular ceremonias previas y dejar bases del siguiente sprint [SM]
*** Criterios de aceptación
**** Historias HU-01..HU-03 marcadas como Completadas; HU-04 definida [PO]
**** Backlog referenciado desde cronología y viceversa [PO]
*** Pruebas
**** Revisión cruzada de doc y enlaces [SM]
*** Evidencias
**** `BACKLOG.md`, `CRONOLOGIA_FASE_DESARROLLO.md` [SM]
*** No incluido
**** Ejecución de HU-04 (se agenda al siguiente sprint) [PO]

** Sprint 5 — HU-04: Consolidado global (Pendiente)
*** Contexto/Objetivo
**** Unificar todas las palabras únicas globales en un archivo consolidado ordenado. [E]
*** Entradas
**** `Words_Files/*_words.txt` [E]
*** Salidas
**** `Words_Files/consolidado_palabras.txt` (únicas, minúsculas, ordenadas) [E]
**** Reporte: `a4_<matrícula>.txt` (tiempos, totales, estadísticas) [E]
**** `README_Actividad4.md` y menú actualizado (opción HU-04) [SM+E]
*** Pasos (Qué se hará)
**** Recorrer `Words_Files/`, consolidar con `set`, ordenar y guardar [E+H]
**** Medir tiempos por archivo y total; generar reporte [E]
**** Agregar opción a `menu_principal.bat` [E]
*** Criterios de aceptación
**** Consolidado sin duplicados, ordenado, minúsculas [PO]
**** Reporte a4 completo y reproducible [PO]
*** Pruebas
**** Verificar conteo único global y orden [H+E]
*** Evidencias
**** `consolidado_palabras.txt`, `a4_<matrícula>.txt`, `README_Actividad4.md`, menú [SM]
*** No incluido
**** Métricas semánticas/lingüísticas avanzadas [PO]
*** Responsables
**** Implementación: [E+H], Doc/Review: [SM], Aceptación: [PO]
@endwbs