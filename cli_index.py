#!/usr/bin/env python3
"""
CLI: Indexación de Documentos Tokenizados
==========================================

Comando para crear índice de posting lists desde línea de comandos.

Uso:
    index <input-dir> <output-dir>

Ejemplo:
    index data/output/tokens data/output/index
"""

import sys
from pathlib import Path
from typing import Dict, List
import json
from collections import defaultdict

# Agregar el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.activities.actividad7_posting_files import create_posting_list

def index_documents(input_dir: str, output_dir: str) -> bool:
    """
    Crea índice de posting lists desde documentos tokenizados
    
    Args:
        input_dir: Directorio con tokens.json
        output_dir: Directorio para guardar índice
        
    Returns:
        True si fue exitoso, False si hubo error
    """
    
    # Validar directorios
    input_path = Path(input_dir)
    tokens_file = input_path / "tokens.json"
    
    if not tokens_file.exists():
        print(f"❌ Error: No se encuentra el archivo '{tokens_file}'")
        print(f"   Asegúrate de ejecutar 'tokenize' primero.")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("INDEXACIÓN DE DOCUMENTOS")
    print("=" * 60)
    print(f"Archivo entrada: {tokens_file}")
    print(f"Directorio salida: {output_dir}")
    print("=" * 60)
    
    try:
        # Cargar tokens
        print("\n📂 Cargando tokens...")
        with open(tokens_file, 'r', encoding='utf-8') as f:
            all_documents = json.load(f)
        
        print(f"  ✓ Documentos cargados: {len(all_documents)}")
        
        # Crear posting list
        print("\n🔨 Creando posting list...")
        posting_list = create_posting_list(all_documents)
        
        print(f"  ✓ Tokens únicos indexados: {len(posting_list):,}")
        
        # Guardar posting list
        print("\n💾 Guardando índice...")
        
        # Formato 1: JSON completo
        posting_file_json = output_path / "posting_list.json"
        with open(posting_file_json, 'w', encoding='utf-8') as f:
            json.dump(posting_list, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ Guardado: posting_list.json")
        
        # Formato 2: Texto legible
        posting_file_txt = output_path / "posting_list.txt"
        with open(posting_file_txt, 'w', encoding='utf-8') as f:
            f.write("POSTING LIST - ÍNDICE INVERTIDO\n")
            f.write("=" * 80 + "\n\n")
            
            sorted_tokens = sorted(posting_list.keys())
            
            for token in sorted_tokens[:100]:  # Primeros 100 para el archivo
                docs = posting_list[token]
                f.write(f"{token}: [{', '.join(docs)}]\n")
            
            if len(sorted_tokens) > 100:
                f.write(f"\n... ({len(sorted_tokens) - 100} tokens más)\n")
        
        print(f"  ✓ Guardado: posting_list.txt (preview)")
        
        # Guardar estadísticas
        stats_file = output_path / "index_stats.txt"
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS DE INDEXACIÓN\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Documentos indexados: {len(all_documents)}\n")
            f.write(f"Tokens únicos (vocabulario): {len(posting_list):,}\n")
            
            # Calcular estadísticas de posting lists
            posting_lengths = [len(docs) for docs in posting_list.values()]
            avg_length = sum(posting_lengths) / len(posting_lengths)
            max_length = max(posting_lengths)
            
            f.write(f"\nEstadísticas de Posting Lists:\n")
            f.write(f"  - Promedio de documentos por token: {avg_length:.2f}\n")
            f.write(f"  - Máximo de documentos por token: {max_length}\n")
            
            # Encontrar token más frecuente
            most_common_token = max(posting_list.keys(), key=lambda t: len(posting_list[t]))
            f.write(f"  - Token más frecuente: '{most_common_token}' ({len(posting_list[most_common_token])} docs)\n")
            
            f.write(f"\nArchivos de salida:\n")
            f.write(f"  - posting_list.json: índice completo\n")
            f.write(f"  - posting_list.txt: preview del índice\n")
            f.write(f"  - index_stats.txt: este archivo\n")
        
        print(f"  ✓ Guardado: index_stats.txt")
        
        # Resultado final
        print("\n" + "=" * 60)
        print("✓ INDEXACIÓN COMPLETADA")
        print("=" * 60)
        print(f"✓ Documentos indexados: {len(all_documents)}")
        print(f"✓ Tokens únicos: {len(posting_list):,}")
        print(f"✓ Promedio de docs por token: {avg_length:.2f}")
        print(f"\n✓ Resultados guardados en: {output_dir}")
        print(f"  - posting_list.json")
        print(f"  - posting_list.txt")
        print(f"  - index_stats.txt")
        print("=" * 60)
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error durante la indexación: {e}")
        return False

def main():
    """Función principal"""
    
    # Verificar argumentos
    if len(sys.argv) != 3:
        print("Uso: index <input-dir> <output-dir>")
        print("\nEjemplo:")
        print("  index data/output/tokens data/output/index")
        print("\nNota: El directorio de entrada debe contener 'tokens.json'")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Ejecutar indexación
    success = index_documents(input_dir, output_dir)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
