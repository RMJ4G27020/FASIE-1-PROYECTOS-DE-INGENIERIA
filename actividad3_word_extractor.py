import os
import time
import glob
import re
from typing import List, Set
from config import MATRICULA, PRECISION_DECIMALS, FALLBACK_ENCODINGS

def extract_and_sort_words(filename: str) -> float:
    """
    Función para extraer palabras de un archivo limpio y ordenarlas alfabéticamente.
    Recibe como parámetro el nombre del archivo.
    Retorna el tiempo que tardó en procesar el archivo.
    """
    start_time = time.perf_counter()
    
    content = None
    
    # Intentar abrir el archivo con diferentes codificaciones
    encodings_to_try = ['utf-8'] + FALLBACK_ENCODINGS
    
    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                content = file.read()
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            print(f"Error al abrir {filename}: {e}")
            return 0
    
    if content is None:
        print(f"No se pudo decodificar {filename} con ninguna codificación")
        return 0
    
    # Extraer palabras usando expresiones regulares
    # Patrón que encuentra palabras (incluye palabras con guiones y apostrofes)
    # Por ejemplo: "word", "don't", "state-of-the-art", "Automata-based"
    word_pattern = re.compile(r'\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b')
    
    # Encontrar todas las palabras
    words_found = word_pattern.findall(content)
    
    # Convertir a minúsculas para ordenamiento consistente y eliminar duplicados
    unique_words = set(word.lower() for word in words_found)
    
    # Ordenar palabras alfabéticamente (usando la función sort integrada de Python)
    sorted_words = sorted(unique_words)
    
    # Crear nombre del archivo de salida
    base_name = os.path.splitext(os.path.basename(filename))[0]
    # Remover "_clean" del nombre si existe
    if base_name.endswith('_clean'):
        base_name = base_name[:-6]
    
    output_dir = "Words_Files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_filename = os.path.join(output_dir, f"{base_name}_words.txt")
    
    # Guardar las palabras ordenadas (una por línea)
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for word in sorted_words:
                file.write(word + '\n')
    except Exception as e:
        print(f"Error al escribir {output_filename}: {e}")
        return 0
    
    end_time = time.perf_counter()
    return end_time - start_time

def main():
    # Configuración
    clean_files_directory = "Clean_Files"
    matricula = MATRICULA
    output_file = f"a3_{matricula}.txt"
    
    # Verificar que existe el directorio Clean_Files
    if not os.path.exists(clean_files_directory):
        print(f"Error: No se encontró el directorio {clean_files_directory}")
        print("Primero ejecuta la Actividad 2 para generar los archivos limpios")
        return
    
    # Obtener todos los archivos limpios (.txt) del directorio Clean_Files
    clean_files = glob.glob(os.path.join(clean_files_directory, "*_clean.txt"))
    clean_files.sort()  # Ordenar alfabéticamente
    
    if not clean_files:
        print(f"No se encontraron archivos limpios en {clean_files_directory}")
        print("Primero ejecuta la Actividad 2 para generar los archivos limpios")
        return
    
    print(f"Encontrados {len(clean_files)} archivos limpios")
    print("Iniciando extracción y ordenamiento de palabras...")
    print(f"Los archivos de palabras se guardarán en el directorio 'Words_Files'")
    print("-" * 70)
    
    # Variables para almacenar resultados
    results = []
    total_individual_time = 0
    successful_files = 0
    total_words_processed = 0
    
    # Medir tiempo total del programa
    program_start_time = time.perf_counter()
    
    # Procesar cada archivo limpio
    for clean_file in clean_files:
        filename = os.path.basename(clean_file)
        file_time = extract_and_sort_words(clean_file)
        
        if file_time > 0:
            successful_files += 1
            # Contar palabras en el archivo generado
            words_file = filename.replace('_clean.txt', '_words.txt')
            words_path = os.path.join("Words_Files", words_file)
            try:
                with open(words_path, 'r', encoding='utf-8') as f:
                    word_count = sum(1 for line in f)
                total_words_processed += word_count
            except:
                word_count = 0
        else:
            word_count = 0
            
        total_individual_time += file_time
        results.append((filename, file_time, word_count))
        
        # Mostrar progreso
        status = "✓" if file_time > 0 else "✗"
        print(f"{status} Procesado: {filename:<25} - Tiempo: {file_time:.{PRECISION_DECIMALS}f}s - Palabras: {word_count}")
    
    # Tiempo total del programa
    program_end_time = time.perf_counter()
    total_program_time = program_end_time - program_start_time
    
    print("-" * 70)
    print(f"Procesamiento completado: {successful_files}/{len(clean_files)} archivos exitosos")
    print(f"Total de palabras únicas procesadas: {total_words_processed}")
    
    # Generar reporte
    with open(output_file, 'w', encoding='utf-8') as log_file:
        log_file.write("="*80 + "\n")
        log_file.write("REPORTE DE EXTRACCIÓN Y ORDENAMIENTO DE PALABRAS\n")
        log_file.write("="*80 + "\n")
        log_file.write(f"Matrícula: {matricula}\n")
        log_file.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Total de archivos procesados: {len(clean_files)}\n")
        log_file.write(f"Archivos procesados exitosamente: {successful_files}\n")
        log_file.write(f"Total de palabras únicas extraídas: {total_words_processed}\n")
        log_file.write(f"Directorio de entrada: {clean_files_directory}/\n")
        log_file.write(f"Directorio de salida: Words_Files/\n")
        log_file.write("="*80 + "\n\n")
        
        log_file.write("TIEMPOS DE PROCESAMIENTO INDIVIDUAL:\n")
        log_file.write("-"*65 + "\n")
        log_file.write(f"{'Archivo':<30} {'Tiempo (seg)':<15} {'Palabras':<10} {'Estado':<10}\n")
        log_file.write("-"*65 + "\n")
        
        for filename, file_time, word_count in results:
            status = "Exitoso" if file_time > 0 else "Error"
            log_file.write(f"{filename:<30} {file_time:<15.{PRECISION_DECIMALS}f} {word_count:<10} {status:<10}\n")
        
        log_file.write("-"*65 + "\n")
        log_file.write(f"{'TOTALES:':<30}\n")
        log_file.write(f"{'Suma individual:':<30} {total_individual_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write(f"{'Tiempo programa:':<30} {total_program_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write(f"{'Total palabras:':<30} {total_words_processed:<15}\n")
        log_file.write("-"*65 + "\n")
        
        # Estadísticas adicionales (solo archivos exitosos)
        if results and successful_files > 0:
            successful_times = [result[1] for result in results if result[1] > 0]
            successful_words = [result[2] for result in results if result[1] > 0]
            
            if successful_times:
                avg_time = sum(successful_times) / len(successful_times)
                max_time = max(successful_times)
                min_time = min(successful_times)
                avg_words = sum(successful_words) / len(successful_words) if successful_words else 0
                max_words = max(successful_words) if successful_words else 0
                min_words = min(successful_words) if successful_words else 0
                
                log_file.write(f"\nESTADÍSTICAS (archivos exitosos):\n")
                log_file.write(f"Tiempo promedio: {avg_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Tiempo máximo: {max_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Tiempo mínimo: {min_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Promedio de palabras por archivo: {avg_words:.1f}\n")
                log_file.write(f"Máximo de palabras en un archivo: {max_words}\n")
                log_file.write(f"Mínimo de palabras en un archivo: {min_words}\n")
                log_file.write(f"Archivos procesados: {successful_files} de {len(clean_files)}\n")
                log_file.write(f"Tasa de éxito: {(successful_files/len(clean_files)*100):.1f}%\n")
        
        log_file.write("\n" + "="*80 + "\n")
        log_file.write("DESCRIPCIÓN DEL PROCESO:\n")
        log_file.write("="*80 + "\n")
        log_file.write("1. Lectura de archivos limpios (sin etiquetas HTML)\n")
        log_file.write("2. Extracción de palabras usando expresiones regulares\n")
        log_file.write("3. Manejo de palabras con caracteres especiales (guiones, apostrofes)\n")
        log_file.write("4. Conversión a minúsculas y eliminación de duplicados\n")
        log_file.write("5. Ordenamiento alfabético usando función sort() de Python\n")
        log_file.write("6. Guardado de palabras en archivos individuales (una palabra por línea)\n")
        log_file.write("7. Medición precisa de tiempos de procesamiento\n")
        log_file.write("\nEJEMPLOS DE PALABRAS PROCESADAS:\n")
        log_file.write("- Palabras simples: 'word', 'example', 'test'\n")
        log_file.write("- Palabras con apostrofe: 'don't', 'can't', 'it's'\n")
        log_file.write("- Palabras con guión: 'state-of-the-art', 'automata-based'\n")
        log_file.write("- Todas convertidas a minúsculas y ordenadas alfabéticamente\n")
        log_file.write("\n" + "="*80 + "\n")
        log_file.write("FIN DEL REPORTE\n")
        log_file.write("="*80 + "\n")
    
    # Mostrar resumen en consola
    print("\n" + "="*70)
    print("RESUMEN DE RESULTADOS:")
    print("="*70)
    print(f"Archivos limpios encontrados: {len(clean_files)}")
    print(f"Archivos procesados exitosamente: {successful_files}")
    print(f"Total de palabras únicas extraídas: {total_words_processed}")
    print(f"Tasa de éxito: {(successful_files/len(clean_files)*100):.1f}%")
    print(f"Tiempo total (suma individual): {total_individual_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Tiempo total del programa: {total_program_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Directorio de entrada: {clean_files_directory}/")
    print(f"Directorio de salida: Words_Files/")
    print(f"Reporte guardado en: {output_file}")
    print("="*70)

if __name__ == "__main__":
    main()
