#!/usr/bin/env python3
"""
Actividad 12: Generar archivos SIN stop list (Fase 4: Query)
============================================================

Este módulo crea una segunda versión de diccionario, posting y documentos
SIN aplicar el filtro de stop list para obtener más resultados en búsquedas.

Autor: JOSE GPE RICO MORENO
Fecha: Noviembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict, Counter

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA

class NoStopListIndexer:
    """Crea índice de documentos SIN filtro de stop list"""
    
    def __init__(self, html_dir: str, output_dir: str):
        """
        Inicializa el indexador sin stop list
        
        Args:
            html_dir: Directorio con archivos HTML
            output_dir: Directorio de salida
        """
        self.html_dir = Path(html_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Estructuras de datos (SIN filtro de stop list)
        self.document_index = {}  # doc_id -> {name, path}
        self.doc_name_to_id = {}  # doc_name -> doc_id
        self.token_doc_freq = defaultdict(lambda: defaultdict(int))  # token -> {doc_id: freq}
        self.document_tokens = {}  # doc_id -> {token: freq}
        self.total_documents = 0
        
        # TF-IDF
        self.idf_scores = {}
        self.tfidf_scores = {}
    
    def clean_html_content(self, html_content: str) -> str:
        """Limpia contenido HTML y extrae texto"""
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def extract_tokens(self, text: str) -> List[str]:
        """Extrae TODOS los tokens alfabéticos (sin filtro)"""
        tokens = re.findall(r'[a-zA-Z]+', text)
        # Solo filtro por longitud mínima (>=2)
        return [token.lower() for token in tokens if len(token) >= 2]
    
    def _read_html_file(self, file_path: Path) -> str:
        """Lee archivo HTML con manejo robusto de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def create_document_index(self) -> None:
        """Crea el índice de documentos SIN stop list"""
        html_files = sorted([f for f in self.html_dir.glob('*.html')])
        self.total_documents = len(html_files)
        
        print(f"\nProcesando {self.total_documents} documentos (SIN stop list)...")
        print("=" * 60)
        
        for doc_id, html_file in enumerate(html_files, 1):
            try:
                # Leer archivo HTML
                content = self._read_html_file(html_file)
                
                # Limpiar y extraer TODOS los tokens
                clean_text = self.clean_html_content(content)
                tokens = self.extract_tokens(clean_text)  # SIN filtro de stop list
                
                # Contar frecuencias
                token_counts = Counter(tokens)
                
                # Almacenar en índice
                doc_name = html_file.name
                doc_path = str(html_file.relative_to(PROJECT_ROOT))
                
                self.document_index[doc_id] = {
                    'name': doc_name,
                    'path': doc_path
                }
                self.doc_name_to_id[doc_name] = doc_id
                self.document_tokens[doc_id] = dict(token_counts)
                
                # Actualizar posting
                for token, freq in token_counts.items():
                    self.token_doc_freq[token][doc_id] = freq
                
                if doc_id % 50 == 0:
                    print(f"  Procesado: {doc_id}/{self.total_documents} documentos")
                    
            except Exception as e:
                print(f"[!] Error procesando {html_file.name}: {e}")
                continue
        
        print(f"[OK] Procesamiento completado")
        print(f"     Documentos: {len(self.document_index)}")
        print(f"     Tokens unicos (SIN stop list): {len(self.token_doc_freq)}")
    
    def calculate_tfidf(self) -> None:
        """Calcula TF-IDF para todos los tokens"""
        print("\nCalculando TF-IDF...")
        
        # Calcular IDF
        for token, doc_freqs in self.token_doc_freq.items():
            df = len(doc_freqs)
            idf = math.log10(self.total_documents / df)
            self.idf_scores[token] = idf
        
        # Calcular TF-IDF
        for doc_id, token_freqs in self.document_tokens.items():
            self.tfidf_scores[doc_id] = {}
            max_freq = max(token_freqs.values()) if token_freqs else 1
            
            for token, freq in token_freqs.items():
                tf = 0.5 + (0.5 * freq / max_freq)
                idf = self.idf_scores.get(token, 0)
                tfidf = tf * idf
                self.tfidf_scores[doc_id][token] = tfidf
        
        print(f"[OK] TF-IDF calculado")
    
    def save_documents(self) -> Path:
        """Guarda índice de documentos (igual que con stop list)"""
        doc_file = self.output_dir / "documents.txt"
        
        print("\nGenerando archivo de documentos...")
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write("documentID\tdocument_name\tpath\n")
            f.write("-" * 80 + "\n")
            
            for doc_id in sorted(self.document_index.keys()):
                doc_info = self.document_index[doc_id]
                f.write(f"{doc_id}\t{doc_info['name']}\t{doc_info['path']}\n")
        
        print(f"[OK] Archivo generado: {doc_file}")
        return doc_file
    
    def save_dictionary(self) -> Path:
        """Guarda diccionario SIN stop list"""
        dict_file = self.output_dir / "dictionary_no_stoplist.txt"
        
        print("\nGenerando diccionario SIN stop list...")
        
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("Token\tRepeticiones\t#Documentos\tIDF\n")
            f.write("-" * 80 + "\n")
            
            for token in sorted(self.token_doc_freq.keys()):
                doc_freqs = self.token_doc_freq[token]
                total_freq = sum(doc_freqs.values())
                doc_count = len(doc_freqs)
                idf = self.idf_scores.get(token, 0)
                
                f.write(f"{token}\t{total_freq}\t{doc_count}\t{idf:.6f}\n")
        
        print(f"[OK] Diccionario generado: {dict_file}")
        print(f"     Total de tokens: {len(self.token_doc_freq)}")
        return dict_file
    
    def save_posting(self) -> Path:
        """Guarda posting SIN stop list"""
        posting_file = self.output_dir / "posting_no_stoplist.txt"
        
        print("\nGenerando posting SIN stop list...")
        
        with open(posting_file, 'w', encoding='utf-8') as f:
            f.write("ARCHIVO POSTING - SIN STOP LIST\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total de tokens unicos: {len(self.token_doc_freq)}\n")
            f.write(f"Total de documentos: {self.total_documents}\n")
            f.write("=" * 80 + "\n\n")
            
            for token in sorted(self.token_doc_freq.keys()):
                doc_freqs = self.token_doc_freq[token]
                
                f.write(f"TOKEN: {token}\n")
                f.write(f"  IDF: {self.idf_scores[token]:.6f}\n")
                f.write(f"  Documentos ({len(doc_freqs)}):\n")
                
                # Ordenar por TF-IDF
                doc_tfidf_list = []
                for doc_id, freq in doc_freqs.items():
                    tfidf = self.tfidf_scores[doc_id].get(token, 0)
                    doc_name = self.document_index[doc_id]['name']
                    doc_tfidf_list.append((doc_id, doc_name, freq, tfidf))
                
                doc_tfidf_list.sort(key=lambda x: x[3], reverse=True)
                
                for doc_id, doc_name, freq, tfidf in doc_tfidf_list:
                    f.write(f"    documentID:{doc_id} | {doc_name} | freq:{freq} | peso:{tfidf:.6f}\n")
                f.write("\n")
        
        print(f"[OK] Posting generado: {posting_file}")
        return posting_file


def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("ACTIVIDAD 12: GENERAR ARCHIVOS SIN STOP LIST")
    print("=" * 80)
    
    # Directorios
    html_dir = PROJECT_ROOT / "data" / "input" / "Files"
    output_dir = PROJECT_ROOT / "data" / "output" / "activity12"
    
    if not html_dir.exists():
        print(f"[!] ERROR: No se encuentra el directorio: {html_dir}")
        return
    
    # Crear indexador
    start_time = time.time()
    indexer = NoStopListIndexer(str(html_dir), str(output_dir))
    
    # Procesar documentos
    indexer.create_document_index()
    indexer.calculate_tfidf()
    
    # Guardar archivos
    indexer.save_documents()
    indexer.save_dictionary()
    indexer.save_posting()
    
    total_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print(f"Archivos generados en: {output_dir}")
    print(f"  - documents.txt")
    print(f"  - dictionary_no_stoplist.txt")
    print(f"  - posting_no_stoplist.txt")
    print(f"\nTiempo total: {total_time:.3f} segundos")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
