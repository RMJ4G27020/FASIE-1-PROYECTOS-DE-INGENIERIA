# Minuta de Sprint Review - Actividad 5

## Fecha: 27/09/2025
## Participantes
- [PO] JOSE GPE RICO MORENO
- [SM] Melanie Esmeralda Garza Guajardo
- [H] Hilary Vanessa Camacho Alvarez
- [E] Eduardo Luis Macouzet Calles

## Historias de Usuario Revisadas

### HU-05: Tokenización y Análisis de Frecuencias
**Como** investigador del corpus HTML  
**Quiero** obtener la frecuencia de cada palabra en archivos específicos  
**Para** analizar patrones de uso y relevancia de términos

#### Criterios de Aceptación
1. Procesar archivos específicos:
   - simple.html
   - medium.html
   - hard.html
   - 49.html
2. Generar archivo individual por cada input con tokens y frecuencias
3. Crear consolidado alfabético con todas las palabras y frecuencias
4. Crear consolidado ordenado por frecuencia descendente
5. Medir y reportar tiempos de procesamiento

#### Detalles Técnicos
- **Entrada:** Directorio con archivos HTML
- **Salida:** 
  - Directorio con *_tokens.txt por archivo
  - consolidated_alpha.txt
  - consolidated_byfreq.txt
  - a5_matricula.txt (reporte de tiempos)
- **Interfaz:** tokenize.bat input-dir output-dir

### HU-06: Automatización y CLI
**Como** usuario técnico  
**Quiero** ejecutar el procesamiento vía línea de comandos  
**Para** automatizar el análisis en diferentes directorios

#### Criterios de Aceptación
1. Aceptar directorios input/output como parámetros
2. Validar existencia de archivos requeridos
3. Crear directorios de salida si no existen
4. Reportar errores claramente

## Resultados del Sprint

### Completado
- [x] Diseño de arquitectura de tokenización
- [x] Implementación de conteo de frecuencias
- [x] Generación de reportes ordenados
- [x] CLI con parámetros

### Pendiente
- [ ] Optimización para archivos grandes
- [ ] Paralelización del procesamiento
- [ ] Interfaz web (backlog futuro)

## Decisiones Técnicas
1. Uso de Counter para eficiencia en conteo
2. Ordenamiento compuesto (frecuencia + alfabético)
3. Medición granular de tiempos por fase

## Siguiente Sprint
- Evaluar rendimiento con corpus completo
- Implementar procesamiento paralelo
- Añadir filtros de stopwords