# Plan Integral de Sprints - Procesamiento de Archivos HTML
## Equipo Scrum
- **Product Owner:** JOSE GPE RICO MORENO
- **Scrum Master:** Melanie Esmeralda Garza Guajardo
- **Developers:**
  - Hilary Vanessa Camacho Alvarez
  - Eduardo Luis Macouzet Calles

## Visión del Producto
Desarrollar un sistema robusto de procesamiento de archivos HTML que permita medir tiempos de acceso, limpiar contenido, extraer y analizar palabras, y generar estadísticas detalladas de uso de vocabulario.

## Definición de "Done" Global
- Código fuente documentado y versionado
- Pruebas ejecutadas y pasadas
- Reportes de tiempos generados
- Documentación actualizada
- Review del Product Owner completada
- Archivos de salida verificados

## Sprint 1: Medición de Tiempos Base
**Duración:** 1 semana
**Meta:** Establecer línea base de tiempos de acceso a archivos HTML

### Historia de Usuario HU-01
**Como** docente evaluador  
**Quiero** medir el tiempo de apertura de cada archivo HTML  
**Para** establecer una línea base de rendimiento del sistema

#### Criterios de Aceptación
1. Medir tiempo individual por archivo
2. Calcular tiempo total de ejecución
3. Generar reporte a1_matricula.txt
4. Ordenar archivos alfabéticamente
5. Incluir estadísticas (promedio, máx, mín)

#### Tareas Técnicas
- [H] Implementar función open_file con time.perf_counter()
- [H] Desarrollar manejo de codificaciones (utf-8, latin-1, etc.)
- [E] Crear script de automatización
- [SM] Documentar en README.md

#### Definition of Done
- ✓ Reporte generado con formato correcto
- ✓ Tiempos medidos con precisión decimal especificada
- ✓ Código documentado y probado
- ✓ Batch file funcional

## Sprint 2: Limpieza de HTML
**Duración:** 1 semana
**Meta:** Implementar sistema de limpieza de etiquetas HTML

### Historia de Usuario HU-02
**Como** analista de contenido  
**Quiero** obtener el texto limpio sin etiquetas HTML  
**Para** analizar el contenido real de los documentos

#### Criterios de Aceptación
1. Eliminar todas las etiquetas HTML
2. Preservar el texto contenido
3. Generar archivos *_clean.txt
4. Crear reporte a2_matricula.txt
5. Medir tiempos de procesamiento

#### Tareas Técnicas
- [E] Implementar regex para limpieza de tags
- [E] Desarrollar normalización de espacios
- [H] Crear script de automatización
- [SM] Documentar proceso

#### Definition of Done
- ✓ Archivos limpios generados
- ✓ Reporte de tiempos creado
- ✓ Tests de limpieza pasados
- ✓ Documentación actualizada

## Sprint 3: Extracción de Palabras
**Duración:** 1 semana
**Meta:** Implementar sistema de extracción y ordenamiento de palabras

### Historia de Usuario HU-03
**Como** investigador  
**Quiero** extraer y ordenar todas las palabras únicas  
**Para** analizar el vocabulario usado

#### Criterios de Aceptación
1. Extraer palabras de archivos limpios
2. Eliminar duplicados
3. Ordenar alfabéticamente
4. Generar archivos *_words.txt
5. Crear reporte a3_matricula.txt

#### Tareas Técnicas
- [H] Implementar extracción de palabras
- [H] Desarrollar ordenamiento
- [E] Crear menú integrado
- [SM] Documentar proceso

#### Definition of Done
- ✓ Archivos de palabras generados
- ✓ Palabras correctamente ordenadas
- ✓ Reporte de tiempos creado
- ✓ Menú principal actualizado

## Sprint 4: Consolidación Global
**Duración:** 1 semana
**Meta:** Implementar sistema de consolidación de palabras

### Historia de Usuario HU-04
**Como** analista de datos  
**Quiero** tener todas las palabras únicas consolidadas  
**Para** obtener un vocabulario global del corpus

#### Criterios de Aceptación
1. Consolidar palabras de todos los archivos
2. Eliminar duplicados globales
3. Ordenar alfabéticamente
4. Generar consolidado_palabras.txt
5. Crear reporte a4_matricula.txt

#### Tareas Técnicas
- [E] Implementar consolidación
- [H] Optimizar proceso de unión
- [E] Actualizar menú principal
- [SM] Documentar proceso

#### Definition of Done
- ✓ Archivo consolidado generado
- ✓ Reporte de tiempos creado
- ✓ Menú actualizado
- ✓ Tests pasados

## Sprint 5: Análisis de Frecuencias
**Duración:** 1 semana
**Meta:** Implementar sistema de análisis de frecuencias

### Historia de Usuario HU-05
**Como** investigador lingüístico  
**Quiero** conocer la frecuencia de cada palabra  
**Para** analizar patrones de uso

#### Criterios de Aceptación
1. Contar frecuencia por palabra
2. Generar reporte ordenado alfabéticamente
3. Generar reporte ordenado por frecuencia
4. Crear reporte a5_matricula.txt

#### Tareas Técnicas
- [E] Implementar conteo de frecuencias
- [H] Desarrollar ordenamientos
- [E] Actualizar interfaz
- [SM] Documentar análisis

#### Definition of Done
- ✓ Reportes de frecuencia generados
- ✓ Ordenamientos correctos
- ✓ Tiempos documentados
- ✓ Tests completados

## Sprint 6: Análisis por Documento
**Duración:** 2 semanas
**Meta:** Implementar análisis detallado por documento

### Historia de Usuario HU-06
**Como** analista de corpus  
**Quiero** saber en cuántos documentos aparece cada palabra  
**Para** identificar términos comunes vs específicos

#### Criterios de Aceptación
1. Contar documentos por palabra
2. Generar diccionario de tres columnas:
   - Token
   - Repeticiones totales
   - Número de documentos
3. Crear reporte a6_matricula.txt

#### Tareas Técnicas
- [E] Implementar tracking de documentos
- [H] Optimizar uso de memoria
- [E] Desarrollar formato de salida
- [SM] Documentar estadísticas

#### Definition of Done
- ✓ Diccionario generado correctamente
- ✓ Estadísticas por documento creadas
- ✓ Rendimiento optimizado
- ✓ Documentación completa

## Backlog de Mejoras Futuras
1. Paralelización de procesamiento
2. Interfaz gráfica
3. Exportación a diferentes formatos
4. Análisis semántico
5. API de consulta

## Métricas de Seguimiento
- Velocidad del equipo por sprint
- Tiempo de procesamiento por archivo
- Uso de memoria
- Cobertura de pruebas
- Satisfacción del usuario

## Riesgos Identificados
1. **Rendimiento con archivos grandes**
   - Mitigación: Implementar procesamiento por lotes
2. **Codificación de caracteres**
   - Mitigación: Usar múltiples encodings de respaldo
3. **Consumo de memoria**
   - Mitigación: Optimizar estructuras de datos
4. **Precisión de mediciones**
   - Mitigación: Usar time.perf_counter()

## Dependencias Técnicas
- Python 3.x
- Módulos estándar:
  - time
  - os
  - sys
  - collections
- Herramientas:
  - VS Code
  - Git
  - PowerShell/CMD

## Calendario de Ceremonias
- **Daily Scrum:** 9:00 AM
- **Sprint Planning:** Lunes inicio de sprint
- **Sprint Review:** Viernes fin de sprint
- **Retrospectiva:** Viernes después de Review