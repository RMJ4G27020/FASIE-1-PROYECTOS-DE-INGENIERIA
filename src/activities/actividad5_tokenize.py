import os
import sys
import time
from collections import Counter
from typing import Dict, List, Tuple

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.config.config import MATRICULA

def process_html_file(input_file: str, output_dir: str) -> Dict[str, int]:
    """Procesa un archivo HTML y retorna diccionario de frecuencias de palabras."""
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Leer archivo de entrada y obtener palabras
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    # Extraer palabras (usando el mismo patrón de actividades anteriores)
    words = [word.strip() for word in content.split() if word.strip().isalnum()]
    
    # Contar frecuencias
    frequencies = Counter(words)
    
    # Crear archivo de salida tokenizado
    output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.html', '_tokens.txt'))
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, freq in sorted(frequencies.items()):
            f.write(f"{word} {freq}\n")
    
    return dict(frequencies)

def create_consolidated_reports(all_frequencies: Dict[str, int], output_dir: str) -> Tuple[float, float, float]:
    """Crea reportes consolidados ordenados por palabra y frecuencia."""
    start_total = time.perf_counter()
    
    # Ordenar alfabéticamente
    start_alpha = time.perf_counter()
    alpha_path = os.path.join(output_dir, "consolidated_alpha.txt")
    with open(alpha_path, 'w', encoding='utf-8') as f:
        for word, freq in sorted(all_frequencies.items()):
            f.write(f"{word} {freq}\n")
    alpha_time = time.perf_counter() - start_alpha
    
    # Ordenar por frecuencia
    start_freq = time.perf_counter()
    freq_path = os.path.join(output_dir, "consolidated_byfreq.txt")
    with open(freq_path, 'w', encoding='utf-8') as f:
        # Ordenar por frecuencia (descendente) y luego alfabéticamente
        sorted_by_freq = sorted(all_frequencies.items(), 
                              key=lambda x: (-x[1], x[0]))
        for word, freq in sorted_by_freq:
            f.write(f"{word} {freq}\n")
    freq_time = time.perf_counter() - start_freq
    
    total_time = time.perf_counter() - start_total
    return alpha_time, freq_time, total_time

def main():
    if len(sys.argv) != 3:
        print("Uso: python actividad5_tokenize.py input-directory output-directory")
        sys.exit(1)
    
    input_dir, output_dir = sys.argv[1:3]
    start_time = time.perf_counter()
    
    # Lista de archivos específicos a procesar
    target_files = ['simple.html', 'medium.html', 'hard.html', '49.html']
    
    # Procesar cada archivo y consolidar frecuencias
    all_frequencies: Dict[str, int] = Counter()
    for filename in target_files:
        input_file = os.path.join(input_dir, filename)
        if os.path.exists(input_file):
            file_frequencies = process_html_file(input_file, output_dir)
            all_frequencies.update(file_frequencies)
    
    # Crear reportes consolidados y medir tiempos
    alpha_time, freq_time, report_time = create_consolidated_reports(all_frequencies, output_dir)
    total_time = time.perf_counter() - start_time
    
    # Generar reporte de tiempos
    report_path = f"a5_{MATRICULA}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Reporte de procesamiento de tokens\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Archivos procesados: {', '.join(target_files)}\n")
        f.write(f"Total de palabras únicas: {len(all_frequencies)}\n")
        f.write(f"Total de ocurrencias: {sum(all_frequencies.values())}\n\n")
        f.write("Tiempos de ejecución:\n")
        f.write(f"- Ordenamiento alfabético: {alpha_time:.2f} segundos\n")
        f.write(f"- Ordenamiento por frecuencia: {freq_time:.2f} segundos\n")
        f.write(f"- Generación de reportes: {report_time:.2f} segundos\n")
        f.write(f"- Tiempo total: {total_time:.2f} segundos\n\n")
        f.write("Archivos generados:\n")
        f.write(f"1. Reporte alfabético: {os.path.join(output_dir, 'consolidated_alpha.txt')}\n")
        f.write(f"2. Reporte por frecuencia: {os.path.join(output_dir, 'consolidated_byfreq.txt')}\n")

if __name__ == "__main__":
    main()