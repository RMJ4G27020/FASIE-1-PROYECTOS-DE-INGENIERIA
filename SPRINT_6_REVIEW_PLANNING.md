# Sprint Review y Planning - Actividades 6-9

## Fecha: 27/09/2025
## Participantes
- [PO] JOSE GPE RICO MORENO
- [SM] Melanie Esmeralda Garza Guajardo
- [H] Hilary Vanessa Camacho Alvarez
- [E] Eduardo Luis Macouzet Calles

## Historias de Usuario - Actividad 6 (Detalladas)

### HU-06.1: Tracking de Documentos por Token
**Como** Analista de Datos  
**Quiero** saber en cuántos documentos aparece cada token  
**Para** identificar términos comunes vs específicos de ciertos documentos

#### Criterios de Aceptación
1. Formato de salida con tres columnas:
   - Token (palabra)
   - Repeticiones totales
   - Número de documentos
2. Separación clara entre columnas (tabs)
3. Reporte de tiempos en a6_matricula.txt

**Puntos de historia:** 8  
**Asignado a:** [E]

### HU-06.2: Optimización de Memoria
**Como** Arquitecto de Sistemas  
**Quiero** procesar grandes volúmenes de texto eficientemente  
**Para** escalar el análisis a corpus más grandes

#### Criterios de Aceptación
1. Uso de estructuras de datos optimizadas
2. Procesamiento por lotes
3. Medición de uso de memoria

**Puntos de historia:** 5  
**Asignado a:** [H]

### HU-06.3: Automatización de Pipeline
**Como** DevOps Engineer  
**Quiero** un proceso automatizado de generación de diccionarios  
**Para** facilitar el análisis continuo de nuevos documentos

#### Criterios de Aceptación
1. Script batch con parámetros
2. Integración con menú principal
3. Manejo de errores

**Puntos de historia:** 3  
**Asignado a:** [E]

## Historias Futuras (Actividades 7-9)

### Actividad 7 - Análisis Estadístico
**Como** Científico de Datos  
**Quiero** obtener métricas estadísticas del corpus  
**Para** entender patrones de uso del lenguaje

- Distribución de frecuencias
- Correlaciones entre tokens
- Visualizaciones

### Actividad 8 - Clasificación de Contenido
**Como** Content Manager  
**Quiero** clasificar documentos por similitud léxica  
**Para** organizar el corpus temáticamente

- Clustering de documentos
- Identificación de temas
- Tags automáticos

### Actividad 9 - API de Consulta
**Como** Desarrollador de Aplicaciones  
**Quiero** una API para consultar el diccionario  
**Para** integrar el análisis en otras aplicaciones

- Endpoints REST
- Búsqueda por patrones
- Cache de resultados

## Plan de Sprint Actual (Actividad 6)

### Objetivos
1. Implementar conteo de documentos por token
2. Optimizar procesamiento de memoria
3. Automatizar pipeline completo

### Riesgos
- Consumo de memoria con corpus grandes
- Tiempo de procesamiento
- Codificación de caracteres

### Métricas
- Tiempo de procesamiento por archivo
- Memoria utilizada
- Cobertura de pruebas

## Siguiente Sprint
- Implementación de análisis estadístico
- Diseño de visualizaciones
- Optimización de consultas