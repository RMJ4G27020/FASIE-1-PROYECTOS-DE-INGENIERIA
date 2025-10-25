#!/usr/bin/env python3
"""
Script launcher para ejecutar las actividades del proyecto.
Este script configura el path correctamente para las importaciones.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_activity_4():
    """Ejecuta la actividad 4: Consolidación de palabras"""
    try:
        from src.activities.actividad4_consolidate_words import consolidate_words
        print("Ejecutando Actividad 4: Consolidación de Palabras")
        execution_time, unique_words, processing_time = consolidate_words()
        print(f"✓ Actividad 4 completada en {execution_time:.2f} segundos")
        print(f"  - Palabras únicas: {len(unique_words)}")
        print(f"  - Tiempo de procesamiento: {processing_time:.2f} segundos")
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 4: {e}")

def run_activity_5():
    """Ejecuta la actividad 5: Tokenización"""
    try:
        print("Ejecutando Actividad 5: Tokenización")
        
        # Configurar directorios con rutas correctas
        input_dir = "data/input/Files"  # Carpeta con archivos HTML
        output_dir = "data/output/activity5"
        
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Importar y ejecutar la función principal
        import src.activities.actividad5_tokenize as act5
        
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad5_tokenize.py", input_dir, output_dir]
        
        try:
            act5.main()
            print(f"✓ Actividad 5 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
            
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 5: {e}")

def run_activity_6():
    """Ejecuta la actividad 6: Análisis de diccionario"""
    try:
        print("Ejecutando Actividad 6: Análisis de Diccionario")
        
        # Configurar directorios
        input_dir = "data/input/Files"  # Usar archivos HTML originales para obtener frecuencias reales
        output_dir = "data/output/activity6"
        
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Importar y ejecutar la función principal
        import src.activities.actividad6_dictionary as act6
        
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad6_dictionary.py", input_dir, output_dir]
        
        try:
            act6.main()
            print(f"✓ Actividad 6 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
            
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 6: {e}")

def run_activity_7():
    """Ejecuta la actividad 7: Archivo Posting"""
    try:
        print("Ejecutando Actividad 7: Archivo Posting")
        # Configurar directorios
        input_dir = "data/input/Files"  # Carpeta con archivos HTML
        output_dir = "data/output/activity7"
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        # Importar y ejecutar la función principal
        import src.activities.actividad7_posting_files as act7
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad7_posting_files.py", input_dir, output_dir]
        try:
            act7.main()
            print(f"✓ Actividad 7 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 7: {e}")

def run_activity_8():
    """Ejecuta la actividad 8: Hash Table"""
    try:
        print("Ejecutando Actividad 8: Hash Table")
        # Configurar directorios
        dict_file = "data/output/activity7/dictionary_posting.txt"
        output_dir = "data/output/activity8"
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        # Importar y ejecutar la función principal
        import src.activities.actividad8_hash_table as act8
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad8_hash_table.py", dict_file, output_dir]
        try:
            act8.main()
            print(f"✓ Actividad 8 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 8: {e}")

def run_activity_9():
    """Ejecuta la actividad 9: Stop List"""
    try:
        print("Ejecutando Actividad 9: Stop List")
        # Configurar directorios
        dict_file = "data/output/activity7/dictionary_posting.txt"
        output_dir = "data/output/activity9"
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        # Importar y ejecutar la función principal
        import src.activities.actividad9_stop_list as act9
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad9_stop_list.py", dict_file, output_dir]
        try:
            act9.main()
            print(f"✓ Actividad 9 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 9: {e}")

def run_activity_10():
    """Ejecuta la actividad 10: TF-IDF Weight Tokens"""
    try:
        print("Ejecutando Actividad 10: TF-IDF Weight Tokens")
        # Configurar directorios
        filtered_dict_file = "data/output/activity9/dictionary_filtered.txt"
        html_dir = "data/input/Files"
        output_dir = "data/output/activity10"
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        # Importar y ejecutar la función principal
        import src.activities.actividad10_tfidf_weights as act10
        # Simular argumentos de línea de comandos
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ["actividad10_tfidf_weights.py", filtered_dict_file, html_dir, output_dir]
        try:
            act10.main()
            print(f"✓ Actividad 10 completada. Resultados en: {output_dir}")
        finally:
            sys.argv = original_argv
    except Exception as e:
        print(f"❌ Error ejecutando Actividad 10: {e}")

def main():
    """Función principal del launcher"""
    print("=== Launcher de Actividades HTML Processor ===")
    print("\n📋 FASE 1 & 2: PROCESAMIENTO BÁSICO")
    print("1. Actividad 4: Consolidación de Palabras")
    print("2. Actividad 5: Tokenización")
    print("3. Actividad 6: Análisis de Diccionario")
    print("\n📋 FASE 3: WEIGHT TOKENS")
    print("7. Actividad 7: Archivo Posting")
    print("8. Actividad 8: Hash Table")
    print("9. Actividad 9: Stop List")
    print("10. Actividad 10: TF-IDF Weight Tokens")
    print("\n📋 OPCIONES ESPECIALES")
    print("4. Ejecutar Fase 1 & 2 (Actividades 4-6)")
    print("11. Ejecutar Fase 3 completa (Actividades 7-10)")
    print("12. Ejecutar TODAS las actividades (4-10)")
    print("0. Salir")
    
    choice = input("\nSeleccione una opción: ")
    
    if choice == "1":
        run_activity_4()
    elif choice == "2":
        run_activity_5()
    elif choice == "3":
        run_activity_6()
    elif choice == "4":
        print("\n🚀 Ejecutando Fase 1 & 2...")
        run_activity_4()
        print("-" * 50)
        run_activity_5()
        print("-" * 50)
        run_activity_6()
    elif choice == "7":
        run_activity_7()
    elif choice == "8":
        run_activity_8()
    elif choice == "9":
        run_activity_9()
    elif choice == "10":
        run_activity_10()
    elif choice == "11":
        print("\n🚀 Ejecutando Fase 3 completa...")
        run_activity_7()
        print("-" * 50)
        run_activity_8()
        print("-" * 50)
        run_activity_9()
        print("-" * 50)
        run_activity_10()
    elif choice == "12":
        print("\n🚀 Ejecutando TODAS las actividades...")
        run_activity_4()
        print("-" * 50)
        run_activity_5()
        print("-" * 50)
        run_activity_6()
        print("-" * 50)
        run_activity_7()
        print("-" * 50)
        run_activity_8()
        print("-" * 50)
        run_activity_9()
        print("-" * 50)
        run_activity_10()
    elif choice == "0":
        print("¡Hasta luego!")
    else:
        print("Opción no válida")


if __name__ == "__main__":
    main()