#!/usr/bin/env python3
"""
Actividad 14: Servidor Web - Motor de Búsqueda
==============================================

Aplicación web Flask para interfaz del motor de búsqueda.
Permite búsqueda de tokens con ranking TF-IDF y resultados ordenados.

Requisitos:
    pip install flask

Uso:
    python web_app.py
    
    Abrir navegador en: http://localhost:5000

Autor: JOSE GPE RICO MORENO
Fecha: Noviembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import json
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importar buscador optimizado con caché
from cached_searcher import CachedSearcher

# Crear aplicación Flask
app = Flask(__name__)

# Inicializar buscador global (se carga al iniciar el servidor)
print("Inicializando motor de búsqueda...")
data_dir = PROJECT_ROOT / "data" / "output"
searcher = CachedSearcher(str(data_dir), use_stop_list=True)
print(f"Motor listo: {len(searcher.token_line_index)} tokens indexados\n")


@app.route('/')
def index():
    """Página principal con formulario de búsqueda"""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """
    Endpoint de búsqueda
    
    Recibe: query (string con uno o más tokens)
    Retorna: JSON con resultados ordenados por ranking
    """
    try:
        # Obtener query del formulario
        query = request.form.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Por favor ingrese un término de búsqueda',
                'results': []
            })
        
        # Medir tiempo de búsqueda
        start_time = time.time()
        
        # Tokenizar query (separar por espacios)
        tokens = query.lower().split()
        
        # Buscar en el motor
        if len(tokens) == 1:
            results = searcher.search_token(tokens[0])
        else:
            results = searcher.search_multiple_tokens(tokens)
        
        # Tiempo de búsqueda
        search_time = time.time() - start_time
        
        # Formatear resultados para JSON
        formatted_results = []
        for i, doc in enumerate(results[:50], 1):  # Top 50 resultados
            doc_id = doc.get('doc_id', 0)
            doc_name = doc.get('doc_name', 'unknown')
            
            # Construir URL del documento
            doc_url = f"/document/{doc_id}"
            
            # Obtener score
            if 'total_tfidf' in doc:
                score = doc['total_tfidf']
            else:
                score = doc.get('tfidf', 0)
            
            formatted_results.append({
                'rank': i,
                'document': doc_name,
                'url': doc_url,
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
    """
    Muestra el contenido de un documento con resaltado de palabras
    
    Args:
        doc_id: ID del documento
    Query params:
        highlight: Palabras a resaltar (separadas por coma)
    """
    try:
        # Buscar información del documento
        if doc_id not in searcher.doc_names:
            return f"<h1>Error 404</h1><p>Documento {doc_id} no encontrado</p>", 404
        
        doc_name = searcher.doc_names[doc_id]
        
        # Construir path al archivo HTML
        html_file = PROJECT_ROOT / "data" / "input" / "Files" / doc_name
        
        if not html_file.exists():
            return f"<h1>Error 404</h1><p>Archivo {doc_name} no encontrado</p>", 404
        
        # Leer contenido del documento
        content = ""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Intentar con otras codificaciones
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(html_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
        
        # Obtener palabras a resaltar
        highlight_param = request.args.get('highlight', '')
        highlight_words = [w.strip().lower() for w in highlight_param.split(',') if w.strip()]
        
        # DEBUG
        print(f"DEBUG: highlight_param = '{highlight_param}'")
        print(f"DEBUG: highlight_words = {highlight_words}")
        print(f"DEBUG: Condition = {bool(highlight_words and highlight_param)}")
        
        # Si hay palabras para resaltar, inyectar JavaScript para resaltado
        if highlight_words and highlight_param:
            # Convertir lista de palabras a formato JSON seguro
            words_json = json.dumps(highlight_words)
            
            highlight_script = f"""
            <script>
                (function() {{
                    if (window.highlightApplied) return; // Evitar recursión
                    window.highlightApplied = true;
                    
                    const words = {words_json};
                    
                    function highlightTextNodes(node) {{
                        if (node.nodeType === Node.TEXT_NODE) {{
                            let text = node.textContent;
                            let changed = false;
                            
                            words.forEach(word => {{
                                const regex = new RegExp('\\\\b(' + word + ')\\\\b', 'gi');
                                if (regex.test(text)) {{
                                    changed = true;
                                    text = text.replace(regex, '<mark class="highlight">$1</mark>');
                                }}
                            }});
                            
                            if (changed) {{
                                const span = document.createElement('span');
                                span.innerHTML = text;
                                node.parentNode.replaceChild(span, node);
                            }}
                        }} else if (node.nodeType === Node.ELEMENT_NODE && 
                                   node.tagName !== 'SCRIPT' && 
                                   node.tagName !== 'STYLE' &&
                                   node.tagName !== 'MARK') {{
                            Array.from(node.childNodes).forEach(highlightTextNodes);
                        }}
                    }}
                    
                    document.addEventListener('DOMContentLoaded', function() {{
                        highlightTextNodes(document.body);
                        
                        // Scroll a la primera marca
                        setTimeout(function() {{
                            const firstMark = document.querySelector('mark.highlight');
                            if (firstMark) {{
                                firstMark.style.backgroundColor = '#ff6b6b';
                                firstMark.style.fontWeight = 'bold';
                                firstMark.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            }}
                        }}, 100);
                    }});
                }})();
            </script>
            <style>
                mark.highlight {{
                    background-color: yellow;
                    padding: 2px 4px;
                    border-radius: 3px;
                    animation: highlight-pulse 1s ease-in-out;
                }}
                @keyframes highlight-pulse {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.7; }}
                }}
            </style>
            """
            
            # Inyectar antes de </body> o </BODY> o al final
            # Buscar el índice de </body> (case insensitive)
            body_tag_lower = content.lower().rfind('</body>')
            if body_tag_lower != -1:
                # Insertar el script antes del </body>
                content = content[:body_tag_lower] + highlight_script + content[body_tag_lower:]
            else:
                content += highlight_script
        
        # Retornar contenido del documento
        return content
    
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500


@app.route('/stats')
def stats():
    """Estadísticas del motor de búsqueda"""
    return jsonify({
        'total_tokens': len(searcher.token_line_index),
        'total_documents': len(searcher.doc_names),
        'index_type': 'Optimized (Disk-based)',
        'use_stop_list': searcher.use_stop_list
    })


@app.route('/health')
def health():
    """Health check para pruebas de carga"""
    return jsonify({'status': 'ok', 'timestamp': time.time()})


if __name__ == '__main__':
    print("=" * 80)
    print("MOTOR DE BUSQUEDA - SERVIDOR WEB")
    print("=" * 80)
    print("Servidor iniciado en: http://localhost:5000")
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 80 + "\n")
    
    # Iniciar servidor Flask
    app.run(
        host='0.0.0.0',  # Accesible desde red local
        port=5000,
        debug=False,  # Desactivar debug para pruebas de carga
        threaded=True  # Soportar múltiples peticiones concurrentes
    )
