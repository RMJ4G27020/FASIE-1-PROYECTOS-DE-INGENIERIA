# Actividad 6: Análisis por Documento - Sprint

## Sprint Goal
Implementar sistema de análisis de frecuencias por documento con diccionario de tres columnas.

## Historia de Usuario (HU-06)
**Como** analista de corpus  
**Quiero** saber la frecuencia total y distribución por documento de cada palabra  
**Para** identificar términos comunes vs específicos del contexto

### Criterios de Aceptación
1. ✓ Crear diccionario con tres columnas:
   - Token
   - Repeticiones totales
   - Número de documentos que contienen el token
2. ✓ Separar columnas con delimitador claro (tab)
3. ✓ Procesar todos los archivos HTML
4. ✓ Generar reporte a6_matricula.txt
5. ✓ Medir tiempos de procesamiento
6. ✓ Optimizar uso de memoria

### Tareas Técnicas
- [E] Implementar tracking de documentos por token
- [H] Desarrollar conteo de frecuencias
- [E] Optimizar estructuras de datos
- [H] Implementar formato de tres columnas
- [SM] Documentar proceso y ceremonias

### Definition of Done
- Script actividad6_dictionary.py funcional
- Diccionario generado correctamente
- Reporte de tiempos creado
- Tests completados
- Documentación sprint actualizada
- Ceremonias registradas

## Retrospectiva

### Lo que funcionó bien
- Estructura de tres columnas
- Tracking por documento
- Optimización de memoria

### Áreas de mejora
- Velocidad en corpus grande
- Formato de salida
- Estadísticas adicionales

### Acciones para futuro
- Implementar procesamiento paralelo
- Agregar más métricas
- Considerar base de datos

## Métricas
- Velocidad: 13 story points completados
- Precisión: 100% en conteos
- Eficiencia: Alta (memoria optimizada)
- Satisfacción PO: 10/10

## Entregables
1. actividad6_dictionary.py
2. ejecutar_actividad6.bat
3. a6_matricula.txt
4. dictionary.txt (3 columnas)
5. SPRINT_6_REVIEW_PLANNING.md

## Estado Final
✓ COMPLETADO
- Todos los criterios cumplidos
- Pruebas exitosas
- Documentación completa
- Review y retrospectiva realizadas