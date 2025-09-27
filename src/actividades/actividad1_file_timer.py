import os
import time
import glob
from typing import List, Tuple
from config import MATRICULA, FILES_DIRECTORY, ENCODING, PRECISION_DECIMALS, FALLBACK_ENCODINGS

def open_file(filename: str) -> float:
    """
    Función para abrir un archivo HTML de manera eficiente.
    Recibe como parámetro el nombre del archivo.
    Retorna el tiempo que tardó en abrir el archivo.
    """
    start_time = time.perf_counter()
    
    content = None
    
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
                    break
            except (UnicodeDecodeError, UnicodeError):
                continue
    except Exception as e:
        print(f"Error al abrir {filename}: {e}")
        return 0
    
    if content is None:
        print(f"No se pudo decodificar {filename} con ninguna codificación")
        return 0
    
    end_time = time.perf_counter()
    return end_time - start_time

def main() -> None:
    # Configuración
    files_directory: str = FILES_DIRECTORY
    matricula: str = MATRICULA
    output_file: str = f"a1_{matricula}.txt"
    
    # Verificar que existe el directorio Files
    if not os.path.exists(files_directory):
        print(f"Error: No se encontró el directorio {files_directory}")
        return
    
    # Obtener todos los archivos HTML del directorio Files
    html_files: List[str] = glob.glob(os.path.join(files_directory, "*.html"))
    html_files.sort()  # Ordenar alfabéticamente
    
    if not html_files:
        print(f"No se encontraron archivos HTML en {files_directory}")
        return
    
    print(f"Encontrados {len(html_files)} archivos HTML")
    print("Iniciando medición de tiempos...")
    
    # Variables para almacenar resultados
    results: List[Tuple[str, float]] = []
    total_individual_time: float = 0
    
    # Medir tiempo total del programa
    program_start_time: float = time.perf_counter()
    
    # Procesar cada archivo HTML
    for html_file in html_files:
        filename: str = os.path.basename(html_file)
        file_time: float = open_file(html_file)
        total_individual_time += file_time
        results.append((filename, file_time))
        print(f"Procesado: {filename} - Tiempo: {file_time:.{PRECISION_DECIMALS}f} segundos")
    
    # Tiempo total del programa
    program_end_time: float = time.perf_counter()
    total_program_time: float = program_end_time - program_start_time
    
    # Generar reporte
    with open(output_file, 'w', encoding='utf-8') as log_file:
        log_file.write("="*60 + "\n")
        log_file.write("REPORTE DE TIEMPOS DE APERTURA DE ARCHIVOS HTML\n")
        log_file.write("="*60 + "\n")
        log_file.write(f"Matrícula: {matricula}\n")
        log_file.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Total de archivos procesados: {len(html_files)}\n")
        log_file.write("="*60 + "\n\n")
        
        log_file.write("TIEMPOS INDIVIDUALES:\n")
        log_file.write("-"*40 + "\n")
        log_file.write(f"{'Archivo':<15} {'Tiempo (seg)':<15}\n")
        log_file.write("-"*40 + "\n")
        
        for filename, file_time in results:
            log_file.write(f"{filename:<15} {file_time:<15.{PRECISION_DECIMALS}f}\n")
        
        log_file.write("-"*40 + "\n")
        log_file.write(f"{'TOTALES:':<15}\n")
        log_file.write(f"{'Suma individual:':<15} {total_individual_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write(f"{'Tiempo programa:':<15} {total_program_time:<15.{PRECISION_DECIMALS}f}\n")
        log_file.write("-"*40 + "\n")
        
        # Estadísticas adicionales
        if results:
            times: List[float] = [result[1] for result in results]
            avg_time: float = sum(times) / len(times)
            max_time: float = max(times)
            min_time: float = min(times)
            
            log_file.write(f"\nESTADÍSTICAS:\n")
            log_file.write(f"Tiempo promedio: {avg_time:.{PRECISION_DECIMALS}f} segundos\n")
            log_file.write(f"Tiempo máximo: {max_time:.{PRECISION_DECIMALS}f} segundos\n")
            log_file.write(f"Tiempo mínimo: {min_time:.{PRECISION_DECIMALS}f} segundos\n")
        
        log_file.write("\n" + "="*60 + "\n")
        log_file.write("FIN DEL REPORTE\n")
        log_file.write("="*60 + "\n")
    
    # Mostrar resumen en consola
    print("\n" + "="*50)
    print("RESUMEN DE RESULTADOS:")
    print("="*50)
    print(f"Archivos procesados: {len(html_files)}")
    print(f"Tiempo total (suma individual): {total_individual_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Tiempo total del programa: {total_program_time:.{PRECISION_DECIMALS}f} segundos")
    print(f"Reporte guardado en: {output_file}")
    print("="*50)

if __name__ == "__main__":
    main()
