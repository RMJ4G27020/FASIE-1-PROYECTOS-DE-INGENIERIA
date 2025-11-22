#!/usr/bin/env python3
"""
Actividad 12: Ejecutar búsquedas requeridas
============================================

Script para ejecutar las 12 búsquedas requeridas en la actividad:
1. Gauch
2. elephants
3. CSCE
4. Arkansas
5. gift
6. abcdef
7. 20
8. 20.07
9. 123-456-7890
10. lawyer consumers
11. garden computer
12. United States laws

Genera archivo log a12_A00000000.txt con tiempos.

Autor: JOSE GPE RICO MORENO
Fecha: Noviembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
from pathlib import Path

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importar buscador
sys.path.insert(0, str(PROJECT_ROOT))
from retrieve import DictionarySearcher
from src.config.config import MATRICULA


def main():
    """Ejecuta todas las búsquedas requeridas"""
    
    # Búsquedas a realizar
    searches = [
        ("Gauch", ["gauch"]),
        ("elephants", ["elephants"]),
        ("CSCE", ["csce"]),
        ("Arkansas", ["arkansas"]),
        ("gift", ["gift"]),
        ("abcdef", ["abcdef"]),
        ("20", ["20"]),
        ("20.07", ["20", "07"]),  # Separado porque no hay puntos en tokens
        ("123-456-7890", ["123", "456", "7890"]),  # Separado por guiones
        ("lawyer consumers", ["lawyer", "consumers"]),
        ("garden computer", ["garden", "computer"]),
        ("United States laws", ["united", "states", "laws"])
    ]
    
    print("\n" + "=" * 80)
    print("ACTIVIDAD 12: BUSQUEDAS REQUERIDAS")
    print("=" * 80)
    
    # Crear directorio de salida
    output_dir = PROJECT_ROOT / "data" / "output" / "activity12"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = output_dir / f"a12_{MATRICULA}.txt"
    
    # Abrir archivo log
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("ACTIVIDAD 12 - LOG DE BUSQUEDAS\n")
        log.write("=" * 80 + "\n")
        log.write(f"Matricula: {MATRICULA}\n")
        log.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total de busquedas: {len(searches)}\n")
        log.write("=" * 80 + "\n\n")
        
        # Inicializar buscadores (con y sin stop list)
        print("\nInicializando buscadores...")
        data_dir = PROJECT_ROOT / "data" / "output"
        
        start_load = time.time()
        searcher_with_stop = DictionarySearcher(str(data_dir), use_stop_list=True)
        load_time_with = time.time() - start_load
        
        start_load = time.time()
        searcher_no_stop = DictionarySearcher(str(data_dir), use_stop_list=False)
        load_time_no = time.time() - start_load
        
        print(f"[OK] Buscadores inicializados")
        print(f"     Con stop list: {load_time_with:.4f} segundos")
        print(f"     Sin stop list: {load_time_no:.4f} segundos")
        
        log.write(f"Tiempo de carga (con stop list): {load_time_with:.6f} segundos\n")
        log.write(f"Tiempo de carga (sin stop list): {load_time_no:.6f} segundos\n\n")
        
        # Realizar búsquedas
        print("\n" + "=" * 80)
        print("EJECUTANDO BUSQUEDAS...")
        print("=" * 80 + "\n")
        
        total_search_time = 0
        
        for i, (query_name, tokens) in enumerate(searches, 1):
            print(f"\n[{i}/{len(searches)}] Buscando: {query_name}")
            log.write(f"\n{'=' * 80}\n")
            log.write(f"BUSQUEDA #{i}: {query_name}\n")
            log.write(f"Tokens: {', '.join(tokens)}\n")
            log.write(f"{'=' * 80}\n\n")
            
            # Buscar CON stop list
            start_time = time.time()
            if len(tokens) == 1:
                results_with = searcher_with_stop.search_token(tokens[0])
            else:
                results_with = searcher_with_stop.search_multiple_tokens(tokens)
            time_with = time.time() - start_time
            
            # Buscar SIN stop list
            start_time = time.time()
            if len(tokens) == 1:
                results_no = searcher_no_stop.search_token(tokens[0])
            else:
                results_no = searcher_no_stop.search_multiple_tokens(tokens)
            time_no = time.time() - start_time
            
            total_search_time += time_with + time_no
            
            # Mostrar resultados
            print(f"  Con stop list: {len(results_with)} documentos ({time_with:.6f} seg)")
            print(f"  Sin stop list: {len(results_no)} documentos ({time_no:.6f} seg)")
            
            # Escribir en log
            log.write("CON STOP LIST:\n")
            log.write(f"  Tiempo de busqueda: {time_with:.6f} segundos\n")
            log.write(f"  Documentos encontrados: {len(results_with)}\n")
            
            if results_with:
                log.write("  Documentos:\n")
                for j, doc in enumerate(results_with[:10], 1):  # Top 10
                    doc_name = doc.get('doc_name', 'unknown')
                    if 'total_tfidf' in doc:
                        score = doc['total_tfidf']
                        log.write(f"    {j}. {doc_name} (score: {score:.4f})\n")
                    else:
                        tfidf = doc.get('tfidf', 0)
                        log.write(f"    {j}. {doc_name} (tfidf: {tfidf:.4f})\n")
                
                if len(results_with) > 10:
                    log.write(f"    ... y {len(results_with) - 10} mas\n")
            else:
                log.write("  No se encontraron documentos\n")
            
            log.write("\nSIN STOP LIST:\n")
            log.write(f"  Tiempo de busqueda: {time_no:.6f} segundos\n")
            log.write(f"  Documentos encontrados: {len(results_no)}\n")
            
            if results_no:
                log.write("  Documentos:\n")
                for j, doc in enumerate(results_no[:10], 1):  # Top 10
                    doc_name = doc.get('doc_name', 'unknown')
                    if 'total_tfidf' in doc:
                        score = doc['total_tfidf']
                        log.write(f"    {j}. {doc_name} (score: {score:.4f})\n")
                    else:
                        tfidf = doc.get('tfidf', 0)
                        log.write(f"    {j}. {doc_name} (tfidf: {tfidf:.4f})\n")
                
                if len(results_no) > 10:
                    log.write(f"    ... y {len(results_no) - 10} mas\n")
            else:
                log.write("  No se encontraron documentos\n")
        
        # Resumen final
        log.write(f"\n{'=' * 80}\n")
        log.write("RESUMEN FINAL\n")
        log.write(f"{'=' * 80}\n")
        log.write(f"Total de busquedas realizadas: {len(searches)}\n")
        log.write(f"Tiempo total de busqueda: {total_search_time:.6f} segundos\n")
        log.write(f"Tiempo promedio por busqueda: {total_search_time/(len(searches)*2):.6f} segundos\n")
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print(f"Archivo log generado: {log_file}")
    print(f"Total de busquedas: {len(searches)} x 2 (con/sin stop list)")
    print(f"Tiempo total de busqueda: {total_search_time:.3f} segundos")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
