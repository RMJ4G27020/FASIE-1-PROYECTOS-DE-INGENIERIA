import os
import sys
import time
from collections import defaultdict
from typing import Dict, Set

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.config.config import MATRICULA

class TokenStats:
    def __init__(self):
        self.frequency = 0  # Total repeticiones
        self.documents = set()  # Set de documentos que contienen el token
    
    @property
    def doc_count(self) -> int:
        return len(self.documents)

def process_html_file(input_file: str, token_dict: Dict[str, TokenStats]) -> float:
    """
    Procesa un archivo HTML y actualiza el diccionario de tokens.
    Retorna el tiempo de procesamiento.
    """
    start_time = time.perf_counter()
    
    # Obtener nombre base del archivo para tracking
    doc_id = os.path.basename(input_file)
    
    try:
        # Intentar con UTF-8 primero
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except UnicodeDecodeError:
        try:
            # Si falla, intentar con latin-1
            with open(input_file, 'r', encoding='latin-1') as f:
                content = f.read().lower()
        except:
            # Si ambos fallan, saltar este archivo
            print(f"Warning: No se pudo leer {input_file}")
            return time.perf_counter() - start_time
    
    # Extraer y contar palabras del documento
    words = [word.strip() for word in content.split() if word.strip().isalnum()]
    doc_frequencies: Dict[str, int] = defaultdict(int)
    
    # Primero contamos frecuencias en este documento
    for word in words:
        doc_frequencies[word] += 1
    
    # Luego actualizamos el diccionario global
    for word, freq in doc_frequencies.items():
        if word not in token_dict:
            token_dict[word] = TokenStats()
        
        token_dict[word].frequency += freq
        token_dict[word].documents.add(doc_id)
    
    return time.perf_counter() - start_time

def process_words_file(input_file: str, token_dict: Dict[str, TokenStats]) -> float:
    """
    Procesa un archivo de palabras y actualiza el diccionario de tokens.
    Retorna el tiempo de procesamiento.
    """
    start_time = time.perf_counter()
    
    # Obtener nombre base del archivo para tracking
    doc_id = os.path.basename(input_file)
    
    # Contador temporal para este documento
    doc_word_count: Dict[str, int] = defaultdict(int)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                doc_word_count[word] += 1
    
    # Actualizar el diccionario global con las frecuencias de este documento
    for word, count in doc_word_count.items():
        if word not in token_dict:
            token_dict[word] = TokenStats()
        
        # Agregar la frecuencia de este documento al total
        token_dict[word].frequency += count
        # Marcar que este documento contiene la palabra
        token_dict[word].documents.add(doc_id)
    
    return time.perf_counter() - start_time
    
    # Luego actualizamos el diccionario global
    for word, freq in doc_frequencies.items():
        if word not in token_dict:
            token_dict[word] = TokenStats()
        token_dict[word].frequency += freq
        token_dict[word].documents.add(doc_id)
    
    return time.perf_counter() - start_time

def create_dictionary_file(token_dict: Dict[str, TokenStats], output_dir: str) -> float:
    """
    Crea el archivo de diccionario con las tres columnas.
    Retorna el tiempo de generación.
    """
    start_time = time.perf_counter()
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear archivo de diccionario usando tabs como separador
    dict_path = os.path.join(output_dir, "dictionary.txt")
    with open(dict_path, 'w', encoding='utf-8') as f:
        # Escribir encabezado
        f.write("Token\tRepeticiones\t#Documentos\n")
        f.write("-" * 50 + "\n")
        
        # Escribir datos
        for token, stats in token_dict.items():
            f.write(f"{token}\t{stats.frequency}\t{stats.doc_count}\n")
    
    return time.perf_counter() - start_time

def main():
    if len(sys.argv) != 3:
        print("Uso: python actividad6_dictionary.py input-directory output-directory")
        sys.exit(1)
    
    input_dir, output_dir = sys.argv[1:3]
    start_total = time.perf_counter()
    
    # Diccionario para almacenar estadísticas de tokens
    token_dict: Dict[str, TokenStats] = {}
    
    # Procesar cada archivo HTML en el directorio
    file_times = []
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.html'):
            input_file = os.path.join(input_dir, filename)
            process_time = process_html_file(input_file, token_dict)
            file_times.append((filename, process_time))
    
    # Crear archivo de diccionario
    dict_time = create_dictionary_file(token_dict, output_dir)
    total_time = time.perf_counter() - start_total
    
    # Generar reporte de tiempos
    report_path = f"a6_{MATRICULA}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Reporte de generación de diccionario\n")
        f.write("=" * 40 + "\n\n")
        
        f.write("1. Procesamiento de archivos\n")
        f.write("-" * 30 + "\n")
        for filename, proc_time in file_times:
            f.write(f"{filename:<30} {proc_time:.2f} segundos\n")
        
        f.write("\n2. Estadísticas del diccionario\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total de tokens únicos: {len(token_dict)}\n")
        f.write(f"Total de documentos procesados: {len(file_times)}\n")
        
        f.write("\n3. Tiempos de ejecución\n")
        f.write("-" * 30 + "\n")
        f.write(f"Tiempo de generación del diccionario: {dict_time:.2f} segundos\n")
        f.write(f"Tiempo total de ejecución: {total_time:.2f} segundos\n")
        
        f.write(f"\nArchivo de diccionario generado en:\n{os.path.join(output_dir, 'dictionary.txt')}\n")

if __name__ == "__main__":
    main()