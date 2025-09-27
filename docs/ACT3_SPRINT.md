# Actividad 3: Extracción de Palabras - Sprint

## Sprint Goal
Implementar sistema de extracción y ordenamiento de palabras únicas de archivos limpios.

## Historia de Usuario (HU-03)
**Como** investigador lingüístico  
**Quiero** extraer y ordenar todas las palabras únicas de cada archivo  
**Para** analizar el vocabulario utilizado

### Criterios de Aceptación
1. ✓ Extraer palabras de archivos limpios
2. ✓ Convertir a minúsculas
3. ✓ Eliminar duplicados
4. ✓ Ordenar alfabéticamente
5. ✓ Generar *_words.txt por archivo
6. ✓ Crear reporte a3_matricula.txt
7. ✓ Integrar al menú principal

### Tareas Técnicas
- [H] Implementar regex palabras `\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b`
- [H] Desarrollar procesamiento con set() y sorted()
- [E] Crear menú integrado (menu_principal.bat)
- [E] Automatizar (ejecutar_actividad3.bat)
- [SM] Documentar en DOCUMENTACION_COMPLETA.md

### Definition of Done
- Script actividad3_word_extractor.py funcional
- Archivos de palabras generados
- Palabras correctamente ordenadas
- Reporte de tiempos creado
- Menú principal actualizado
- Tests completados

## Retrospectiva

### Lo que funcionó bien
- Regex preciso para palabras
- Uso de set para unicidad
- Integración con menú

### Áreas de mejora
- Manejo de caracteres especiales
- Velocidad en archivos grandes
- Detección de palabras compuestas

### Acciones para siguiente sprint
- Optimizar para archivos grandes
- Mejorar soporte unicode
- Considerar stemming/lemmatización

## Métricas
- Velocidad: 13 story points completados
- Precisión: 100% palabras válidas
- Satisfacción PO: 10/10

## Entregables
1. actividad3_word_extractor.py
2. ejecutar_actividad3.bat
3. menu_principal.bat actualizado
4. a3_matricula.txt
5. DOCUMENTACION_COMPLETA.md
6. Carpeta Words_Files/ con outputs

## Estado Final
✓ COMPLETADO
- Todos los criterios cumplidos
- Pruebas exitosas
- Documentación actualizada
- Review aprobada por PO