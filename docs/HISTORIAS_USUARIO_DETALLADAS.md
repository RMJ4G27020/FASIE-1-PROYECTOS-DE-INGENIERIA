# Historias de Usuario Detalladas - Procesamiento HTML

## Equipo Scrum
- **Product Owner:** JOSE GPE RICO MORENO [PO]
- **Scrum Master:** Melanie Esmeralda Garza Guajardo [SM]
- **Developers:**
  - Hilary Vanessa Camacho Alvarez [H]
  - Eduardo Luis Macouzet Calles [E]

## HU-01: Medición de Tiempos de Apertura
### Contexto
El sistema procesa una gran cantidad de archivos HTML y necesitamos entender el rendimiento de acceso a estos archivos para optimizar futuros procesamientos.

### Como
Docente evaluador del sistema

### Quiero
Medir con precisión el tiempo que toma:
- Abrir cada archivo HTML individual
- Procesar todo el conjunto de archivos
- Generar estadísticas de rendimiento

### Para
- Establecer una línea base de rendimiento
- Identificar cuellos de botella
- Planificar optimizaciones futuras
- Documentar el comportamiento del sistema

### Detalles Técnicos
1. **Medición Individual**
   - Usar time.perf_counter() para precisión microsegundos
   - Registrar tiempo de apertura por archivo
   - Manejar múltiples codificaciones (utf-8, latin-1, etc.)

2. **Medición Global**
   - Calcular tiempo total de ejecución
   - Generar estadísticas (min, max, promedio)
   - Ordenar resultados alfabéticamente

3. **Reporte**
   - Formato: a1_matricula.txt
   - Incluir timestamp de ejecución
   - Mostrar métricas detalladas

### Criterios de Éxito
1. ✓ **Precisión**
   - Mediciones a nivel de microsegundos
   - Consistencia en múltiples ejecuciones

2. ✓ **Completitud**
   - Todos los archivos procesados
   - Estadísticas generadas
   - Reporte creado

3. ✓ **Usabilidad**
   - Automatizado via batch
   - Mensajes claros de progreso
   - Manejo de errores

## HU-02: Limpieza de Contenido HTML
### Contexto
Los archivos HTML contienen etiquetas que no son relevantes para el análisis de contenido. Necesitamos extraer solo el texto útil.

### Como
Analista de contenido textual

### Quiero
- Eliminar todas las etiquetas HTML
- Preservar el contenido textual relevante
- Normalizar espacios y líneas vacías
- Mantener la codificación correcta

### Para
- Analizar el contenido real de los documentos
- Preparar texto para procesamiento posterior
- Facilitar análisis lingüístico

### Detalles Técnicos
1. **Limpieza HTML**
   - Regex: `<[^>]+>` para tags
   - Preservar texto entre etiquetas
   - Manejar HTML malformado

2. **Normalización**
   - Espacios múltiples → único
   - Líneas vacías → una
   - UTF-8 para output

3. **Validación**
   - Verificar contenido preservado
   - Confirmar eliminación de tags
   - Medir tasa de éxito

### Criterios de Éxito
1. ✓ **Limpieza**
   - Sin etiquetas HTML
   - Texto preservado
   - Espacios normalizados

2. ✓ **Performance**
   - Tiempo por archivo registrado
   - Memoria optimizada
   - Escalable a corpus grande

## HU-03: Extracción y Ordenamiento de Palabras
### Contexto
Necesitamos identificar y analizar el vocabulario único usado en cada documento HTML limpio.

### Como
Investigador lingüístico/Analista léxico

### Quiero
- Extraer palabras únicas de cada archivo
- Normalizar a minúsculas
- Ordenar alfabéticamente
- Generar archivo por documento

### Para
- Analizar vocabulario usado
- Preparar para análisis de frecuencia
- Facilitar búsqueda de términos

### Detalles Técnicos
1. **Extracción**
   - Regex: `\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b`
   - Manejo de palabras compuestas
   - Eliminación de duplicados

2. **Procesamiento**
   - Conversión a minúsculas
   - Set para unicidad
   - Sorted() para orden

3. **Output**
   - Un archivo *_words.txt por input
   - Una palabra por línea
   - UTF-8 encoding

### Criterios de Éxito
1. ✓ **Precisión**
   - Solo palabras válidas
   - Sin duplicados
   - Orden correcto

2. ✓ **Completitud**
   - Todos los archivos procesados
   - Reportes generados
   - Estadísticas claras

## HU-04: Consolidación de Vocabulario Global
### Contexto
Necesitamos una vista unificada de todo el vocabulario presente en el corpus.

### Como
Analista de datos textuales

### Quiero
- Unificar palabras de todos los archivos
- Eliminar duplicados globales
- Mantener orden alfabético
- Medir tiempos del proceso

### Para
- Obtener vocabulario completo del corpus
- Analizar riqueza léxica global
- Preparar para análisis estadístico

### Detalles Técnicos
1. **Consolidación**
   - Lectura de todos *_words.txt
   - Set para unicidad global
   - Ordenamiento final

2. **Performance**
   - Medición de tiempos
   - Optimización de memoria
   - Manejo de archivos grandes

3. **Reportes**
   - consolidado_palabras.txt
   - a4_matricula.txt con tiempos
   - Estadísticas globales

### Criterios de Éxito
1. ✓ **Datos**
   - Todas las palabras únicas
   - Orden correcto
   - Sin pérdida de información

2. ✓ **Eficiencia**
   - Tiempo razonable
   - Memoria optimizada
   - Escalable

## HU-05: Análisis de Frecuencias
### Contexto
Necesitamos entender la distribución y frecuencia de uso de las palabras en el corpus.

### Como
Investigador lingüístico/Estadístico

### Quiero
- Contar frecuencias por palabra
- Generar múltiples vistas ordenadas
- Procesar archivos específicos
- Medir rendimiento

### Para
- Analizar patrones de uso
- Identificar términos comunes
- Estudiar distribución léxica

### Detalles Técnicos
1. **Procesamiento**
   - Archivos target específicos
   - Conteo de frecuencias
   - Doble ordenamiento

2. **Vistas**
   - Orden alfabético
   - Orden por frecuencia
   - Formato tabular

3. **Medición**
   - Tiempo por archivo
   - Tiempo de ordenamiento
   - Tiempo total

### Criterios de Éxito
1. ✓ **Precisión**
   - Conteos exactos
   - Ordenamientos correctos
   - Reportes claros

2. ✓ **Usabilidad**
   - CLI con parámetros
   - Mensajes claros
   - Reportes formatados

## HU-06: Análisis por Documento
### Contexto
Necesitamos entender no solo cuánto se usa cada palabra, sino también su distribución entre documentos.

### Como
Analista de corpus lingüístico

### Quiero
- Contar repeticiones totales
- Contar documentos por palabra
- Generar diccionario triple
- Medir tiempos detallados

### Para
- Identificar términos transversales
- Detectar vocabulario específico
- Analizar coherencia del corpus

### Detalles Técnicos
1. **Diccionario**
   - Tres columnas separadas por tabs
   - Token | Repeticiones | #Documentos
   - Optimización de memoria

2. **Procesamiento**
   - Tracking por documento
   - Conteo eficiente
   - Manejo de memoria

3. **Reportes**
   - dictionary.txt
   - a6_matricula.txt
   - Estadísticas completas

### Criterios de Éxito
1. ✓ **Datos**
   - Conteos precisos
   - Tracking correcto
   - Formato claro

2. ✓ **Performance**
   - Memoria optimizada
   - Tiempo razonable
   - Escalable

## Matriz de Trazabilidad
| Historia | Dependencias | Prioridad | Complejidad | Sprint |
|----------|--------------|-----------|-------------|---------|
| HU-01    | Ninguna     | Alta      | Media       | 1       |
| HU-02    | HU-01       | Alta      | Alta        | 2       |
| HU-03    | HU-02       | Alta      | Media       | 3       |
| HU-04    | HU-03       | Media     | Baja        | 4       |
| HU-05    | HU-04       | Media     | Alta        | 5       |
| HU-06    | HU-05       | Baja      | Alta        | 6       |