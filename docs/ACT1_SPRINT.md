# Actividad 1: Medición de Tiempos - Sprint

## Sprint Goal
Implementar sistema de medición de tiempos de apertura para archivos HTML y generar reportes detallados.

## Historia de Usuario (HU-01)
**Como** docente evaluador  
**Quiero** medir el tiempo que toma abrir cada archivo HTML  
**Para** establecer una línea base de rendimiento del sistema

### Criterios de Aceptación
1. ✓ Medir tiempo individual por archivo HTML
2. ✓ Medir tiempo total del programa
3. ✓ Generar reporte en formato a1_matricula.txt
4. ✓ Ordenar archivos alfabéticamente
5. ✓ Incluir estadísticas (promedio, máximo, mínimo)

### Tareas Técnicas
- [H] Implementar función open_file con time.perf_counter()
- [H] Desarrollar manejo de múltiples codificaciones:
  - utf-8
  - latin-1
  - cp1252
  - iso-8859-1
- [E] Crear script de automatización (ejecutar.bat)
- [SM] Documentar proceso en README.md

### Definition of Done
- Script buscador_html.py funcionando
- Reporte a1_matricula.txt generado correctamente
- Tiempos medidos con precisión específica
- Documentación completa
- Pruebas exitosas con todo el corpus

## Retrospectiva

### Lo que funcionó bien
- Uso de time.perf_counter() para precisión
- Manejo de múltiples codificaciones
- Automatización con batch file

### Áreas de mejora
- Considerar paralelización futura
- Agregar más estadísticas
- Mejorar formato del reporte

### Acciones para siguiente sprint
- Implementar manejo de errores más robusto
- Documentar mejor las codificaciones soportadas
- Considerar cache para archivos frecuentes

## Métricas
- Velocidad: 8 story points completados
- Precisión: Alta (microsegundos)
- Satisfacción PO: 9/10

## Entregables
1. buscador_html.py
2. ejecutar.bat
3. a1_matricula.txt
4. README.md

## Estado Final
✓ COMPLETADO
- Todos los criterios cumplidos
- Pruebas pasadas
- Documentación actualizada
- Review aprobada por PO