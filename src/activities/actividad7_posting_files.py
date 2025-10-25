#!/usr/bin/env python3
"""
Actividad 7: Archivo Posting (Fase 3: Weight Tokens)
====================================================

Este módulo implementa la creación de archivos posting que muestran:
1. Diccionario con 3 columnas: Token, Repeticiones, #Documentos
2. Archivo posting con lista de documentos donde aparece cada token
3. Frecuencias por documento para cada token

Autor: JOSE GPE RICO MORENO
Fecha: Septiembre 2025
Proyecto: FASIE-3-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA

class PostingFileGenerator:
    """Genera archivos posting para análisis de documentos"""
    
    def __init__(self, html_dir: str, output_dir: str):
        """
        Inicializa el generador de archivos posting
        
        Args:
            html_dir: Directorio con archivos HTML
            output_dir: Directorio de salida
        """
        self.html_dir = Path(html_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Estructuras de datos para el posting
        self.token_doc_freq = defaultdict(Counter)  # token -> {doc_id: freq}
        self.token_total_freq = Counter()           # token -> freq_total
        self.total_documents = 0
        
    def clean_html_content(self, html_content: str) -> str:
        """Limpia contenido HTML y extrae texto"""
        # Remover etiquetas HTML
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # Remover caracteres especiales y normalizar espacios
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def extract_tokens(self, text: str) -> List[str]:
        """Extrae tokens alfabéticos del texto"""
        tokens = re.findall(r'[a-zA-Z]+', text)
        return [token.lower() for token in tokens if len(token) >= 2]
    
    def process_html_files(self) -> None:
        """Procesa todos los archivos HTML y genera posting data"""
        html_files = sorted([f for f in self.html_dir.glob('*.html')])
        self.total_documents = len(html_files)
        
        print(f"Procesando {self.total_documents} archivos HTML...")
        
        for i, html_file in enumerate(html_files, 1):
            if i % 50 == 0:
                print(f"  Procesado: {i}/{self.total_documents} archivos")
                
            try:
                # Leer archivo HTML con múltiples encodings
                content = self._read_html_file(html_file)
                
                # Limpiar y extraer tokens
                clean_text = self.clean_html_content(content)
                tokens = self.extract_tokens(clean_text)
                
                # Contar frecuencias por documento
                doc_token_count = Counter(tokens)
                doc_id = html_file.stem  # nombre sin extensión
                
                # Actualizar estructuras de datos
                for token, freq in doc_token_count.items():
                    self.token_doc_freq[token][doc_id] = freq
                    self.token_total_freq[token] += freq
                    
            except Exception as e:
                print(f"Error procesando {html_file.name}: {e}")
                continue
        
        print(f"✓ Procesamiento completado: {len(self.token_total_freq)} tokens únicos")
    
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
    
    def generate_dictionary_file(self) -> Path:
        """Genera archivo de diccionario con 3 columnas"""
        dict_file = self.output_dir / "dictionary_posting.txt"
        
        print("Generando archivo de diccionario...")
        
        with open(dict_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("Token\tRepeticiones\t#Documentos\n")
            f.write("-" * 50 + "\n")
            
            # Datos ordenados alfabéticamente
            for token in sorted(self.token_total_freq.keys()):
                total_freq = self.token_total_freq[token]
                doc_count = len(self.token_doc_freq[token])
                f.write(f"{token}\t{total_freq}\t{doc_count}\n")
        
        print(f"✓ Diccionario generado: {dict_file}")
        return dict_file
    
    def generate_posting_file(self) -> Path:
        """Genera archivo posting con documentos por token"""
        posting_file = self.output_dir / "posting_list.txt"
        
        print("Generando archivo posting...")
        
        with open(posting_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("ARCHIVO POSTING - DOCUMENTOS POR TOKEN\n")
            f.write("=" * 60 + "\n")
            f.write(f"Total de tokens únicos: {len(self.token_total_freq)}\n")
            f.write(f"Total de documentos: {self.total_documents}\n")
            f.write("=" * 60 + "\n\n")
            
            # Posting list para cada token
            for token in sorted(self.token_total_freq.keys()):
                doc_freqs = self.token_doc_freq[token]
                total_freq = self.token_total_freq[token]
                doc_count = len(doc_freqs)
                
                f.write(f"TOKEN: {token}\n")
                f.write(f"  Frecuencia total: {total_freq}\n")
                f.write(f"  Aparece en {doc_count} documentos:\n")
                
                # Lista de documentos ordenada por frecuencia descendente
                sorted_docs = sorted(doc_freqs.items(), key=lambda x: x[1], reverse=True)
                for doc_id, freq in sorted_docs:
                    f.write(f"    {doc_id}: {freq} veces\n")
                f.write("\n")
        
        print(f"✓ Archivo posting generado: {posting_file}")
        return posting_file
    
    def generate_summary_stats(self) -> Path:
        """Genera estadísticas resumidas del posting"""
        stats_file = self.output_dir / "posting_stats.txt"
        
        print("Generando estadísticas de posting...")
        
        # Calcular estadísticas
        total_tokens = len(self.token_total_freq)
        total_occurrences = sum(self.token_total_freq.values())
        
        # Token más frecuente
        most_frequent = self.token_total_freq.most_common(1)[0]
        
        # Token en más documentos
        doc_counts = {token: len(docs) for token, docs in self.token_doc_freq.items()}
        most_widespread = max(doc_counts.items(), key=lambda x: x[1])
        
        # Distribución de frecuencias
        freq_distribution = Counter(self.token_total_freq.values())
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS DEL ARCHIVO POSTING\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total de tokens únicos: {total_tokens:,}\n")
            f.write(f"Total de ocurrencias: {total_occurrences:,}\n")
            f.write(f"Total de documentos: {self.total_documents}\n")
            f.write(f"Promedio de tokens por documento: {total_occurrences/self.total_documents:.1f}\n")
            f.write("\n")
            
            f.write("TOKEN MÁS FRECUENTE:\n")
            f.write(f"  '{most_frequent[0]}': {most_frequent[1]:,} ocurrencias\n")
            f.write(f"  Aparece en {len(self.token_doc_freq[most_frequent[0]])} documentos\n")
            f.write("\n")
            
            f.write("TOKEN MÁS DISTRIBUIDO:\n")
            f.write(f"  '{most_widespread[0]}': aparece en {most_widespread[1]} documentos\n")
            f.write(f"  Frecuencia total: {self.token_total_freq[most_widespread[0]]:,}\n")
            f.write("\n")
            
            f.write("TOP 10 TOKENS MÁS FRECUENTES:\n")
            for i, (token, freq) in enumerate(self.token_total_freq.most_common(10), 1):
                doc_count = len(self.token_doc_freq[token])
                f.write(f"  {i:2d}. {token}: {freq:,} veces ({doc_count} docs)\n")
            f.write("\n")
            
            f.write("DISTRIBUCIÓN DE FRECUENCIAS:\n")
            for freq in sorted(freq_distribution.keys(), reverse=True)[:10]:
                count = freq_distribution[freq]
                f.write(f"  {count:,} tokens aparecen {freq} veces\n")
        
        print(f"✓ Estadísticas generadas: {stats_file}")
        return stats_file
    
    def generate_report(self, processing_time: float) -> Path:
        """Genera reporte académico de la actividad"""
        report_file = self.output_dir / f"a7_{MATRICULA}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE ACADÉMICO - ACTIVIDAD 7: ARCHIVO POSTING\n")
            f.write("=" * 60 + "\n")
            f.write(f"Matrícula: {MATRICULA}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Actividad: Generación de Archivos Posting\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("RESULTADOS DEL PROCESAMIENTO:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Archivos HTML procesados: {self.total_documents}\n")
            f.write(f"Tokens únicos encontrados: {len(self.token_total_freq):,}\n")
            f.write(f"Total de ocurrencias: {sum(self.token_total_freq.values()):,}\n")
            f.write(f"Tiempo de procesamiento: {processing_time:.3f} segundos\n")
            f.write("\n")
            
            f.write("ARCHIVOS GENERADOS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. dictionary_posting.txt - Diccionario con 3 columnas\n")
            f.write("2. posting_list.txt - Lista de documentos por token\n")
            f.write("3. posting_stats.txt - Estadísticas resumidas\n")
            f.write("4. a7_matricula.txt - Este reporte\n")
            f.write("\n")
            
            f.write("TOKENS MÁS RELEVANTES:\n")
            f.write("-" * 40 + "\n")
            for i, (token, freq) in enumerate(self.token_total_freq.most_common(5), 1):
                doc_count = len(self.token_doc_freq[token])
                f.write(f"{i}. '{token}': {freq:,} veces en {doc_count} documentos\n")
        
        print(f"✓ Reporte académico generado: {report_file}")
        return report_file


def main():
    """Función principal de la Actividad 7"""
    start_time = time.time()
    
    print("=" * 60)
    print("ACTIVIDAD 7: ARCHIVO POSTING")
    print("Fase 3: Weight Tokens")
    print("=" * 60)
    
    # Configurar directorios
    if len(sys.argv) > 2:
        html_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        html_dir = "data/input/Files"
        output_dir = "data/output/activity7"
    
    try:
        # Crear generador de posting
        generator = PostingFileGenerator(html_dir, output_dir)
        
        # Procesar archivos HTML
        generator.process_html_files()
        
        # Generar archivos de salida
        dict_file = generator.generate_dictionary_file()
        posting_file = generator.generate_posting_file()
        stats_file = generator.generate_summary_stats()
        
        # Calcular tiempo total
        processing_time = time.time() - start_time
        
        # Generar reporte
        report_file = generator.generate_report(processing_time)
        
        print("\n" + "=" * 60)
        print("ACTIVIDAD 7 COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print(f"Tiempo total: {processing_time:.3f} segundos")
        print(f"Tokens procesados: {len(generator.token_total_freq):,}")
        print(f"Documentos analizados: {generator.total_documents}")
        print(f"Archivos generados en: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error en Actividad 7: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())