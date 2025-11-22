#!/usr/bin/env python3
"""
Actividad 13: Búsquedas optimizadas en el diccionario (Fase 4: Query)
======================================================================

Programa retrieve_optimized que:
1. NO carga archivos en memoria (lectura directa desde disco)
2. Usa hash para buscar línea específica en diccionario
3. Lee posting solo para el token buscado
4. Retorna TOP 10 documentos más relevantes (TF-IDF)
5. Soporta múltiples tokens

Uso: python retrieve_optimized.py <token1> [token2] [token3] ...

Autor: JOSE GPE RICO MORENO
Fecha: Noviembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA


class OptimizedDictionarySearcher:
    """Buscador optimizado que NO carga archivos en memoria"""
    
    def __init__(self, data_dir: str, use_stop_list: bool = True):
        """
        Inicializa el buscador optimizado
        
        Args:
            data_dir: Directorio con archivos de diccionario/posting/documentos
            use_stop_list: Si True, usa archivos con stop list
        """
        self.data_dir = Path(data_dir)
        self.use_stop_list = use_stop_list
        
        # Archivos (NO se cargan en memoria)
        if use_stop_list:
            self.dict_file = self.data_dir / "activity11" / "dictionary.txt"
            self.posting_file = self.data_dir / "activity11" / "posting.txt"
            self.docs_file = self.data_dir / "activity11" / "documents.txt"
        else:
            self.dict_file = self.data_dir / "activity12" / "dictionary_no_stoplist.txt"
            self.posting_file = self.data_dir / "activity12" / "posting_no_stoplist.txt"
            self.docs_file = self.data_dir / "activity12" / "documents.txt"
        
        # Índice de hash: token -> line_number (solo esto en memoria)
        self.token_line_index = {}
        self._build_token_index()
        
        # Caché de documentos (solo nombres)
        self.doc_names = {}
        self._load_doc_names()
    
    def _build_token_index(self) -> None:
        """Construye índice hash: token -> número de línea (solo índice en memoria)"""
        if not self.dict_file.exists():
            print(f"[!] ERROR: No se encuentra {self.dict_file}")
            return
        
        print(f"Construyendo indice hash desde: {self.dict_file.name}")
        start_time = time.time()
        
        with open(self.dict_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line_num <= 2:  # Saltar encabezado
                    continue
                
                line = line.strip()
                if line and '\t' in line:
                    token = line.split('\t')[0]
                    self.token_line_index[token] = line_num
        
        elapsed = time.time() - start_time
        print(f"[OK] Indice construido: {len(self.token_line_index)} tokens ({elapsed:.4f} seg)")
    
    def _load_doc_names(self) -> None:
        """Carga solo nombres de documentos (ligero)"""
        if not self.docs_file.exists():
            return
        
        with open(self.docs_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line_num <= 2:
                    continue
                
                line = line.strip()
                if line and '\t' in line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        doc_id = int(parts[0])
                        doc_name = parts[1]
                        self.doc_names[doc_id] = doc_name
    
    def _read_line_from_dict(self, token: str) -> Dict:
        """
        Lee SOLO la línea del diccionario para el token (sin cargar todo)
        
        Returns:
            Dict con info del token o None si no existe
        """
        token = token.lower()
        
        # Buscar en índice hash
        if token not in self.token_line_index:
            return None
        
        line_num = self.token_line_index[token]
        
        # Leer solo esa línea del archivo
        with open(self.dict_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if i == line_num:
                    parts = line.strip().split('\t')
                    if len(parts) >= 4:
                        return {
                            'token': parts[0],
                            'total_freq': int(parts[1]),
                            'doc_count': int(parts[2]),
                            'idf': float(parts[3])
                        }
                    break
        
        return None
    
    def _read_posting_for_token(self, token: str) -> List[Dict]:
        """
        Lee SOLO el posting para el token específico (sin cargar todo)
        
        Returns:
            Lista de documentos con sus TF-IDF
        """
        token = token.lower()
        
        # Leer posting línea por línea hasta encontrar el token
        if not self.posting_file.exists():
            return []
        
        results = []
        reading_token = False
        
        with open(self.posting_file, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                
                # Encontrar inicio del token
                if line_stripped.startswith("TOKEN: "):
                    current_token = line_stripped.replace("TOKEN: ", "")
                    
                    if current_token == token:
                        reading_token = True
                    elif reading_token:
                        # Ya terminamos de leer este token
                        break
                
                # Leer documentos del token
                elif reading_token and line.startswith("    documentID:"):
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        try:
                            doc_id = int(parts[0].strip().replace("documentID:", ""))
                            doc_name = parts[1].strip()
                            freq = int(parts[2].strip().replace("freq:", ""))
                            tfidf = float(parts[3].strip().replace("peso:", ""))
                            
                            results.append({
                                'doc_id': doc_id,
                                'doc_name': doc_name,
                                'freq': freq,
                                'tfidf': tfidf
                            })
                        except ValueError:
                            continue
        
        return results
    
    def search_token(self, token: str) -> List[Dict]:
        """
        Busca un token (lectura optimizada desde disco)
        
        Args:
            token: Token a buscar
            
        Returns:
            Lista de documentos ordenada por TF-IDF (descendente)
        """
        # Verificar en índice hash (rápido)
        dict_info = self._read_line_from_dict(token)
        
        if not dict_info:
            return []
        
        # Leer posting solo para este token
        results = self._read_posting_for_token(token)
        
        # Ya vienen ordenados por TF-IDF desde el archivo
        return results
    
    def search_multiple_tokens(self, tokens: List[str]) -> List[Dict]:
        """
        Busca múltiples tokens y combina resultados
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de documentos ordenada por score acumulado (top resultados)
        """
        doc_scores = defaultdict(lambda: {'doc_name': '', 'total_tfidf': 0.0, 'token_count': 0})
        
        for token in tokens:
            results = self.search_token(token)
            
            for doc in results:
                doc_id = doc['doc_id']
                doc_name = doc['doc_name']
                tfidf = doc['tfidf']
                
                doc_scores[doc_id]['doc_id'] = doc_id
                doc_scores[doc_id]['doc_name'] = doc_name
                doc_scores[doc_id]['total_tfidf'] += tfidf
                doc_scores[doc_id]['token_count'] += 1
        
        # Convertir a lista y ordenar
        results_list = list(doc_scores.values())
        results_list.sort(key=lambda x: x['total_tfidf'], reverse=True)
        
        return results_list
    
    def format_top_results(self, results: List[Dict], top_n: int = 10) -> str:
        """
        Formatea TOP N resultados
        
        Args:
            results: Lista de documentos
            top_n: Número de documentos a mostrar
            
        Returns:
            String formateado
        """
        if not results:
            return "No se encontraron documentos."
        
        output = []
        output.append(f"Top {min(top_n, len(results))} documentos:\n")
        
        for i, doc in enumerate(results[:top_n], 1):
            doc_name = doc.get('doc_name', 'unknown')
            
            if 'total_tfidf' in doc:
                score = doc['total_tfidf']
                output.append(f"{i}. {doc_name} (score: {score:.4f})")
            else:
                tfidf = doc.get('tfidf', 0)
                output.append(f"{i}. {doc_name} (tfidf: {tfidf:.4f})")
        
        if len(results) > top_n:
            output.append(f"\n... y {len(results) - top_n} documentos mas")
        
        return "\n".join(output)


def main():
    """Función principal - CLI retrieve optimizado"""
    
    if len(sys.argv) < 2:
        print("\nUSO: retrieve_optimized <token> [token2] [token3] ...")
        print("     retrieve_optimized gato")
        print("     retrieve_optimized lawyer consumers")
        print("\nOpciones:")
        print("  --no-stoplist    Buscar en diccionario sin stop list")
        print("  --top <N>        Mostrar top N resultados (default: 10)")
        sys.exit(1)
    
    # Parsear argumentos
    tokens = []
    use_stop_list = True
    top_n = 10
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--no-stoplist":
            use_stop_list = False
        elif arg == "--top":
            if i + 1 < len(sys.argv):
                top_n = int(sys.argv[i + 1])
                i += 1
        else:
            tokens.append(arg)
        
        i += 1
    
    if not tokens:
        print("[!] ERROR: Debe proporcionar al menos un token")
        sys.exit(1)
    
    # Crear buscador optimizado
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data" / "output"
    
    print("\n" + "=" * 80)
    print("RETRIEVE OPTIMIZADO - BUSQUEDA SIN CARGAR EN MEMORIA")
    print("=" * 80)
    print(f"Tokens a buscar: {', '.join(tokens)}")
    print(f"Usar stop list: {'Si' if use_stop_list else 'No'}")
    print(f"Top resultados: {top_n}")
    print("=" * 80 + "\n")
    
    # Inicializar (solo carga índice hash)
    start_time = time.time()
    searcher = OptimizedDictionarySearcher(str(data_dir), use_stop_list=use_stop_list)
    init_time = time.time() - start_time
    
    print(f"\nTiempo de inicializacion (solo indice hash): {init_time:.4f} segundos\n")
    
    # Buscar tokens
    search_start = time.time()
    
    if len(tokens) == 1:
        results = searcher.search_token(tokens[0])
    else:
        results = searcher.search_multiple_tokens(tokens)
    
    search_time = time.time() - search_start
    
    # Mostrar resultados
    print(searcher.format_top_results(results, top_n=top_n))
    print(f"\nTiempo de busqueda (lectura desde disco): {search_time:.6f} segundos")
    print(f"Total de documentos encontrados: {len(results)}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
