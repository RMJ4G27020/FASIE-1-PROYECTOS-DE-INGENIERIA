# Actividad 2: Limpieza HTML - Sprint

## Sprint Goal
Implementar sistema robusto de limpieza de etiquetas HTML preservando el contenido textual.

## Historia de Usuario (HU-02)
**Como** analista de contenido  
**Quiero** obtener el texto limpio sin etiquetas HTML  
**Para** poder analizar el contenido real de los documentos

### Criterios de Aceptación
1. ✓ Eliminar todas las etiquetas HTML
2. ✓ Preservar el texto contenido
3. ✓ Generar archivos *_clean.txt
4. ✓ Crear reporte a2_matricula.txt
5. ✓ Medir y reportar tiempos de procesamiento
6. ✓ Mantener codificación UTF-8

### Tareas Técnicas
- [E] Implementar regex para limpieza `<[^>]+>`
- [E] Desarrollar normalización de espacios/líneas
- [E] Implementar manejo de errores E/S
- [H] Crear automatización (ejecutar_actividad2.bat)
- [SM] Documentar en README_Actividad2.md

### Definition of Done
- Script actividad2_html_cleaner.py funcional
- Archivos limpios generados correctamente
- Reporte de tiempos creado
- Pruebas de limpieza pasadas
- Documentación actualizada

## Retrospectiva

### Lo que funcionó bien
- Regex eficiente para tags
- Normalización de espacios
- Manejo de codificaciones

### Áreas de mejora
- Velocidad en archivos grandes
- Detección de encoding
- Manejo de HTML malformado

### Acciones para siguiente sprint
- Considerar procesamiento paralelo
- Mejorar detección de encoding
- Agregar validación HTML

## Métricas
- Velocidad: 13 story points completados
- Tasa de éxito: 100% archivos procesados
- Satisfacción PO: 9/10

## Entregables
1. actividad2_html_cleaner.py
2. ejecutar_actividad2.bat
3. a2_matricula.txt
4. README_Actividad2.md
5. Carpeta Clean_Files/ con outputs

## Estado Final
✓ COMPLETADO
- Criterios cumplidos
- Tests pasados
- Documentación completa
- Review aprobada