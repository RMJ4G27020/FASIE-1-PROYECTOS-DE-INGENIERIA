#!/usr/bin/env python3
"""
Script para mostrar un resumen de todos los resultados generados.
"""

import os
from pathlib import Path

def show_results_summary():
    """Muestra un resumen de todos los archivos generados por las actividades"""
    
    print("=" * 60)
    print("RESUMEN DE RESULTADOS GENERADOS")
    print("=" * 60)
    
    # Actividad 4: Consolidación
    print("\n📁 ACTIVIDAD 4: CONSOLIDACIÓN DE PALABRAS")
    print("-" * 40)
    words_dir = Path("Words_Files")
    if words_dir.exists():
        files = list(words_dir.glob("*.txt"))
        print(f"✓ Directorio: {words_dir}")
        print(f"✓ Archivos generados: {len(files)}")
        
        # Mostrar algunos archivos importantes
        important_files = ["consolidado_palabras.txt", "test-002_words.txt"]
        for file in important_files:
            file_path = words_dir / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  - {file} ({size:,} bytes)")
    else:
        print("❌ Directorio Words_Files no encontrado")
    
    # Actividad 5: Tokenización
    print("\n📁 ACTIVIDAD 5: TOKENIZACIÓN")
    print("-" * 40)
    act5_dir = Path("data/output/activity5")
    if act5_dir.exists():
        files = list(act5_dir.glob("*.txt"))
        print(f"✓ Directorio: {act5_dir}")
        print(f"✓ Archivos generados: {len(files)}")
        
        for file in files:
            size = file.stat().st_size
            print(f"  - {file.name} ({size:,} bytes)")
    else:
        print("❌ Directorio activity5 no encontrado")
    
    # Actividad 6: Análisis de Diccionario
    print("\n📁 ACTIVIDAD 6: ANÁLISIS DE DICCIONARIO")
    print("-" * 40)
    act6_dir = Path("data/output/activity6")
    if act6_dir.exists():
        files = list(act6_dir.glob("*.txt"))
        print(f"✓ Directorio: {act6_dir}")
        print(f"✓ Archivos generados: {len(files)}")
        
        for file in files:
            size = file.stat().st_size
            print(f"  - {file.name} ({size:,} bytes)")
    else:
        print("❌ Directorio activity6 no encontrado")
    
    # Otros directorios de salida
    print("\n📁 OTROS ARCHIVOS DE SALIDA")
    print("-" * 40)
    other_dirs = [
        "data/output/clean_files",
        "data/output/words_files", 
        "data/output/reports"
    ]
    
    for dir_path in other_dirs:
        path = Path(dir_path)
        if path.exists():
            files = list(path.glob("*"))
            print(f"✓ {dir_path}: {len(files)} archivos")
        else:
            print(f"❌ {dir_path}: No encontrado")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    total_output_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk("data/output"):
        for file in files:
            file_path = Path(root) / file
            total_output_files += 1
            total_size += file_path.stat().st_size
    
    words_files = len(list(Path("Words_Files").glob("*.txt"))) if Path("Words_Files").exists() else 0
    
    print(f"✓ Total archivos de salida (data/output): {total_output_files}")
    print(f"✓ Total archivos Words_Files: {words_files}")
    print(f"✓ Tamaño total: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print(f"✓ Actividades completadas: 3/3")

if __name__ == "__main__":
    show_results_summary()