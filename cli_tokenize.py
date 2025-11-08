#!/usr/bin/env python3
"""
CLI: Tokenización de Documentos HTML
=====================================

Comando para tokenizar documentos HTML desde línea de comandos.

Uso:
    tokenize <input-dir> <output-dir>

Ejemplo:
    tokenize data/input/Files data/output/tokens
"""

import sys
import os
from pathlib import Path
from typing import List
import json

# Agregar el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.activities.actividad5_tokenize import tokenize_file, clean_html_content

def tokenize_directory(input_dir: str, output_dir: str) -> bool:
    """
    Tokeniza todos los archivos HTML de un directorio
    
    Args:
        input_dir: Directorio con archivos HTML
        output_dir: Directorio para guardar tokens
        
    Returns:
        True si fue exitoso, False si hubo error
    """
    
    # Validar directorios
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Error: No se encuentra el directorio '{input_dir}'")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Obtener archivos HTML
    html_files = list(input_path.glob('*.html'))
    if not html_files:
        print(f"⚠️ No se encontraron archivos HTML en '{input_dir}'")
        return False
    
    print("=" * 60)
    print("TOKENIZACIÓN DE DOCUMENTOS")
    print("=" * 60)
    print(f"Directorio entrada: {input_dir}")
    print(f"Directorio salida: {output_dir}")
    print(f"Archivos a procesar: {len(html_files)}")
    print("=" * 60)
    
    # Procesar archivos
    success_count = 0
    error_count = 0
    all_tokens = {}
    total_tokens = 0
    
    for idx, html_file in enumerate(html_files, 1):
        try:
            # Leer archivo
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Limpiar y tokenizar
            clean_text = clean_html_content(content)
            tokens = tokenize_file(clean_text)
            
            # Guardar tokens
            all_tokens[html_file.name] = tokens
            total_tokens += len(tokens)
            
            success_count += 1
            
            if idx % 50 == 0:
                print(f"  Procesado: {idx}/{len(html_files)} archivos...")
        
        except Exception as e:
            print(f"  ❌ Error en {html_file.name}: {e}")
            error_count += 1
    
    # Guardar resultados
    output_file = output_path / "tokens.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_tokens, f, ensure_ascii=False, indent=2)
    
    # Guardar estadísticas
    stats_file = output_path / "tokenize_stats.txt"
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("ESTADÍSTICAS DE TOKENIZACIÓN\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Archivos procesados exitosamente: {success_count}\n")
        f.write(f"Archivos con errores: {error_count}\n")
        f.write(f"Total de tokens: {total_tokens:,}\n")
        f.write(f"Promedio de tokens por archivo: {total_tokens/success_count:.2f}\n")
        
        # Tokens únicos
        unique_tokens = set()
        for tokens in all_tokens.values():
            unique_tokens.update(tokens)
        
        f.write(f"Tokens únicos (vocabulario): {len(unique_tokens):,}\n")
        f.write(f"\nArchivos de salida:\n")
        f.write(f"  - tokens.json: {len(all_tokens)} documentos\n")
        f.write(f"  - tokenize_stats.txt: este archivo\n")
    
    # Resultado final
    print("\n" + "=" * 60)
    print("✓ TOKENIZACIÓN COMPLETADA")
    print("=" * 60)
    print(f"✓ Archivos procesados: {success_count}/{len(html_files)}")
    print(f"✓ Total de tokens: {total_tokens:,}")
    print(f"✓ Tokens únicos: {len(unique_tokens):,}")
    print(f"\n✓ Resultados guardados en: {output_dir}")
    print(f"  - tokens.json")
    print(f"  - tokenize_stats.txt")
    print("=" * 60)
    
    return error_count == 0

def main():
    """Función principal"""
    
    # Verificar argumentos
    if len(sys.argv) != 3:
        print("Uso: tokenize <input-dir> <output-dir>")
        print("\nEjemplo:")
        print("  tokenize data/input/Files data/output/tokens")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Ejecutar tokenización
    success = tokenize_directory(input_dir, output_dir)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
