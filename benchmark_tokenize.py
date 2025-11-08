#!/usr/bin/env python3
"""
Script de Benchmark para Tokenización
======================================

Mide el tiempo de tokenización con número variable de documentos.

Uso:
    python benchmark_tokenize.py
"""

import sys
import os
import time
import random
import shutil
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt

# Agregar el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.activities.actividad5_tokenize import process_html_file

def get_sample_files(input_dir: str, num_files: int) -> List[Path]:
    """Obtiene una muestra de archivos HTML"""
    html_files = list(Path(input_dir).glob('*.html'))
    if len(html_files) < num_files:
        print(f"[WARN] Solo hay {len(html_files)} archivos disponibles, usando todos.")
        return html_files
    return random.sample(html_files, num_files)

def benchmark_tokenization(input_dir: str, num_docs_list: List[int]) -> Dict[int, float]:
    """
    Ejecuta benchmark de tokenización con diferentes cantidades de documentos
    
    Args:
        input_dir: Directorio con archivos HTML
        num_docs_list: Lista de cantidades de documentos a probar
        
    Returns:
        Diccionario con num_docs -> tiempo (segundos)
    """
    results = {}
    
    print("=" * 60)
    print("BENCHMARK DE TOKENIZACIÓN")
    print("=" * 60)
    
    for num_docs in num_docs_list:
        print(f"\n[*] Procesando {num_docs} documentos...")
        
        # Obtener muestra de archivos
        sample_files = get_sample_files(input_dir, num_docs)
        
        # Medir tiempo
        start_time = time.time()
        
        total_tokens = 0
        temp_output = "temp_benchmark_output"
        os.makedirs(temp_output, exist_ok=True)
        
        for html_file in sample_files:
            try:
                # Procesar archivo (tokenizar y contar frecuencias)
                frequencies = process_html_file(str(html_file), temp_output)
                total_tokens += sum(frequencies.values())
                
            except Exception as e:
                print(f"  [WARN] Error en {html_file.name}: {e}")
                continue
        
        elapsed_time = time.time() - start_time
        results[num_docs] = elapsed_time
        
    # Limpiar archivos temporales
    shutil.rmtree(temp_output, ignore_errors=True)
        
    print(f"  [OK] Tiempo: {elapsed_time:.4f} segundos")
    print(f"  [OK] Tokens procesados: {total_tokens:,}")
    print(f"  [OK] Velocidad: {total_tokens/elapsed_time:.0f} tokens/seg")
    
    return results

def plot_results(results: Dict[int, float], output_file: str = "benchmark_tokenize.png"):
    """Genera gráfica de resultados"""
    
    num_docs = sorted(results.keys())
    times = [results[n] for n in num_docs]
    
    plt.figure(figsize=(10, 6))
    plt.plot(num_docs, times, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    
    plt.xlabel('Número de Documentos', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: Tiempo de Tokenización vs Número de Documentos', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Anotar valores
    for i, (n, t) in enumerate(zip(num_docs, times)):
        plt.annotate(f'{t:.3f}s', 
                    xy=(n, t), 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    ha='center',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n[OK] Gráfica guardada en: {output_file}")
    
    return output_file

def save_results_table(results: Dict[int, float], output_file: str = "benchmark_tokenize_results.txt"):
    """Guarda tabla de resultados"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DE BENCHMARK - TOKENIZACIÓN\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"{'Num Docs':<15} {'Tiempo (seg)':<20} {'Tokens/seg':<15}\n")
        f.write("-" * 60 + "\n")
        
        for num_docs in sorted(results.keys()):
            time_sec = results[num_docs]
            # Estimar tokens (promedio 1695 por doc)
            estimated_tokens = num_docs * 1695
            tokens_per_sec = estimated_tokens / time_sec if time_sec > 0 else 0
            
            f.write(f"{num_docs:<15} {time_sec:<20.4f} {tokens_per_sec:<15,.0f}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"[OK] Tabla de resultados guardada en: {output_file}")

def main():
    """Función principal"""
    
    # Configuración
    input_dir = "data/input/Files"
    # Para ejecución rápida durante desarrollo, probamos un subconjunto
    num_docs_to_test = [10, 20, 30, 50, 100]
    
    # Verificar que el directorio existe
    if not Path(input_dir).exists():
        print(f"[!] Error: No se encuentra el directorio {input_dir}")
        return
    
    # Ejecutar benchmark
    results = benchmark_tokenization(input_dir, num_docs_to_test)
    
    # Generar gráfica
    plot_results(results)
    
    # Guardar tabla de resultados
    save_results_table(results)
    
    print("\n" + "=" * 60)
    print("[OK] Benchmark completado exitosamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
