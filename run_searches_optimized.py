#!/usr/bin/env python3
"""
Actividad 13: Ejecutar búsquedas optimizadas
=============================================

Script para ejecutar las 12 búsquedas requeridas usando el método optimizado
(sin cargar archivos en memoria, solo lectura directa desde disco).

Genera archivo log a13_A00000000.txt con tiempos y top 10 resultados.

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

# Importar buscador optimizado
from retrieve_optimized import OptimizedDictionarySearcher
from src.config.config import MATRICULA


def main():
    """Ejecuta todas las búsquedas requeridas con método optimizado"""
    
    # Búsquedas a realizar
    searches = [
        ("Gauch", ["gauch"]),
        ("elephants", ["elephants"]),
        ("CSCE", ["csce"]),
        ("Arkansas", ["arkansas"]),
        ("gift", ["gift"]),
        ("abcdef", ["abcdef"]),
        ("20", ["20"]),
        ("20.07", ["20", "07"]),
        ("123-456-7890", ["123", "456", "7890"]),
        ("lawyer consumers", ["lawyer", "consumers"]),
        ("garden computer", ["garden", "computer"]),
        ("United States laws", ["united", "states", "laws"])
    ]
    
    print("\n" + "=" * 80)
    print("ACTIVIDAD 13: BUSQUEDAS OPTIMIZADAS (SIN CARGAR EN MEMORIA)")
    print("=" * 80)
    
    # Crear directorio de salida
    output_dir = PROJECT_ROOT / "data" / "output" / "activity13"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = output_dir / f"a13_{MATRICULA}.txt"
    
    # Abrir archivo log
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("ACTIVIDAD 13 - LOG DE BUSQUEDAS OPTIMIZADAS\n")
        log.write("=" * 80 + "\n")
        log.write(f"Matricula: {MATRICULA}\n")
        log.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total de busquedas: {len(searches)}\n")
        log.write(f"Metodo: Busqueda optimizada (sin cargar en memoria)\n")
        log.write("=" * 80 + "\n\n")
        
        # Inicializar buscadores optimizados
        print("\nInicializando buscadores optimizados...")
        data_dir = PROJECT_ROOT / "data" / "output"
        
        start_init = time.time()
        searcher_with_stop = OptimizedDictionarySearcher(str(data_dir), use_stop_list=True)
        init_time_with = time.time() - start_init
        
        start_init = time.time()
        searcher_no_stop = OptimizedDictionarySearcher(str(data_dir), use_stop_list=False)
        init_time_no = time.time() - start_init
        
        print(f"[OK] Buscadores inicializados")
        print(f"     Con stop list: {init_time_with:.4f} segundos")
        print(f"     Sin stop list: {init_time_no:.4f} segundos")
        
        log.write(f"Tiempo de inicializacion (con stop list): {init_time_with:.6f} segundos\n")
        log.write(f"Tiempo de inicializacion (sin stop list): {init_time_no:.6f} segundos\n\n")
        
        # Realizar búsquedas
        print("\n" + "=" * 80)
        print("EJECUTANDO BUSQUEDAS OPTIMIZADAS...")
        print("=" * 80 + "\n")
        
        total_search_time = 0
        
        for i, (query_name, tokens) in enumerate(searches, 1):
            print(f"\n[{i}/{len(searches)}] Buscando: {query_name}")
            log.write(f"\n{'=' * 80}\n")
            log.write(f"BUSQUEDA #{i}: {query_name}\n")
            log.write(f"Tokens: {', '.join(tokens)}\n")
            log.write(f"{'=' * 80}\n\n")
            
            # Buscar CON stop list (optimizado)
            start_time = time.time()
            if len(tokens) == 1:
                results_with = searcher_with_stop.search_token(tokens[0])
            else:
                results_with = searcher_with_stop.search_multiple_tokens(tokens)
            time_with = time.time() - start_time
            
            # Buscar SIN stop list (optimizado)
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
            
            # Escribir en log - CON STOP LIST
            log.write("CON STOP LIST:\n")
            log.write(f"  Tiempo de busqueda: {time_with:.6f} segundos\n")
            log.write(f"  Total de documentos: {len(results_with)}\n")
            
            if results_with:
                log.write("  Top 10 documentos:\n")
                for j, doc in enumerate(results_with[:10], 1):
                    doc_name = doc.get('doc_name', 'unknown')
                    if 'total_tfidf' in doc:
                        score = doc['total_tfidf']
                        log.write(f"    {j}. {doc_name} (score: {score:.4f})\n")
                    else:
                        tfidf = doc.get('tfidf', 0)
                        log.write(f"    {j}. {doc_name} (tfidf: {tfidf:.4f})\n")
                
                if len(results_with) > 10:
                    log.write(f"    ... y {len(results_with) - 10} documentos mas\n")
            else:
                log.write("  No se encontraron documentos\n")
            
            # Escribir en log - SIN STOP LIST
            log.write("\nSIN STOP LIST:\n")
            log.write(f"  Tiempo de busqueda: {time_no:.6f} segundos\n")
            log.write(f"  Total de documentos: {len(results_no)}\n")
            
            if results_no:
                log.write("  Top 10 documentos:\n")
                for j, doc in enumerate(results_no[:10], 1):
                    doc_name = doc.get('doc_name', 'unknown')
                    if 'total_tfidf' in doc:
                        score = doc['total_tfidf']
                        log.write(f"    {j}. {doc_name} (score: {score:.4f})\n")
                    else:
                        tfidf = doc.get('tfidf', 0)
                        log.write(f"    {j}. {doc_name} (tfidf: {tfidf:.4f})\n")
                
                if len(results_no) > 10:
                    log.write(f"    ... y {len(results_no) - 10} documentos mas\n")
            else:
                log.write("  No se encontraron documentos\n")
        
        # Resumen final
        log.write(f"\n{'=' * 80}\n")
        log.write("RESUMEN FINAL\n")
        log.write(f"{'=' * 80}\n")
        log.write(f"Total de busquedas realizadas: {len(searches)}\n")
        log.write(f"Tiempo total de busqueda: {total_search_time:.6f} segundos\n")
        log.write(f"Tiempo promedio por busqueda: {total_search_time/(len(searches)*2):.6f} segundos\n")
        log.write(f"\nNOTA: Metodo optimizado - sin cargar archivos en memoria\n")
        log.write(f"      Solo se carga indice hash ({init_time_with:.6f} seg)\n")
        log.write(f"      Lectura directa desde disco durante busqueda\n")
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print(f"Archivo log generado: {log_file}")
    print(f"Total de busquedas: {len(searches)} x 2 (con/sin stop list)")
    print(f"Tiempo total de busqueda: {total_search_time:.3f} segundos")
    print(f"Metodo: Optimizado (sin cargar en memoria)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
