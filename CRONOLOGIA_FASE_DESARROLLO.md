# Cronología y Línea del Tiempo — Fase de Desarrollo

Este documento reconstruye el orden real de las actividades realizadas en esta fase de desarrollo y las mapea a eventos Scrum, dejando una línea del tiempo clara para documentación académica.

> Nota: La fase se ejecutó sin documentación Scrum previa; aquí se emula la trazabilidad con base en entregables, archivos y fechas aproximadas.

## Resumen de Entregables
- Actividad 1: `buscador_html.py` + `a1_<matrícula>.txt` + `README.md`
- Actividad 2: `actividad2_html_cleaner.py` + `a2_<matrícula>.txt` + `README_Actividad2.md`
- Actividad 3: `actividad3_word_extractor.py` + `a3_<matrícula>.txt` + `README_Actividad3.md`
- Configuración y automatización: `config.py`, scripts `.bat`, `menu_principal.bat`
- Backlog y documentación: `BACKLOG.md`, `DOCUMENTACION_COMPLETA.md`

## Línea del Tiempo (emulada)

| Fecha (aprox.) | Actividad | Artefactos | Evento Scrum emulado |
|---|---|---|---|
| 2025-08-24 | Preparación del entorno y datos | Estructura `Files/` con .html | Sprint 0 (Setup) |
| 2025-08-25 | Implementación HU-01 (Medición de tiempos) | `buscador_html.py`, `a1_*.txt` | Sprint 1 — Desarrollo |
| 2025-08-26 | Documentación HU-01 | `README.md` | Sprint 1 — Documentación |
| 2025-08-27 | Implementación HU-02 (Limpieza HTML) | `actividad2_html_cleaner.py`, `a2_*.txt` | Sprint 2 — Desarrollo |
| 2025-08-28 | Automatización y limpieza | `ejecutar_actividad2.bat` | Sprint 2 — Mejora |
| 2025-08-29 | Implementación HU-03 (Palabras) | `actividad3_word_extractor.py`, `a3_*.txt` | Sprint 3 — Desarrollo |
| 2025-08-30 | Scripts y validación | `ejecutar_actividad3.bat`, `menu_principal.bat` | Sprint 3 — QA |
| 2025-08-31 | Documentación consolidada | `DOCUMENTACION_COMPLETA.md` | Sprint 3 — Sprint Review |
| 2025-09-17 | Backlog y equipo Scrum | `BACKLOG.md` (PO/SM/Devs) | Sprint 4 — Planificación |

> Las fechas pueden variar ligeramente; se basan en el estado de archivos y el repositorio actual.

## Mapeo a Historias de Usuario

- HU-01 (Completada): Medición de tiempos — Actividad 1
  - Entradas: `Files/*.html`
  - Salidas: `a1_<matrícula>.txt`
- HU-02 (Completada): Limpieza de etiquetas HTML — Actividad 2
  - Entradas: `Files/*.html`
  - Salidas: `Clean_Files/*_clean.txt`, `a2_<matrícula>.txt`
- HU-03 (Completada): Extracción y ordenamiento de palabras — Actividad 3
  - Entradas: `Clean_Files/*_clean.txt`
  - Salidas: `Words_Files/*_words.txt`, `a3_<matrícula>.txt`
- HU-04 (Pendiente): Consolidado global de palabras
  - Entradas: `Words_Files/*_words.txt`
  - Salidas: `consolidado_palabras.txt`, `a4_<matrícula>.txt`

## Ceremonias Scrum (emuladas)

- Sprint Planning: Definición de HU y capacidad por sprint (HU-01, HU-02, HU-03, próxima HU-04).
- Daily Scrum: Seguimiento informal de bloqueos (codificaciones, tiempos, lotes grandes de archivos).
- Sprint Review: Presentación de reportes `a1/a2/a3` y scripts .bat al “cliente”.
- Retrospective: Decisiones de mejora (centralizar config, robustecer codificaciones, automatizar menús y reportes).

## Decisiones Técnicas
- Codificaciones múltiples (utf-8, latin‑1, cp1252, iso‑8859‑1) para robustez.
- `time.perf_counter()` para mediciones de alta resolución.
- Regex para limpieza y extracción de palabras con guiones/apóstrofes.
- Estructura de carpetas de salida (`Clean_Files/`, `Words_Files/`).
- Scripts .bat para ejecución reproducible en Windows.

## Próximos Pasos (Sprint siguiente)
1) Implementar HU-04 (consolidado) y agregar al menú.
2) Añadir validaciones y pruebas sobre archivos vacíos/duplicados.
3) Documentar resultados y actualizar `BACKLOG.md` con cierre de HU-04.
