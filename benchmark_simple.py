#!/usr/bin/env python3
"""
Script de Benchmark Simplificado para Tokenización
"""

import sys
import time
import random
from pathlib import Path
from typing import List, Dict

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.activities.actividad5_tokenize import process_html_file

def get_sample_files(input_dir: str, num_files: int) -> List[Path]:
    """Obtiene una muestra de archivos HTML"""
    html_files = list(Path(input_dir).glob('*.html'))
    if len(html_files) < num_files:
        return html_files
    return random.sample(html_files, num_files)

def benchmark_tokenization(input_dir: str, num_docs_list: List[int]) -> Dict[int, float]:
    """Ejecuta benchmark de tokenización"""
    results = {}
    
    print("=" * 60)
    print("BENCHMARK DE TOKENIZACION")
    print("=" * 60)
    
    for num_docs in num_docs_list:
        print(f"\nProcesando {num_docs} documentos...")
        
        sample_files = get_sample_files(input_dir, num_docs)
        
        start_time = time.time()
        
        total_tokens = 0
        for html_file in sample_files:
            try:
                frequencies = process_html_file(str(html_file), "temp_out")
                total_tokens += sum(frequencies.values())
            except:
                continue
        
        elapsed_time = time.time() - start_time
        results[num_docs] = elapsed_time
        
        print(f"  Tiempo: {elapsed_time:.4f} segundos")
        print(f"  Tokens: {total_tokens:,}")
    
    # Guardar resultados
    with open("benchmark_tokenize_results.txt", 'w') as f:
        f.write("RESULTADOS - TOKENIZACION\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'Num Docs':<15} {'Tiempo (seg)':<20}\n")
        f.write("-" * 60 + "\n")
        for num_docs in sorted(results.keys()):
            f.write(f"{num_docs:<15} {results[num_docs]:<20.4f}\n")
    
    print("\n[OK] Resultados guardados en benchmark_tokenize_results.txt")
    
    return results

def main():
    input_dir = "data/input/Files"
    # Usar menos documentos para testing rápido
    num_docs_to_test = [10, 20, 30, 50]
    
    if not Path(input_dir).exists():
        print(f"[!] Error: No se encuentra el directorio {input_dir}")
        return
    
    results = benchmark_tokenization(input_dir, num_docs_to_test)
    print("\n[OK] Benchmark completado exitosamente")

if __name__ == "__main__":
    main()
