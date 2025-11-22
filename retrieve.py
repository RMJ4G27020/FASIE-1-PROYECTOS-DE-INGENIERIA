#!/usr/bin/env python3
"""
Actividad 12: Buscar en el diccionario (Fase 4: Query)
======================================================

Programa retrieve para buscar tokens en el diccionario.
Uso: retrieve <token>
     retrieve <token1> <token2> ...

Retorna lista de documentos que contienen el token(s).

Autor: JOSE GPE RICO MORENO
Fecha: Noviembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA


class DictionarySearcher:
    """Busca tokens en el diccionario y retorna documentos relevantes"""
    
    def __init__(self, data_dir: str, use_stop_list: bool = True):
        """
        Inicializa el buscador
        
        Args:
            data_dir: Directorio con archivos de diccionario/posting/documentos
            use_stop_list: Si True, usa archivos con stop list. Si False, sin stop list.
        """
        self.data_dir = Path(data_dir)
        self.use_stop_list = use_stop_list
        
        # Archivos a cargar
        if use_stop_list:
            # Con stop list (activity11)
            self.dict_file = self.data_dir / "activity11" / "dictionary.txt"
            self.posting_file = self.data_dir / "activity11" / "posting.txt"
            self.docs_file = self.data_dir / "activity11" / "documents.txt"
        else:
            # Sin stop list (activity12)
            self.dict_file = self.data_dir / "activity12" / "dictionary_no_stoplist.txt"
            self.posting_file = self.data_dir / "activity12" / "posting_no_stoplist.txt"
            self.docs_file = self.data_dir / "activity12" / "documents.txt"
        
        # Estructuras de datos en memoria
        self.dictionary = {}  # token -> {total_freq, doc_count, idf, line_num}
        self.posting = {}  # token -> [(doc_id, doc_name, freq, tfidf)]
        self.documents = {}  # doc_id -> {name, path}
        
        # Cargar archivos
        self._load_documents()
        self._load_dictionary()
        self._load_posting()
    
    def _load_documents(self) -> None:
        """Carga el índice de documentos"""
        if not self.docs_file.exists():
            print(f"[!] ERROR: No se encuentra {self.docs_file}")
            return
        
        print(f"Cargando documentos desde: {self.docs_file.name}")
        
        with open(self.docs_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar encabezado
        for line in lines[2:]:
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    doc_id = int(parts[0])
                    doc_name = parts[1]
                    doc_path = parts[2]
                    self.documents[doc_id] = {'name': doc_name, 'path': doc_path}
        
        print(f"[OK] Cargados {len(self.documents)} documentos")
    
    def _load_dictionary(self) -> None:
        """Carga el diccionario en memoria"""
        if not self.dict_file.exists():
            print(f"[!] ERROR: No se encuentra {self.dict_file}")
            return
        
        print(f"Cargando diccionario desde: {self.dict_file.name}")
        
        with open(self.dict_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar encabezado
        for i, line in enumerate(lines[2:], start=2):
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 4:
                    token = parts[0]
                    total_freq = int(parts[1])
                    doc_count = int(parts[2])
                    idf = float(parts[3])
                    self.dictionary[token] = {
                        'total_freq': total_freq,
                        'doc_count': doc_count,
                        'idf': idf,
                        'line_num': i
                    }
        
        print(f"[OK] Cargados {len(self.dictionary)} tokens")
    
    def _load_posting(self) -> None:
        """Carga el posting file en memoria"""
        if not self.posting_file.exists():
            print(f"[!] ERROR: No se encuentra {self.posting_file}")
            return
        
        print(f"Cargando posting desde: {self.posting_file.name}")
        
        with open(self.posting_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_token = None
        for line in lines:
            line_stripped = line.strip()
            
            if line_stripped.startswith("TOKEN: "):
                current_token = line_stripped.replace("TOKEN: ", "")
                self.posting[current_token] = []
            elif line.startswith("    documentID:") and current_token:
                # Parsear línea de documento
                # Formato: "    documentID:X | nombre | freq:Y | peso:Z"
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    doc_id_str = parts[0].strip().replace("documentID:", "")
                    doc_name = parts[1].strip()
                    freq_str = parts[2].strip().replace("freq:", "")
                    peso_str = parts[3].strip().replace("peso:", "")
                    
                    try:
                        doc_id = int(doc_id_str)
                        freq = int(freq_str)
                        tfidf = float(peso_str)
                        
                        self.posting[current_token].append({
                            'doc_id': doc_id,
                            'doc_name': doc_name,
                            'freq': freq,
                            'tfidf': tfidf
                        })
                    except ValueError:
                        continue
        
        print(f"[OK] Cargado posting para {len(self.posting)} tokens")
    
    def search_token(self, token: str) -> List[Dict]:
        """
        Busca un token en el diccionario
        
        Args:
            token: Token a buscar (se convierte a minúsculas)
            
        Returns:
            Lista de documentos que contienen el token con info de relevancia
        """
        # Normalizar token
        token = token.lower()
        
        # Verificar si existe en diccionario
        if token not in self.dictionary:
            return []
        
        # Obtener posting list
        if token not in self.posting:
            return []
        
        return self.posting[token]
    
    def search_multiple_tokens(self, tokens: List[str]) -> List[Dict]:
        """
        Busca múltiples tokens y combina resultados
        
        Args:
            tokens: Lista de tokens a buscar
            
        Returns:
            Lista de documentos con scores acumulados
        """
        # Diccionario para acumular scores
        doc_scores = {}  # doc_id -> {doc_name, total_tfidf, token_count}
        
        for token in tokens:
            results = self.search_token(token)
            
            for doc in results:
                doc_id = doc['doc_id']
                doc_name = doc['doc_name']
                tfidf = doc['tfidf']
                
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = {
                        'doc_id': doc_id,
                        'doc_name': doc_name,
                        'total_tfidf': 0.0,
                        'token_count': 0
                    }
                
                doc_scores[doc_id]['total_tfidf'] += tfidf
                doc_scores[doc_id]['token_count'] += 1
        
        # Convertir a lista y ordenar por score descendente
        results = list(doc_scores.values())
        results.sort(key=lambda x: x['total_tfidf'], reverse=True)
        
        return results
    
    def format_results(self, results: List[Dict], show_all: bool = True) -> str:
        """
        Formatea resultados para impresión
        
        Args:
            results: Lista de documentos encontrados
            show_all: Si True, muestra todos. Si False, solo top 10.
            
        Returns:
            String formateado con resultados
        """
        if not results:
            return "No se encontraron documentos."
        
        output = []
        
        if not show_all:
            results = results[:10]  # Top 10
            output.append("Top 10 documentos:\n")
        else:
            output.append(f"Total de documentos encontrados: {len(results)}\n")
        
        for i, doc in enumerate(results, 1):
            doc_name = doc.get('doc_name', 'unknown')
            if 'total_tfidf' in doc:
                score = doc['total_tfidf']
                output.append(f"{i}. {doc_name} (score: {score:.4f})")
            else:
                output.append(f"{i}. {doc_name}")
        
        return "\n".join(output)


def main():
    """Función principal - CLI retrieve"""
    
    if len(sys.argv) < 2:
        print("\nUSO: retrieve <token> [token2] [token3] ...")
        print("     retrieve gato")
        print("     retrieve lawyer consumers")
        print("\nOpciones:")
        print("  --no-stoplist    Buscar en diccionario sin stop list")
        print("  --top10          Mostrar solo top 10 resultados")
        sys.exit(1)
    
    # Parsear argumentos
    tokens = []
    use_stop_list = True
    show_all = True
    
    for arg in sys.argv[1:]:
        if arg == "--no-stoplist":
            use_stop_list = False
        elif arg == "--top10":
            show_all = False
        else:
            tokens.append(arg)
    
    if not tokens:
        print("[!] ERROR: Debe proporcionar al menos un token para buscar")
        sys.exit(1)
    
    # Crear buscador
    # Usar el directorio actual del script
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data" / "output"
    
    print("\n" + "=" * 80)
    print("RETRIEVE - BUSQUEDA EN DICCIONARIO")
    print("=" * 80)
    print(f"Tokens a buscar: {', '.join(tokens)}")
    print(f"Usar stop list: {'Si' if use_stop_list else 'No'}")
    print("=" * 80 + "\n")
    
    # Inicializar buscador
    start_time = time.time()
    searcher = DictionarySearcher(str(data_dir), use_stop_list=use_stop_list)
    load_time = time.time() - start_time
    
    print(f"\nTiempo de carga: {load_time:.4f} segundos\n")
    
    # Buscar tokens
    search_start = time.time()
    
    if len(tokens) == 1:
        results = searcher.search_token(tokens[0])
    else:
        results = searcher.search_multiple_tokens(tokens)
    
    search_time = time.time() - search_start
    
    # Mostrar resultados
    print(searcher.format_results(results, show_all=show_all))
    print(f"\nTiempo de busqueda: {search_time:.6f} segundos")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
