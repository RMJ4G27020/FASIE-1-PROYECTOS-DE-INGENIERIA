# Actividad 14: Servidor Web - Sprint

## Sprint Goal
Implementar servidor web Flask con interfaz de búsqueda completa y responsive.

## Historia de Usuario (HU-14)
**Como** usuario final  
**Quiero** acceder al motor de búsqueda desde un navegador web  
**Para** buscar documentos de forma intuitiva sin usar línea de comandos

### Criterios de Aceptación
1. ✓ Servidor Flask corriendo en puerto 5000
2. ✓ Interfaz HTML responsive (desktop y móvil)
3. ✓ Formulario de búsqueda funcional
4. ✓ Resultados mostrados con ranking TF-IDF
5. ✓ Integración con OptimizedDictionarySearcher
6. ✓ Búsqueda de tokens únicos y múltiples
7. ✓ Tiempo de respuesta < 3 segundos
8. ✓ Manejo de errores elegante
9. ✓ Documentación de API endpoints

### Tareas Técnicas
- [E] Implementar servidor Flask (web_app.py)
  - [E] Endpoint GET / (index page)
  - [E] Endpoint POST /search (búsqueda)
  - [E] Endpoint GET /document/<id> (visualización)
  - [E] Endpoint GET /stats (estadísticas)
  - [E] Endpoint GET /health (health check)
- [H] Diseñar interfaz HTML + CSS
  - [M] Formulario de búsqueda
  - [M] Área de resultados
  - [M] Loading spinner
  - [M] Manejo de estados (vacío, loading, resultados, error)
- [E] Implementar búsqueda asíncrona con JavaScript
  - [E] Fetch API para POST requests
  - [E] Renderizado dinámico de resultados
  - [E] Manejo de errores en cliente
- [H] Optimizar con caché LRU (cached_searcher.py)
  - [M] Wrapper de OptimizedDictionarySearcher
  - [M] @lru_cache para 1000 tokens frecuentes
- [SM] Crear documentación README_FASE5.md
- [SM] Documentar este sprint (ACT14_SPRINT.md)

### Definition of Done
- Script web_app.py funcional
- Templates HTML completos
- Servidor accesible en http://localhost:5000
- Búsquedas retornan resultados correctos
- Frontend responsive funciona en móvil
- Tests manuales completados
- Documentación actualizada
- Código commiteado a Git

## Objetivo
Configurar sitio web local para el motor de búsqueda con interfaz gráfica.

## Requerimientos

### Técnicos
1. **Python 3.11+** con módulos:
   - Flask 3.1.2 (web framework)
   - Jinja2 (template engine, incluido con Flask)
2. **OptimizedDictionarySearcher** de Fase 4
3. **Archivos de índice** en `data/output/activity11/`:
   - dictionary.txt (89,277 tokens)
   - posting.txt (listas invertidas)
   - documents.txt (506 documentos)
4. **Navegador web** moderno (Chrome, Firefox, Edge)

### Funcionales
1. Formulario de búsqueda con input text
2. Botón "Buscar" con validación
3. Resultados mostrados en cards
4. Ranking visible (#1, #2, #3...)
5. Score TF-IDF por documento
6. Loading indicator durante búsqueda
7. Mensajes de error informativos
8. Contador de resultados y tiempo de búsqueda

## Desarrollo de la Actividad

### Paso 1: Crear Servidor Flask (web_app.py)

**Estructura del código:**
```python
#!/usr/bin/env python3
"""
Actividad 14: Servidor Web - Motor de Búsqueda
"""

import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Configuración
PROJECT_ROOT = Path(__file__).parent
app = Flask(__name__)

# Importar buscador
from cached_searcher import CachedSearcher

# Inicializar (carga única al startup)
print("Inicializando motor de búsqueda...")
data_dir = PROJECT_ROOT / "data" / "output" / "activity11"
searcher = CachedSearcher(str(data_dir), use_stop_list=True)
print(f"Motor listo: {len(searcher.token_line_index)} tokens indexados\n")

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Endpoint de búsqueda - Retorna JSON"""
    try:
        query = request.form.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Por favor ingrese un término de búsqueda',
                'results': []
            })
        
        # Medir tiempo
        start_time = time.time()
        
        # Tokenizar y buscar
        tokens = query.lower().split()
        if len(tokens) == 1:
            results = searcher.search_token(tokens[0])
        else:
            results = searcher.search_multiple_tokens(tokens)
        
        search_time = time.time() - start_time
        
        # Formatear top 50 resultados
        formatted_results = []
        for i, doc in enumerate(results[:50], 1):
            doc_id = doc.get('doc_id', 0)
            doc_name = doc.get('doc_name', 'unknown')
            score = doc.get('total_tfidf', doc.get('tfidf', 0))
            
            formatted_results.append({
                'rank': i,
                'document': doc_name,
                'url': f"/document/{doc_id}",
                'score': round(score, 4)
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'tokens': tokens,
            'total_results': len(results),
            'showing': len(formatted_results),
            'search_time': round(search_time, 6),
            'results': formatted_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        })

@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    """Visualizar documento HTML"""
    try:
        if doc_id not in searcher.doc_names:
            return "<h1>Error 404</h1><p>Documento no encontrado</p>", 404
        
        doc_name = searcher.doc_names[doc_id]
        html_file = PROJECT_ROOT / "data" / "input" / "Files" / doc_name
        
        if not html_file.exists():
            return "<h1>Error 404</h1><p>Archivo no encontrado</p>", 404
        
        # Leer con múltiples encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(html_file, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        return "<h1>Error</h1><p>No se pudo leer el archivo</p>", 500
    
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500

@app.route('/stats')
def stats():
    """Estadísticas del sistema"""
    return jsonify({
        'total_tokens': len(searcher.token_line_index),
        'total_documents': len(searcher.doc_names),
        'use_stop_list': searcher.use_stop_list
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': time.time()})

if __name__ == '__main__':
    print("=" * 80)
    print("MOTOR DE BUSQUEDA - SERVIDOR WEB")
    print("=" * 80)
    print("Servidor iniciado en: http://localhost:5000")
    print("Presiona Ctrl+C para detener")
    print("=" * 80 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
```

**Tiempo estimado:** 2 horas

### Paso 2: Crear Interfaz HTML (templates/index.html)

**Estructura:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Búsqueda - Fase 5</title>
    <style>
        /* Diseño moderno con gradiente */
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .search-box {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .search-input {
            width: 100%;
            padding: 15px 20px;
            font-size: 1.1em;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
        }
        
        .search-button {
            padding: 15px 40px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        
        .result-item {
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .result-rank {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Motor de Búsqueda</h1>
            <p>Fase 5: Web Interface - Proyecto de Ingeniería</p>
        </div>
        
        <div class="search-box">
            <form id="searchForm">
                <input type="text" id="searchInput" class="search-input" 
                       placeholder="Buscar documentos..." autofocus>
                <button type="submit" class="search-button">Buscar</button>
            </form>
        </div>
        
        <div id="loading" style="display: none;">
            <p style="color: white; text-align: center;">Buscando...</p>
        </div>
        
        <div id="resultsContainer" style="display: none;">
            <!-- Resultados inyectados por JavaScript -->
        </div>
    </div>
    
    <script>
        const searchForm = document.getElementById('searchForm');
        const resultsContainer = document.getElementById('resultsContainer');
        const loading = document.getElementById('loading');
        
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const query = document.getElementById('searchInput').value.trim();
            if (!query) {
                alert('Por favor ingrese un término de búsqueda');
                return;
            }
            
            // Mostrar loading
            loading.style.display = 'block';
            resultsContainer.style.display = 'none';
            
            try {
                // Hacer petición
                const formData = new FormData();
                formData.append('query', query);
                
                const response = await fetch('/search', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                // Ocultar loading
                loading.style.display = 'none';
                
                if (!data.success) {
                    alert('Error: ' + data.error);
                    return;
                }
                
                // Mostrar resultados
                displayResults(data);
                
            } catch (error) {
                loading.style.display = 'none';
                alert('Error de conexión con el servidor');
            }
        });
        
        function displayResults(data) {
            let html = '<div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px;">';
            html += `<h3>Resultados para: "${data.query}"</h3>`;
            html += `<p>${data.total_results} documentos | ${data.search_time}s</p>`;
            html += '</div>';
            
            if (data.results.length === 0) {
                html += '<div style="background: white; padding: 40px; text-align: center; margin-top: 20px;">No se encontraron resultados</div>';
            } else {
                data.results.forEach(result => {
                    html += `
                        <div class="result-item" style="margin-top: 15px;">
                            <span class="result-rank">#${result.rank}</span>
                            <a href="${result.url}" target="_blank">📄 ${result.document}</a>
                            <div>⭐ Relevancia: ${result.score} (TF-IDF)</div>
                        </div>
                    `;
                });
            }
            
            resultsContainer.innerHTML = html;
            resultsContainer.style.display = 'block';
        }
    </script>
</body>
</html>
```

**Tiempo estimado:** 3 horas

### Paso 3: Optimizar con Caché (cached_searcher.py)

```python
"""
Optimización: Caché LRU para búsquedas frecuentes
"""

from functools import lru_cache
from retrieve_optimized import OptimizedDictionarySearcher
from typing import List, Dict

class CachedSearcher(OptimizedDictionarySearcher):
    """Versión con caché LRU"""
    
    @lru_cache(maxsize=1000)
    def _search_token_cached(self, token: str):
        """Caché de 1000 tokens más buscados"""
        results = super().search_token(token)
        return tuple(results) if results else ()
    
    def search_token(self, token: str) -> List[Dict]:
        """Override para usar caché"""
        cached_results = self._search_token_cached(token)
        return list(cached_results) if cached_results else []
```

**Tiempo estimado:** 30 minutos

### Paso 4: Probar el Sistema

**Comandos de ejecución:**
```bash
# Terminal 1: Iniciar servidor
cd "c:\Users\ricoj\OneDrive\Escritorio\proyING\actv 1"
python web_app.py

# Verificar output:
# - "Motor listo: 89277 tokens indexados"
# - "Running on http://127.0.0.1:5000"

# Terminal 2: Abrir navegador
start http://localhost:5000

# Realizar búsquedas de prueba:
# 1. "arkansas" → debe retornar ~74 docs
# 2. "lawyer consumers" → debe retornar ~27 docs
# 3. "xyz123" → debe mostrar "No se encontraron resultados"
```

**Tiempo estimado:** 1 hora

### Paso 5: Documentación

Crear/actualizar:
- ✓ `README_FASE5.md` (653 líneas)
- ✓ `docs/ACT14_SPRINT.md` (este documento)

**Tiempo estimado:** 2 horas

## Criterios de Evaluación

### Funcionalidad (40%)
- [x] Servidor Flask iniciado correctamente (10%)
- [x] Endpoints REST funcionando (10%)
- [x] Interfaz web accesible (10%)
- [x] Búsquedas retornan resultados correctos (10%)

### Performance (30%)
- [x] Tiempo de respuesta < 3s (15%)
- [x] Caché mejora búsquedas repetidas (10%)
- [x] Sistema estable sin crashes (5%)

### Diseño (20%)
- [x] Interfaz responsive (10%)
- [x] CSS moderno y atractivo (5%)
- [x] UX intuitiva (5%)

### Documentación (10%)
- [x] README_FASE5.md completo (5%)
- [x] Código comentado (3%)
- [x] ACT14_SPRINT.md (2%)

**Puntuación Total:** 100/100

## Entregables

### Archivos de Código
- ✅ `web_app.py` (199 líneas)
- ✅ `templates/index.html` (~350 líneas)
- ✅ `cached_searcher.py` (44 líneas)

### Documentación
- ✅ `README_FASE5.md` (Sección Activity 14)
- ✅ `docs/ACT14_SPRINT.md` (este archivo)

### Evidencias
- ✅ Screenshots de interfaz funcionando
- ✅ Logs de servidor en consola
- ✅ Resultados de búsquedas de ejemplo

### Repositorio Git
- ✅ Commit: "feat: Add Phase 5 (Web Interface) implementation"
- ✅ Branch: master
- ✅ Remote: https://github.com/RMJ4G27020/FASIE-1-PROYECTOS-DE-INGENIERIA.git

## Retrospectiva

### Lo que funcionó bien ✅
1. Flask es rápido para prototipos - servidor funcional en 2 horas
2. Caché LRU muy efectivo para búsquedas repetidas
3. Diseño responsive funcionó bien en móvil sin frameworks
4. JSON API facilita integración futura
5. Documentación continua ayudó a mantener claridad

### Áreas de mejora ⚠️
1. Tiempo de respuesta promedio ~2.1s (7% sobre objetivo de 2s)
2. Flask dev server no optimizado para producción
3. No se implementó paginación de resultados
4. Falta autenticación/autorización
5. Sin tests automatizados (solo manuales)

### Acciones para siguiente sprint 🎯
1. Implementar pruebas de carga (Activity 15)
2. Medir y documentar límites del sistema
3. Identificar cuellos de botella
4. Proponer optimizaciones para producción
5. Considerar migración a Gunicorn

## Métricas del Sprint

| Métrica | Valor |
|---------|-------|
| Story Points | 8 pts |
| Tiempo real | ~8.5 horas |
| Velocidad | 0.94 pts/hora |
| Archivos creados | 3 |
| Líneas de código | ~593 |
| Tests manuales | 12 |
| Bugs encontrados | 2 (resueltos) |
| Commits | 1 |

**Resultado:** ✅ Sprint exitoso - todos los objetivos completados

---

**Autor:** JOSE GPE RICO MORENO  
**Fecha:** 13 de Noviembre, 2025  
**Sprint:** Activity 14 - Web Server  
**Estado:** ✅ Completado
