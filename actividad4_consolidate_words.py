import os
import time
from typing import Set
from config import MATRICULA, FILES_DIRECTORY

def consolidate_words() -> tuple[float, Set[str], float]:
    start_total = time.perf_counter()
    
    # Ruta a la carpeta Words_Files
    words_dir = os.path.join(os.path.dirname(FILES_DIRECTORY), "Words_Files")
    consolidated_words: Set[str] = set()
    
    # Medir tiempo de consolidación
    start_consolidate = time.perf_counter()
    
    # Leer cada archivo _words.txt y agregar palabras al set
    for filename in sorted(os.listdir(words_dir)):
        if filename.endswith("_words.txt"):
            file_path = os.path.join(words_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                words = {line.strip().lower() for line in f if line.strip()}
                consolidated_words.update(words)
    
    consolidate_time = time.perf_counter() - start_consolidate
    total_time = time.perf_counter() - start_total
    
    return consolidate_time, consolidated_words, total_time

def main():
    # Ejecutar consolidación y obtener tiempos
    consolidate_time, words, total_time = consolidate_words()
    
    # Ordenar palabras
    sorted_words = sorted(words)
    
    # Guardar archivo consolidado
    words_dir = os.path.join(os.path.dirname(FILES_DIRECTORY), "Words_Files")
    consolidated_path = os.path.join(words_dir, "consolidado_palabras.txt")
    
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(f"{word}\n")
    
    # Crear reporte
    report_path = f"a4_{MATRICULA}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Reporte de consolidación de palabras\n")
        f.write(f"{'='*40}\n\n")
        f.write(f"Tiempo de consolidación: {consolidate_time:.2f} segundos\n")
        f.write(f"Número de palabras únicas: {len(words)}\n")
        f.write(f"Tiempo total de ejecución: {total_time:.2f} segundos\n")
        f.write(f"\nArchivo consolidado guardado en: {consolidated_path}\n")

if __name__ == "__main__":
    main()