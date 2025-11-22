#!/usr/bin/env python3
"""
Actividad 11: Índice de documentos (Fase 4: Query)
===================================================

Este módulo implementa:
1. Archivo de documentos con ID único (documents.txt)
2. Modificación del posting file para incluir documentID y peso TF-IDF
3. Medición de tiempos de procesamiento

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

class DocumentIndexer:
    """Crea índice de documentos con IDs únicos"""
    
    def __init__(self, html_dir: str, output_dir: str):
        """
        Inicializa el indexador de documentos
        
        Args:
            html_dir: Directorio con archivos HTML
            output_dir: Directorio de salida
        """
        self.html_dir = Path(html_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Estructuras de datos
        self.document_index = {}  # doc_id (int) -> {name, path}
        self.doc_name_to_id = {}  # doc_name (str) -> doc_id (int)
        self.token_doc_freq = defaultdict(lambda: defaultdict(int))  # token -> {doc_id: freq}
        self.document_tokens = {}  # doc_id -> {token: freq}
        self.total_documents = 0
        self.filtered_tokens = set()
        
        # TF-IDF
        self.idf_scores = {}  # token -> idf
        self.tfidf_scores = {}  # doc_id -> {token: tfidf}
        
        # Tiempos de procesamiento
        self.processing_times = []  # [(filename, time)]
        
    def load_filtered_dictionary(self, dict_file: str) -> Set[str]:
        """
        Carga tokens del diccionario filtrado (con stop list aplicada)
        
        Args:
            dict_file: Archivo de diccionario filtrado
            
        Returns:
            Set de tokens filtrados
        """
        dict_path = Path(dict_file)
        
        if not dict_path.exists():
            print(f"[!] No se encontro el archivo: {dict_file}")
            return set()
        
        print(f"Cargando diccionario filtrado desde: {dict_file}")
        
        filtered_tokens = set()
        with open(dict_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar encabezado
        for line in lines[2:]:
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 1:
                    token = parts[0]
                    filtered_tokens.add(token)
        
        self.filtered_tokens = filtered_tokens
        print(f"[OK] Cargados {len(filtered_tokens)} tokens filtrados")
        return filtered_tokens
    
    def clean_html_content(self, html_content: str) -> str:
        """Limpia contenido HTML y extrae texto"""
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def extract_tokens(self, text: str) -> List[str]:
        """Extrae tokens alfabéticos del texto"""
        tokens = re.findall(r'[a-zA-Z]+', text)
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
        
        # Si falla todo, usar errors='ignore'
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def create_document_index(self) -> Path:
        """
        Crea el índice de documentos con IDs únicos
        Procesa todos los archivos HTML y genera:
        1. Índice de documentos (documentID | nombre | path)
        2. Frecuencias de tokens por documento
        """
        html_files = sorted([f for f in self.html_dir.glob('*.html')])
        self.total_documents = len(html_files)
        
        print(f"\nProcesando {self.total_documents} documentos...")
        print("=" * 60)
        
        for doc_id, html_file in enumerate(html_files, 1):
            start_time = time.time()
            
            try:
                # Leer archivo HTML
                content = self._read_html_file(html_file)
                
                # Limpiar y extraer tokens
                clean_text = self.clean_html_content(content)
                tokens = self.extract_tokens(clean_text)
                
                # Filtrar solo tokens del diccionario filtrado
                filtered_tokens = [token for token in tokens if token in self.filtered_tokens]
                
                # Contar frecuencias
                token_counts = Counter(filtered_tokens)
                
                # Almacenar en índice de documentos
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
                
                # Medir tiempo
                elapsed = time.time() - start_time
                self.processing_times.append((doc_name, elapsed))
                
                if doc_id % 50 == 0:
                    print(f"  Procesado: {doc_id}/{self.total_documents} documentos")
                    
            except Exception as e:
                print(f"[!] Error procesando {html_file.name}: {e}")
                continue
        
        print(f"[OK] Procesamiento completado: {len(self.document_index)} documentos indexados")
        return self.save_document_index()
    
    def calculate_tfidf(self) -> None:
        """Calcula TF-IDF para todos los tokens en todos los documentos"""
        print("\nCalculando TF-IDF...")
        
        # Calcular IDF para cada token
        for token, doc_freqs in self.token_doc_freq.items():
            df = len(doc_freqs)  # Document Frequency
            idf = math.log10(self.total_documents / df)
            self.idf_scores[token] = idf
        
        # Calcular TF-IDF para cada documento
        for doc_id, token_freqs in self.document_tokens.items():
            self.tfidf_scores[doc_id] = {}
            
            # Encontrar frecuencia máxima en el documento
            max_freq = max(token_freqs.values()) if token_freqs else 1
            
            for token, freq in token_freqs.items():
                # TF normalizado
                tf = 0.5 + (0.5 * freq / max_freq)
                
                # IDF
                idf = self.idf_scores.get(token, 0)
                
                # TF-IDF
                tfidf = tf * idf
                self.tfidf_scores[doc_id][token] = tfidf
        
        print(f"[OK] TF-IDF calculado para {len(self.tfidf_scores)} documentos")
    
    def save_document_index(self) -> Path:
        """Guarda el índice de documentos"""
        doc_file = self.output_dir / "documents.txt"
        
        print("\nGenerando archivo de documentos...")
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("documentID\tdocument_name\tpath\n")
            f.write("-" * 80 + "\n")
            
            # Datos ordenados por ID
            for doc_id in sorted(self.document_index.keys()):
                doc_info = self.document_index[doc_id]
                f.write(f"{doc_id}\t{doc_info['name']}\t{doc_info['path']}\n")
        
        print(f"[OK] Archivo de documentos generado: {doc_file}")
        print(f"     Total de documentos: {len(self.document_index)}")
        return doc_file
    
    def save_dictionary_with_ids(self) -> Path:
        """Guarda diccionario con IDs de documentos"""
        dict_file = self.output_dir / "dictionary.txt"
        
        print("\nGenerando diccionario con documentIDs...")
        
        with open(dict_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("Token\tRepeticiones\t#Documentos\tIDF\n")
            f.write("-" * 80 + "\n")
            
            # Datos ordenados alfabéticamente
            for token in sorted(self.token_doc_freq.keys()):
                doc_freqs = self.token_doc_freq[token]
                total_freq = sum(doc_freqs.values())
                doc_count = len(doc_freqs)
                idf = self.idf_scores.get(token, 0)
                
                f.write(f"{token}\t{total_freq}\t{doc_count}\t{idf:.6f}\n")
        
        print(f"[OK] Diccionario generado: {dict_file}")
        print(f"     Total de tokens: {len(self.token_doc_freq)}")
        return dict_file
    
    def save_posting_with_weights(self) -> Path:
        """Guarda posting con documentID y pesos TF-IDF"""
        posting_file = self.output_dir / "posting.txt"
        
        print("\nGenerando posting con documentID y pesos...")
        
        with open(posting_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("ARCHIVO POSTING - DOCUMENTOS CON PESOS TF-IDF\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total de tokens unicos: {len(self.token_doc_freq)}\n")
            f.write(f"Total de documentos: {self.total_documents}\n")
            f.write("=" * 80 + "\n\n")
            
            # Posting para cada token
            for token in sorted(self.token_doc_freq.keys()):
                doc_freqs = self.token_doc_freq[token]
                
                f.write(f"TOKEN: {token}\n")
                f.write(f"  IDF: {self.idf_scores[token]:.6f}\n")
                f.write(f"  Documentos ({len(doc_freqs)}):\n")
                
                # Ordenar por TF-IDF descendente
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
    
    def save_time_log(self) -> Path:
        """Guarda archivo log con tiempos de procesamiento"""
        log_file = self.output_dir / f"a11_{MATRICULA}.txt"
        
        print("\nGenerando archivo log de tiempos...")
        
        total_time = sum(t for _, t in self.processing_times)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("ACTIVIDAD 11 - LOG DE TIEMPOS DE PROCESAMIENTO\n")
            f.write("=" * 80 + "\n")
            f.write(f"Matricula: {MATRICULA}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de archivos procesados: {len(self.processing_times)}\n")
            f.write(f"Tiempo total: {total_time:.6f} segundos\n")
            f.write(f"Tiempo promedio por archivo: {total_time/len(self.processing_times):.6f} segundos\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("TIEMPOS POR ARCHIVO:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Archivo':<30} {'Tiempo (s)':>15}\n")
            f.write("-" * 80 + "\n")
            
            for filename, elapsed in self.processing_times:
                f.write(f"{filename:<30} {elapsed:>15.6f}\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"{'TOTAL':<30} {total_time:>15.6f}\n")
        
        print(f"[OK] Log de tiempos generado: {log_file}")
        print(f"     Tiempo total de procesamiento: {total_time:.3f} segundos")
        print(f"     Tiempo promedio por archivo: {total_time/len(self.processing_times):.6f} segundos")
        return log_file


def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("ACTIVIDAD 11: INDICE DE DOCUMENTOS (FASE 4 - QUERY)")
    print("=" * 80)
    
    # Directorios
    html_dir = PROJECT_ROOT / "data" / "input" / "Files"
    dict_file = PROJECT_ROOT / "data" / "output" / "activity9" / "dictionary_filtered.txt"
    output_dir = PROJECT_ROOT / "data" / "output" / "activity11"
    
    # Verificar que existan los archivos necesarios
    if not html_dir.exists():
        print(f"[!] ERROR: No se encuentra el directorio: {html_dir}")
        return
    
    if not dict_file.exists():
        print(f"[!] ERROR: No se encuentra el diccionario filtrado: {dict_file}")
        return
    
    # Crear indexador
    indexer = DocumentIndexer(str(html_dir), str(output_dir))
    
    # Cargar diccionario filtrado
    indexer.load_filtered_dictionary(str(dict_file))
    
    # Crear índice de documentos
    start_total = time.time()
    indexer.create_document_index()
    
    # Calcular TF-IDF
    indexer.calculate_tfidf()
    
    # Guardar archivos
    indexer.save_dictionary_with_ids()
    indexer.save_posting_with_weights()
    indexer.save_time_log()
    
    total_elapsed = time.time() - start_total
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print(f"Archivos generados en: {output_dir}")
    print(f"  - documents.txt (indice de documentos)")
    print(f"  - dictionary.txt (diccionario con IDs)")
    print(f"  - posting.txt (posting con pesos TF-IDF)")
    print(f"  - a11_{MATRICULA}.txt (log de tiempos)")
    print(f"\nTiempo total de ejecucion: {total_elapsed:.3f} segundos")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
