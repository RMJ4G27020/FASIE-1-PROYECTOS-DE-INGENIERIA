import os
import time
import glob
import re
from typing import List, Tuple, Optional
from config import MATRICULA, FILES_DIRECTORY, ENCODING, PRECISION_DECIMALS, FALLBACK_ENCODINGS

def remove_html_tags(filename: str) -> float:
    """
    Función para eliminar las etiquetas HTML de un archivo.
    Recibe como parámetro el nombre del archivo.
    Retorna el tiempo que tardó en procesar el archivo.
    """
    start_time = time.perf_counter()
    
    content: Optional[str] = None
    encoding_used = ENCODING
    
    # Intentar abrir con UTF-8 primero
    try:
        with open(filename, 'r', encoding=ENCODING) as file:
            content = file.read()
    except UnicodeDecodeError:
        # Si falla UTF-8, intentar con codificaciones alternativas
        for encoding in FALLBACK_ENCODINGS:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                    encoding_used = encoding
                    break
            except (UnicodeDecodeError, UnicodeError):
                continue
    except Exception as e:
        print(f"Error al abrir {filename}: {e}")
        return 0
    
    if content is None:
        print(f"No se pudo decodificar {filename} con ninguna codificación")
        return 0
    
    # Eliminar etiquetas HTML usando expresiones regulares
    # Patrón que encuentra etiquetas HTML (incluye etiquetas con atributos)
    html_tag_pattern = re.compile(r'<[^>]+>')
    
    # Eliminar todas las etiquetas HTML
    clean_content = html_tag_pattern.sub('', content)
    
    # Limpiar espacios en blanco excesivos y líneas vacías
    clean_content = re.sub(r'\n\s*\n', '\n\n', clean_content)  # Múltiples líneas vacías -> doble salto
    clean_content = re.sub(r'[ \t]+', ' ', clean_content)  # Múltiples espacios -> un espacio
    clean_content = clean_content.strip()  # Quitar espacios al inicio y final
    
    # Crear nombre del archivo de salida
    base_name: str = os.path.splitext(os.path.basename(filename))[0]
    output_dir = "Clean_Files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_filename = os.path.join(output_dir, f"{base_name}_clean.txt")
    
    # Guardar el archivo sin etiquetas HTML
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(clean_content)
    except Exception as e:
        print(f"Error al escribir {output_filename}: {e}")
        return 0
    
    end_time = time.perf_counter()
    return end_time - start_time

def main():
    
    # Configuración
    files_directory = FILES_DIRECTORY
    matricula = MATRICULA
    output_file = f"a2_{matricula}.txt"
    
    # Verificar que existe el directorio Files
    if not os.path.exists(files_directory):
        print(f"Error: No se encontró el directorio {files_directory}")
        return
    
    # Obtener todos los archivos HTML del directorio Files
    html_files = glob.glob(os.path.join(files_directory, "*.html"))
    html_files.sort()  # Ordenar alfabéticamente
    
    if not html_files:
        print(f"No se encontraron archivos HTML en {files_directory}")
        return
    
    print(f"Encontrados {len(html_files)} archivos HTML")
    print("Iniciando eliminación de etiquetas HTML...")
    print(f"Los archivos limpios se guardarán en el directorio 'Clean_Files'")
    print("-" * 60)
    
    # Variables para almacenar resultados
    results = []
    total_individual_time = 0
    successful_files = 0
    
    # Medir tiempo total del programa
    program_start_time = time.perf_counter()
    
    # Procesar cada archivo HTML
    for html_file in html_files:
        filename = os.path.basename(html_file)
        file_time = remove_html_tags(html_file)
        
        if file_time > 0:
            successful_files += 1
            
        total_individual_time += file_time
        results.append((filename, file_time))
        
        # Mostrar progreso
        status = "✓" if file_time > 0 else "✗"
        print(f"{status} Procesado: {filename:<20} - Tiempo: {file_time:.{PRECISION_DECIMALS}f} segundos")
    
    # Tiempo total del programa
    program_end_time = time.perf_counter()
    total_program_time = program_end_time - program_start_time
    
    print("-" * 60)
    print(f"Procesamiento completado: {successful_files}/{len(html_files)} archivos exitosos")
    
    # Generar reporte
    with open(output_file, 'w', encoding='utf-8') as log_file:
        log_file.write("="*70 + "\n")
        log_file.write("REPORTE DE ELIMINACIÓN DE ETIQUETAS HTML\n")
        log_file.write("="*70 + "\n")
        log_file.write(f"Matrícula: {matricula}\n")
        log_file.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Total de archivos procesados: {len(html_files)}\n")
        log_file.write(f"Archivos procesados exitosamente: {successful_files}\n")
        log_file.write(f"Directorio de salida: Clean_Files/\n")
        log_file.write("="*70 + "\n\n")
        
        log_file.write("TIEMPOS DE PROCESAMIENTO INDIVIDUAL:\n")
        log_file.write("-"*50 + "\n")
        log_file.write(f"{'Archivo':<25} {'Tiempo (seg)':<15} {'Estado':<10}\n")
        log_file.write("-"*50 + "\n")
        
        for filename, file_time in results:
            status = "Exitoso" if file_time > 0 else "Error"
            log_file.write(f"{filename:<25} {file_time:<15.{PRECISION_DECIMALS}f} {status:<10}\n")
        
        log_file.write("-"*50 + "\n")
        log_file.write(f"{'TOTALES:':<25}\n")
        log_file.write(f"{'Suma individual:':<25} {total_individual_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write(f"{'Tiempo programa:':<25} {total_program_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write("-"*50 + "\n")
        
        # Estadísticas adicionales (solo archivos exitosos)
        if results and successful_files > 0:
            successful_times = [result[1] for result in results if result[1] > 0]
            if successful_times:
                avg_time = sum(successful_times) / len(successful_times)
                max_time = max(successful_times)
                min_time = min(successful_times)
                
                log_file.write(f"\nESTADÍSTICAS (archivos exitosos):\n")
                log_file.write(f"Tiempo promedio: {avg_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Tiempo máximo: {max_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Tiempo mínimo: {min_time:.{PRECISION_DECIMALS}f} segundos\n")
                log_file.write(f"Archivos procesados: {successful_files} de {len(html_files)}\n")
                log_file.write(f"Tasa de éxito: {(successful_files/len(html_files)*100):.1f}%\n")
        
        log_file.write("\n" + "="*70 + "\n")
        log_file.write("DESCRIPCIÓN DEL PROCESO:\n")
        log_file.write("="*70 + "\n")
        log_file.write("1. Lectura de archivos HTML con manejo de múltiples codificaciones\n")
        log_file.write("2. Eliminación de etiquetas HTML usando expresiones regulares\n")
        log_file.write("3. Limpieza de espacios en blanco y líneas vacías excesivas\n")
        log_file.write("4. Guardado de archivos limpios en directorio 'Clean_Files/'\n")
        log_file.write("5. Medición precisa de tiempos de procesamiento\n")
        log_file.write("\n" + "="*70 + "\n")
        log_file.write("FIN DEL REPORTE\n")
        log_file.write("="*70 + "\n")
    
    # Mostrar resumen en consola
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS:")
    print("="*60)
    print(f"Archivos HTML encontrados: {len(html_files)}")
    print(f"Archivos procesados exitosamente: {successful_files}")
    print(f"Tasa de éxito: {(successful_files/len(html_files)*100):.1f}%")
    print(f"Tiempo total (suma individual): {total_individual_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Tiempo total del programa: {total_program_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Directorio de salida: Clean_Files/")
    print(f"Reporte guardado en: {output_file}")
    print("="*60)

if __name__ == "__main__":
    main()
