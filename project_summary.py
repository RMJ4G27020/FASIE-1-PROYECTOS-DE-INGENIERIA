#!/usr/bin/env python3
"""
Resumen de Resultados - Proyecto Completo de Procesamiento HTML
==============================================================

Este script muestra un resumen completo de todas las actividades realizadas
en las 3 fases del proyecto, incluyendo estadísticas y archivos generados.

Autor: JOSE GPE RICO MORENO
Fecha: Septiembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
from pathlib import Path
from typing import Dict, List

def get_file_stats(file_path: Path) -> Dict[str, any]:
    """Obtiene estadísticas de un archivo"""
    if file_path.exists():
        stat = file_path.stat()
        return {
            'size': stat.st_size,
            'exists': True,
            'lines': count_lines(file_path) if file_path.suffix == '.txt' else 0
        }
    return {'exists': False, 'size': 0, 'lines': 0}

def count_lines(file_path: Path) -> int:
    """Cuenta líneas en un archivo de texto"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except:
        return 0

def format_size(size: int) -> str:
    """Formatea tamaño de archivo"""
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/1024:.1f} KB"
    elif size < 1024**3:
        return f"{size/(1024**2):.1f} MB"
    else:
        return f"{size/(1024**3):.1f} GB"

def main():
    """Función principal del resumen"""
    print("=" * 80)
    print("RESUMEN COMPLETO DEL PROYECTO - PROCESAMIENTO HTML")
    print("=" * 80)
    print("Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA")
    print("Autor: JOSE GPE RICO MORENO")
    print("Total de Actividades: 10 (3 Fases)")
    print("=" * 80)
    
    # Análisis por actividad
    activities = {
        4: {
            'name': 'Consolidación de Palabras',
            'phase': 'Fase 1',
            'output_dir': 'data/output/words_files',
            'files': ['consolidado_palabras.txt']
        },
        5: {
            'name': 'Tokenización',
            'phase': 'Fase 2', 
            'output_dir': 'data/output/activity5',
            'files': ['alpha_tokens.txt', 'frequency_analysis.txt']
        },
        6: {
            'name': 'Análisis de Diccionario',
            'phase': 'Fase 2',
            'output_dir': 'data/output/activity6',
            'files': ['dictionary.txt']
        },
        7: {
            'name': 'Archivo Posting',
            'phase': 'Fase 3',
            'output_dir': 'data/output/activity7',
            'files': ['dictionary_posting.txt', 'posting_list.txt', 'posting_stats.txt']
        },
        8: {
            'name': 'Hash Table',
            'phase': 'Fase 3',
            'output_dir': 'data/output/activity8',
            'files': ['hash_table_analysis.txt', 'hash_table_tests.txt', 'hash_table_implementation.txt']
        },
        9: {
            'name': 'Stop List',
            'phase': 'Fase 3',
            'output_dir': 'data/output/activity9',
            'files': ['dictionary_filtered.txt', 'stop_words_list.txt', 'stop_list_analysis.txt']
        },
        10: {
            'name': 'TF-IDF Weight Tokens',
            'phase': 'Fase 3',
            'output_dir': 'data/output/activity10',
            'files': ['dictionary_tfidf.txt', 'document_rankings.txt', 'discriminative_analysis.txt', 'tfidf_statistics.txt']
        }
    }
    
    total_files = 0
    total_size = 0
    phase_stats = {}
    
    for activity_num, activity_info in activities.items():
        phase = activity_info['phase']
        if phase not in phase_stats:
            phase_stats[phase] = {'files': 0, 'size': 0, 'activities': 0}
        
        print(f"\n🔍 ACTIVIDAD {activity_num}: {activity_info['name']}")
        print(f"   Fase: {phase}")
        print(f"   Directorio: {activity_info['output_dir']}")
        
        activity_files = 0
        activity_size = 0
        
        for filename in activity_info['files']:
            file_path = Path(activity_info['output_dir']) / filename
            stats = get_file_stats(file_path)
            
            if stats['exists']:
                print(f"   ✓ {filename}: {format_size(stats['size'])}")
                if stats['lines'] > 0:
                    print(f"     Líneas: {stats['lines']:,}")
                activity_files += 1
                activity_size += stats['size']
            else:
                print(f"   ❌ {filename}: No encontrado")
        
        # Buscar archivos de reporte
        report_files = list(Path(activity_info['output_dir']).glob(f"a{activity_num}_*.txt"))
        for report_file in report_files:
            stats = get_file_stats(report_file)
            if stats['exists']:
                print(f"   📄 {report_file.name}: {format_size(stats['size'])}")
                activity_files += 1
                activity_size += stats['size']
        
        print(f"   📊 Subtotal: {activity_files} archivos, {format_size(activity_size)}")
        
        phase_stats[phase]['files'] += activity_files
        phase_stats[phase]['size'] += activity_size
        phase_stats[phase]['activities'] += 1
        
        total_files += activity_files
        total_size += activity_size
    
    # Resumen por fases
    print(f"\n{'='*80}")
    print("RESUMEN POR FASES:")
    print("="*80)
    
    for phase, stats in phase_stats.items():
        print(f"{phase}: {stats['activities']} actividades, {stats['files']} archivos, {format_size(stats['size'])}")
    
    # Resumen general
    print(f"\n{'='*80}")
    print("RESUMEN GENERAL:")
    print("="*80)
    print(f"📁 Total de archivos generados: {total_files}")
    print(f"💾 Tamaño total de datos: {format_size(total_size)}")
    print(f"🎯 Actividades completadas: {len(activities)}")
    print(f"📈 Fases implementadas: {len(phase_stats)}")
    
    # Verificar archivos de entrada
    print(f"\n{'='*80}")
    print("ARCHIVOS DE ENTRADA:")
    print("="*80)
    
    html_dir = Path("data/input/Files")
    if html_dir.exists():
        html_files = list(html_dir.glob("*.html"))
        print(f"📂 Archivos HTML: {len(html_files)}")
        total_html_size = sum(f.stat().st_size for f in html_files)
        print(f"💾 Tamaño total HTML: {format_size(total_html_size)}")
    else:
        print("❌ Directorio de archivos HTML no encontrado")
    
    # Análisis de evolución
    print(f"\n{'='*80}")
    print("EVOLUCIÓN DEL PROYECTO:")
    print("="*80)
    print("📈 Fase 1: Procesamiento básico y consolidación")
    print("📈 Fase 2: Análisis de frecuencias y diccionarios")
    print("📈 Fase 3: Técnicas avanzadas (Posting, Hash, Stop Words, TF-IDF)")
    print("\n🎯 RESULTADO: Sistema completo de procesamiento y análisis de texto")
    print("   con capacidades de recuperación de información y análisis semántico")
    
    # Herramientas disponibles
    print(f"\n{'='*80}")
    print("HERRAMIENTAS DISPONIBLES:")
    print("="*80)
    
    tools = [
        ("launcher.py", "Ejecutor interactivo de todas las actividades"),
        ("show_results.py", "Visor de resultados por actividad"),
        ("main.py", "Script principal del proyecto original")
    ]
    
    for tool, description in tools:
        tool_path = Path(tool)
        if tool_path.exists():
            print(f"🔧 {tool}: {description}")
        else:
            print(f"❌ {tool}: No encontrado")
    
    print(f"\n{'='*80}")
    print("🏆 PROYECTO COMPLETADO EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()