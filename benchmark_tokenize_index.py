#!/usr/bin/env python3
"""
Script de Benchmark para Tokenización + Indexación
===================================================

Mide el tiempo combinado de tokenización e indexación con número variable de documentos.

Uso:
    python benchmark_tokenize_index.py
"""

import sys
import os
import time
import random
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import matplotlib.pyplot as plt

# Agregar el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.activities.actividad5_tokenize import process_html_file
from src.activities.actividad7_posting_files import PostingFileGenerator

def get_sample_files(input_dir: str, num_files: int) -> List[Path]:
    """Obtiene una muestra de archivos HTML"""
    html_files = list(Path(input_dir).glob('*.html'))
    if len(html_files) < num_files:
        print(f"⚠️ Solo hay {len(html_files)} archivos disponibles, usando todos.")
        return html_files
    return random.sample(html_files, num_files)

def benchmark_tokenize_and_index(input_dir: str, num_docs_list: List[int]) -> Dict[int, Tuple[float, float, int]]:
    """
    Ejecuta benchmark de tokenización + indexación
    
    Args:
        input_dir: Directorio con archivos HTML
        num_docs_list: Lista de cantidades de documentos a probar
        
    Returns:
        Diccionario con num_docs -> (tiempo_tokenize, tiempo_index, num_tokens_unicos)
    """
    results = {}
    
    print("=" * 60)
    print("BENCHMARK DE TOKENIZACIÓN + INDEXACIÓN")
    print("=" * 60)
    
    for num_docs in num_docs_list:
        print(f"\n📊 Procesando {num_docs} documentos...")
        
        # Obtener muestra de archivos
        sample_files = get_sample_files(input_dir, num_docs)
        
        # Crear directorio temporal para esta prueba
        temp_input = Path("temp_bench_input")
        temp_output = Path("temp_bench_output")
        temp_input.mkdir(exist_ok=True)
        temp_output.mkdir(exist_ok=True)
        
        try:
            # Copiar archivos a directorio temporal
            for f in sample_files:
                shutil.copy(str(f), str(temp_input / f.name))
            
            # FASE 1: Tokenización
            start_tokenize = time.time()
            
            tokenize_out = temp_output / "tokenize"
            tokenize_out.mkdir(exist_ok=True)
            
            total_tokens = 0
            for html_file in temp_input.glob('*.html'):
                frequencies = process_html_file(str(html_file), str(tokenize_out))
                total_tokens += sum(frequencies.values())
            
            time_tokenize = time.time() - start_tokenize
            
            # FASE 2: Indexación (Posting List)
            start_index = time.time()
            
            posting_out = temp_output / "posting"
            posting_out.mkdir(exist_ok=True)
            
            generator = PostingFileGenerator(str(temp_input), str(posting_out))
            generator.process_html_files()
            
            time_index = time.time() - start_index
            
            # Obtener tokens únicos
            unique_tokens = len(generator.token_total_freq)
            
            # Guardar resultados
            results[num_docs] = (time_tokenize, time_index, unique_tokens)
            
            total_time = time_tokenize + time_index
            
            print(f"  ✓ Tiempo tokenización: {time_tokenize:.4f} seg")
            print(f"  ✓ Tiempo indexación: {time_index:.4f} seg")
            print(f"  ✓ Tiempo total: {total_time:.4f} seg")
            print(f"  ✓ Tokens únicos: {unique_tokens:,}")
            print(f"  ✓ Velocidad: {total_tokens/total_time:.0f} tokens/seg")
            
        finally:
            # Limpiar temporales
            shutil.rmtree(temp_input, ignore_errors=True)
            shutil.rmtree(temp_output, ignore_errors=True)
    
    return results

def plot_results(results: Dict[int, Tuple[float, float, int]], 
                output_file: str = "benchmark_tokenize_index.png"):
    """Genera gráfica de resultados"""
    
    num_docs = sorted(results.keys())
    times_tokenize = [results[n][0] for n in num_docs]
    times_index = [results[n][1] for n in num_docs]
    times_total = [results[n][0] + results[n][1] for n in num_docs]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfica 1: Comparación de tiempos
    x_pos = range(len(num_docs))
    width = 0.25
    
    ax1.bar([x - width for x in x_pos], times_tokenize, width, 
            label='Tokenización', color='#2E86AB', alpha=0.8)
    ax1.bar([x for x in x_pos], times_index, width, 
            label='Indexación', color='#A23B72', alpha=0.8)
    ax1.bar([x + width for x in x_pos], times_total, width, 
            label='Total', color='#F18F01', alpha=0.8)
    
    ax1.set_xlabel('Número de Documentos', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax1.set_title('Tiempo de Procesamiento por Fase', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(num_docs)
    ax1.legend()
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Gráfica 2: Tiempo total
    ax2.plot(num_docs, times_total, marker='o', linewidth=2, markersize=8, 
            color='#F18F01', label='Tiempo Total')
    ax2.fill_between(num_docs, times_total, alpha=0.3, color='#F18F01')
    
    ax2.set_xlabel('Número de Documentos', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tiempo Total (segundos)', fontsize=12, fontweight='bold')
    ax2.set_title('Tiempo Total: Tokenización + Indexación', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend()
    
    # Anotar valores en gráfica 2
    for i, (n, t) in enumerate(zip(num_docs, times_total)):
        ax2.annotate(f'{t:.3f}s', 
                    xy=(n, t), 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    ha='center',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada en: {output_file}")
    
    return output_file

def plot_unique_tokens(results: Dict[int, Tuple[float, float, int]], 
                      output_file: str = "benchmark_unique_tokens.png"):
    """Genera gráfica de tokens únicos vs documentos"""
    
    num_docs = sorted(results.keys())
    unique_tokens = [results[n][2] for n in num_docs]
    
    plt.figure(figsize=(10, 6))
    plt.plot(num_docs, unique_tokens, marker='s', linewidth=2, markersize=8, 
            color='#06A77D', label='Tokens Únicos')
    plt.fill_between(num_docs, unique_tokens, alpha=0.2, color='#06A77D')
    
    plt.xlabel('Número de Documentos', fontsize=12, fontweight='bold')
    plt.ylabel('Tokens Únicos', fontsize=12, fontweight='bold')
    plt.title('Crecimiento de Vocabulario: Tokens Únicos vs Documentos', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica de tokens únicos guardada en: {output_file}")
    
    return output_file

def save_results_table(results: Dict[int, Tuple[float, float, int]], 
                      output_file: str = "benchmark_tokenize_index_results.txt"):
    """Guarda tabla de resultados"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DE BENCHMARK - TOKENIZACIÓN + INDEXACIÓN\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"{'Num Docs':<12} {'T.Token(s)':<15} {'T.Index(s)':<15} {'Total(s)':<15} {'Tokens Únicos':<15}\n")
        f.write("-" * 80 + "\n")
        
        for num_docs in sorted(results.keys()):
            time_tokenize, time_index, unique_tokens = results[num_docs]
            total_time = time_tokenize + time_index
            
            f.write(f"{num_docs:<12} {time_tokenize:<15.4f} {time_index:<15.4f} "
                   f"{total_time:<15.4f} {unique_tokens:<15,}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        
        # Análisis de escalabilidad
        f.write("\nANÁLISIS DE ESCALABILIDAD:\n")
        f.write("-" * 80 + "\n")
        
        sorted_docs = sorted(results.keys())
        if len(sorted_docs) >= 2:
            first_docs = sorted_docs[0]
            last_docs = sorted_docs[-1]
            
            first_total = results[first_docs][0] + results[first_docs][1]
            last_total = results[last_docs][0] + results[last_docs][1]
            
            factor = last_docs / first_docs
            time_factor = last_total / first_total
            
            f.write(f"- Documentos: {first_docs} → {last_docs} (factor: {factor:.1f}x)\n")
            f.write(f"- Tiempo total: {first_total:.4f}s → {last_total:.4f}s (factor: {time_factor:.2f}x)\n")
            f.write(f"- Eficiencia: {'Lineal' if time_factor < factor * 1.5 else 'Sublineal'}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"✓ Tabla de resultados guardada en: {output_file}")

def main():
    """Función principal"""
    
    # Configuración
    input_dir = "data/input/Files"
    num_docs_to_test = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
    
    # Verificar que el directorio existe
    if not Path(input_dir).exists():
        print(f"❌ Error: No se encuentra el directorio {input_dir}")
        return
    
    # Ejecutar benchmark
    results = benchmark_tokenize_and_index(input_dir, num_docs_to_test)
    
    # Generar gráficas
    plot_results(results)
    plot_unique_tokens(results)
    
    # Guardar tabla de resultados
    save_results_table(results)
    
    print("\n" + "=" * 60)
    print("✓ Benchmark completado exitosamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
