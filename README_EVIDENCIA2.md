# Evidencia 2 — LSTI4017

Este documento reúne la evidencia solicitada para la **Evidencia 2** (rúbrica LSTI4017_Rúbrica_Evidencia_2). Cada criterio de la rúbrica está mapeado a los artefactos existentes del repositorio y se indica dónde encontrar las pruebas (archivos, logs y capturas) generadas durante el proyecto.

> Autor: JOSE GPE RICO MORENO
> Fecha: 29 de Noviembre, 2025

---

**Índice**
- Introducción
- Resumen ejecutivo
- Mapeo de la rúbrica a evidencias (criterios 1–4)
- Evidencias de compromiso y metas (criterios 5–12)
- Cómo revisar las evidencias (instrucciones rápidas)
- Archivos clave y rutas

---

## Introducción

Este README agrupa la evidencia solicitada por la rúbrica de la actividad: aplicación de SCRUM, interfaz del buscador, desempeño/funcionalidad, pruebas y consultas, y una sección con indicadores de compromiso y competencias blandas.

Los artefactos provienen del directorio `actv 1/` y subcarpetas (`activity15/`, `data/output/`, `templates/`, etc.). Aquí se listan y documentan para facilitar la evaluación.

## Resumen ejecutivo

- Proyecto: Motor de búsqueda y procesamiento de archivos HTML (506 documentos de prueba)
- Sprints: 5 (documentados en `README_SCRUM.md` y `SPRINT_PLANNING_COMPLETO.md`)
- Resultado: sistema funcional con CLI y Web UI (Flask), índice TF-IDF, posting lists y pruebas de carga documentadas.

---

## Mapeo de la rúbrica a evidencias (criterios principales)

Nota: Para cada criterio de la rúbrica se indica la puntuación máxima posible y las evidencias concretas (archivos) que demuestran cumplimiento.

### Criterio 1 — Desarrollo e implementación de la metodología SCRUM (28 pts)
- Evidencias:
  - `actv 1/README_SCRUM.md` — Documentación SCRUM completa (historias, sprint review, métricas).
  - `actv 1/SPRINT_PLANNING_COMPLETO.md` — Planificación y backlog por sprint.
  - `actv 1/SCRUM_Y_MINUTA.md` — Minutas y actas de reuniones.
  - `actv 1/BACKLOG.md` — Backlog con historias antes/después de sprints.
- Entregables que respaldan criterios: historias de usuario (al inicio de cada sprint), product backlog antes y después, casos de prueba iterativos, gráfica de velocidad (en `README_SCRUM.md`) y referencias a uso de TFS (documentado en SCRUM y anexos).

### Criterio 2 — Interfaz del buscador (18 pts)
- Evidencias:
  - `actv 1/web_app.py` — Servidor Flask que expone la UI y endpoints (`/`, `/search`, `/document/<id>`).
  - `actv 1/templates/index.html` (o plantilla en `templates/`) — Página web con buscador y listado de resultados.
  - `actv 1/retrieve.py` y `actv 1/retrieve_optimized.py` — Implementaciones backend/CGI-equivalente para búsquedas.
  - `actv 1/activity15/PERFORMANCE_REPORT.md` — Documenta pruebas y dirección del buscador usada para las pruebas.
- Comentario: La UI lista resultados (top 10) y permite ver documentos; los endpoints y logs respaldan funcionamiento 100% o parcial según versión (memoria vs disco).

### Criterio 3 — Desempeño y funcionalidad del buscador (28 pts)
- Evidencias:
  - `actv 1/data/output/activity11/dictionary.txt` y `posting.txt` — Archivos de diccionario e índice (acceso desde disco).
  - `actv 1/benchmark_tokenize_results.txt` y `actv 1/benchmark_tokenize.py` — Resultados de tokenización y throughput.
  - `actv 1/README_FASE4.md` y `actv 1/README_FASE5.md` — Documentación técnica de TF‑IDF, hash index y optimizaciones.
  - `actv 1/cached_searcher.py` — Implementación con caché (stopwords y normalización de tokens).
- Comentario: Se demuestra acceso desde disco al índice (actividad 13), tokens en minúsculas, stopwords aplicadas y diagramas/estadísticas incluidas en los README de fase.

### Criterio 4 — Pruebas y consultas (evidencia de ejecución) (28 pts)
- Evidencias:
  - `actv 1/activity15/load_test_*.json` y `activity15/load_test_*.txt` — Resultados de pruebas de carga y métricas (RPS, latencias, percentiles).
  - `actv 1/load_test.py` y `actv 1/load_test_quick.py` — Scripts usados para las pruebas.
  - `actv 1/activity15/PERFORMANCE_REPORT.md` — Reporte de las pruebas, incluyendo capturas/prints y enlaces a la URL del buscador (http://localhost:5000 durante pruebas).
  - Logs `a11_*.txt`, `a12_*.txt`, `a13_*.txt` (en `data/output/` o raíz de activity) — Registro de búsquedas y tiempos.
- Comentario: Se presentan resultados reproducibles y capturas/archivos JSON con métricas, además de enlaces y rutas de documentos.

---

## Evidencias de competencias y criterios 5–12 (1 pt c/u)

Los criterios 5–12 (compromiso activo, metas de trabajo, identificación de programas de bienestar, acciones para cambios, pronóstico de cambios, toma de decisiones, visión global, tecnología y ambiente sustentable) se documentan en:

- `actv 1/README_SCRUM.md` — Roles del equipo, minutas, participación en metas y responsabilidades.
- `actv 1/SPRINT_PLANNING_COMPLETO.md` — Evidencia de participación en metas del equipo y decisiones de priorización.
- `actv 1/CODE_REVIEW_SUMMARY.md` y `CODE_REVIEW.md` — Toma de decisiones técnicas, revisiones y mejoras propuestas.
- `actv 1/DOCUMENTACION_COMPLETA.md` y `INDICE_DOCUMENTACION.md` — Visión global del proyecto y consideraciones de sostenibilidad/tecnología.

Estos documentos contienen descripciones de la participación del equipo, decisiones tomadas, propuestas de mejora y previsiones de impacto (pronósticos), que son la evidencia requerida para estos criterios.

---

## Cómo revisar las evidencias (inmediato)

1. Abrir `actv 1/README_SCRUM.md` para ver el registro SCRUM, historias por sprint y la gráfica de velocidad.
2. Ejecutar localmente el servidor web para comprobar la interfaz:

```powershell
cd "c:\Users\ricoj\OneDrive\Escritorio\proyING\actv 1"
python web_app.py
# Abrir http://localhost:5000 en un navegador
```

3. Reproducir pruebas rápidas:

```powershell
python load_test_quick.py
cat activity15\quick_test_*.json
```

4. Inspeccionar índices y logs:

- `data/output/activity11/dictionary.txt`
- `data/output/activity11/posting.txt`
- `activity15/load_test_*.json` y `activity15/PERFORMANCE_REPORT.md`

---

## Archivos clave y rutas (resumen)

- SCRUM / planificación:
  - `actv 1/README_SCRUM.md`
  - `actv 1/SPRINT_PLANNING_COMPLETO.md`
  - `actv 1/BACKLOG.md`
- Interfaz / Web:
  - `actv 1/web_app.py`
  - `actv 1/templates/index.html` - plantilla (si existe en proyecto)
  - `actv 1/cached_searcher.py`
- Búsqueda / CLI:
  - `actv 1/retrieve.py`
  - `actv 1/retrieve_optimized.py`
- Índices y outputs:
  - `actv 1/data/output/activity11/dictionary.txt`
  - `actv 1/data/output/activity11/posting.txt`
  - `actv 1/data/output/activity11/documents.txt`
- Benchmarks y pruebas:
  - `actv 1/benchmark_tokenize_results.txt`
  - `actv 1/activity15/PERFORMANCE_REPORT.md`
  - `actv 1/activity15/load_test_*.json`

---

## Conclusión y recomendaciones para el evaluador

- La evidencia está organizada y localizada en los archivos listados arriba. Cada criterio de la rúbrica tiene al menos un artefacto que lo respalda (documentación SCRUM, listas de historias, logs, índices, UI y reportes de performance).
- Recomendación: para la máxima puntuación, revisar en orden: `README_SCRUM.md` (metodología), `web_app.py` + `templates/` (interfaz), `data/output/...` (índices y tokens), y `activity15/PERFORMANCE_REPORT.md` (pruebas y capturas).

