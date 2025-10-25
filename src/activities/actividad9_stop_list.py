#!/usr/bin/env python3
"""
Actividad 9: Stop List (Fase 3: Weight Tokens)
==============================================

Este módulo implementa la eliminación de palabras comunes (stop words) para:
1. Refinar el diccionario eliminando términos irrelevantes
2. Crear lista personalizada de stop words basada en frecuencia
3. Generar diccionario limpio sin palabras comunes
4. Análisis comparativo antes y después de la limpieza

Autor: JOSE GPE RICO MORENO
Fecha: Septiembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import Counter

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA

class StopListProcessor:
    """Procesador de stop words para limpieza de diccionario"""
    
    def __init__(self, output_dir: str):
        """
        Inicializa el procesador de stop list
        
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Stop words predefinidas (inglés y español)
        self.predefined_stopwords = {
            # Inglés
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
            'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
            'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
            'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
            'one', 'all', 'would', 'there', 'their', 'what', 'so',
            'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
            'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just',
            'him', 'know', 'take', 'people', 'into', 'year', 'your',
            'good', 'some', 'could', 'them', 'see', 'other', 'than',
            'then', 'now', 'look', 'only', 'come', 'its', 'over',
            'think', 'also', 'back', 'after', 'use', 'two', 'how',
            'our', 'work', 'first', 'well', 'way', 'even', 'new',
            'want', 'because', 'any', 'these', 'give', 'day', 'most',
            'us', 'is', 'was', 'are', 'been', 'has', 'had', 'were',
            
            # Español básico
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se',
            'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con',
            'para', 'al', 'del', 'los', 'las', 'una', 'pero', 'sus',
            'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están',
            'estado', 'desde', 'todo', 'nos', 'durante', 'todos',
            'uno', 'les', 'ni', 'contra', 'otros', 'fueron', 'ese',
            'eso', 'había', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes',
            'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra',
            
            # Palabras técnicas comunes
            'com', 'org', 'net', 'edu', 'gov', 'www', 'http', 'https',
            'html', 'htm', 'asp', 'php', 'jsp', 'xml', 'css', 'js',
            'pdf', 'doc', 'txt', 'gif', 'jpg', 'jpeg', 'png', 'img',
            
            # Palabras muy cortas (menos de 3 caracteres)
            'a', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'i',
            'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or',
            'so', 'to', 'up', 'us', 'we'
        }
        
        # Estadísticas
        self.original_count = 0
        self.filtered_count = 0
        self.removed_tokens = set()
        
    def load_dictionary_data(self, dict_file: str) -> Dict[str, Dict[str, Any]]:
        """
        Carga datos del diccionario desde archivo
        
        Args:
            dict_file: Archivo de diccionario
            
        Returns:
            Diccionario de tokens
        """
        dictionary_data = {}
        dict_path = Path(dict_file)
        
        if not dict_path.exists():
            print(f"❌ No se encontró el archivo: {dict_file}")
            return dictionary_data
        
        print(f"Cargando diccionario desde: {dict_file}")
        
        with open(dict_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar encabezado
        for line in lines[2:]:  # Saltar líneas de encabezado
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    token = parts[0]
                    try:
                        repetitions = int(parts[1])
                        documents = int(parts[2])
                        dictionary_data[token] = {
                            'repetitions': repetitions,
                            'documents': documents
                        }
                    except ValueError:
                        continue
        
        self.original_count = len(dictionary_data)
        print(f"✓ Cargados {self.original_count:,} tokens del diccionario")
        return dictionary_data
    
    def generate_frequency_based_stopwords(self, dictionary_data: Dict[str, Dict[str, Any]], 
                                         top_n: int = 100) -> Set[str]:
        """
        Genera stop words basadas en frecuencia
        
        Args:
            dictionary_data: Datos del diccionario
            top_n: Número de tokens más frecuentes a considerar
            
        Returns:
            Set de stop words basadas en frecuencia
        """
        print(f"Generando stop words basadas en los {top_n} tokens más frecuentes...")
        
        # Ordenar por frecuencia descendente
        frequency_sorted = sorted(
            dictionary_data.items(),
            key=lambda x: x[1]['repetitions'],
            reverse=True
        )
        
        frequency_stopwords = set()
        
        # Analizar los más frecuentes
        for i, (token, data) in enumerate(frequency_sorted[:top_n]):
            # Criterios para considerar como stop word:
            # 1. Aparece en más del 70% de los documentos
            # 2. Es muy corto (1-2 caracteres)
            # 3. Es muy común (top 50 más frecuentes)
            
            doc_ratio = data['documents'] / 506  # Total de documentos
            
            if (doc_ratio > 0.7 or  # Aparece en más del 70% de documentos
                len(token) <= 2 or  # Muy corto
                i < 50):  # Top 50 más frecuentes
                frequency_stopwords.add(token)
        
        print(f"✓ Generadas {len(frequency_stopwords)} stop words basadas en frecuencia")
        return frequency_stopwords
    
    def generate_pattern_based_stopwords(self, dictionary_data: Dict[str, Dict[str, Any]]) -> Set[str]:
        """
        Genera stop words basadas en patrones
        
        Args:
            dictionary_data: Datos del diccionario
            
        Returns:
            Set de stop words basadas en patrones
        """
        print("Generando stop words basadas en patrones...")
        
        pattern_stopwords = set()
        
        for token in dictionary_data.keys():
            # Patrones a filtrar:
            
            # 1. Números puros
            if re.match(r'^\d+$', token):
                pattern_stopwords.add(token)
            
            # 2. URLs y dominios
            elif any(domain in token for domain in ['com', 'org', 'net', 'edu', 'gov']):
                if '.' in token or len(token) < 4:
                    pattern_stopwords.add(token)
            
            # 3. Extensiones de archivo
            elif token in ['html', 'htm', 'php', 'asp', 'jsp', 'pdf', 'doc', 'txt']:
                pattern_stopwords.add(token)
            
            # 4. Caracteres especiales o codificación
            elif not re.match(r'^[a-zA-Z]+$', token):
                if len(token) < 3 or any(char in token for char in ['&', '#', '%', '_']):
                    pattern_stopwords.add(token)
            
            # 5. Palabras muy largas (probablemente basura)
            elif len(token) > 20:
                pattern_stopwords.add(token)
            
            # 6. Repeticiones de caracteres
            elif re.match(r'^(.)\1{3,}$', token):  # aaaa, bbbb, etc.
                pattern_stopwords.add(token)
        
        print(f"✓ Generadas {len(pattern_stopwords)} stop words basadas en patrones")
        return pattern_stopwords
    
    def create_comprehensive_stoplist(self, dictionary_data: Dict[str, Dict[str, Any]]) -> Set[str]:
        """
        Crea lista completa de stop words
        
        Args:
            dictionary_data: Datos del diccionario
            
        Returns:
            Set completo de stop words
        """
        print("Creando lista comprehensiva de stop words...")
        
        # Combinar todas las fuentes
        comprehensive_stoplist = set(self.predefined_stopwords)
        
        # Agregar basadas en frecuencia
        frequency_stops = self.generate_frequency_based_stopwords(dictionary_data)
        comprehensive_stoplist.update(frequency_stops)
        
        # Agregar basadas en patrones
        pattern_stops = self.generate_pattern_based_stopwords(dictionary_data)
        comprehensive_stoplist.update(pattern_stops)
        
        # Filtrar solo tokens que existen en el diccionario
        existing_stopwords = comprehensive_stoplist.intersection(dictionary_data.keys())
        
        print(f"✓ Lista comprehensiva creada: {len(existing_stopwords)} stop words")
        return existing_stopwords
    
    def filter_dictionary(self, dictionary_data: Dict[str, Dict[str, Any]], 
                         stopwords: Set[str]) -> Dict[str, Dict[str, Any]]:
        """
        Filtra el diccionario removiendo stop words
        
        Args:
            dictionary_data: Diccionario original
            stopwords: Stop words a remover
            
        Returns:
            Diccionario filtrado
        """
        print("Filtrando diccionario...")
        
        filtered_dict = {}
        removed_count = 0
        
        for token, data in dictionary_data.items():
            if token not in stopwords:
                filtered_dict[token] = data
            else:
                removed_count += 1
                self.removed_tokens.add(token)
        
        self.filtered_count = len(filtered_dict)
        
        print(f"✓ Diccionario filtrado: {removed_count:,} tokens removidos")
        print(f"✓ Tokens restantes: {self.filtered_count:,}")
        
        return filtered_dict
    
    def save_stopwords_list(self, stopwords: Set[str]) -> Path:
        """
        Guarda la lista de stop words
        
        Args:
            stopwords: Set de stop words
            
        Returns:
            Path del archivo guardado
        """
        stoplist_file = self.output_dir / "stop_words_list.txt"
        
        print("Guardando lista de stop words...")
        
        with open(stoplist_file, 'w', encoding='utf-8') as f:
            f.write("LISTA DE STOP WORDS - ACTIVIDAD 9\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total de stop words: {len(stopwords)}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Categorizar stop words
            categories = {
                'predefined': set(),
                'frequency': set(),
                'pattern': set(),
                'technical': set()
            }
            
            for word in stopwords:
                if word in self.predefined_stopwords:
                    categories['predefined'].add(word)
                elif any(tech in word for tech in ['com', 'org', 'net', 'edu', 'www']):
                    categories['technical'].add(word)
                elif len(word) <= 2 or word.isdigit():
                    categories['pattern'].add(word)
                else:
                    categories['frequency'].add(word)
            
            for category, words in categories.items():
                if words:
                    f.write(f"{category.upper()} ({len(words)} palabras):\n")
                    f.write("-" * 30 + "\n")
                    sorted_words = sorted(words)
                    for i, word in enumerate(sorted_words):
                        f.write(f"{word}")
                        if (i + 1) % 10 == 0:
                            f.write("\n")
                        else:
                            f.write(", " if i < len(sorted_words) - 1 else "\n")
                    f.write("\n\n")
        
        print(f"✓ Lista de stop words guardada: {stoplist_file}")
        return stoplist_file
    
    def save_filtered_dictionary(self, filtered_dict: Dict[str, Dict[str, Any]]) -> Path:
        """
        Guarda el diccionario filtrado
        
        Args:
            filtered_dict: Diccionario sin stop words
            
        Returns:
            Path del archivo guardado
        """
        filtered_file = self.output_dir / "dictionary_filtered.txt"
        
        print("Guardando diccionario filtrado...")
        
        with open(filtered_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("Token\tRepeticiones\t#Documentos\n")
            f.write("-" * 50 + "\n")
            
            # Datos ordenados alfabéticamente
            for token in sorted(filtered_dict.keys()):
                data = filtered_dict[token]
                f.write(f"{token}\t{data['repetitions']}\t{data['documents']}\n")
        
        print(f"✓ Diccionario filtrado guardado: {filtered_file}")
        return filtered_file
    
    def generate_comparison_analysis(self, original_dict: Dict[str, Dict[str, Any]], 
                                   filtered_dict: Dict[str, Dict[str, Any]], 
                                   stopwords: Set[str]) -> Path:
        """
        Genera análisis comparativo
        
        Args:
            original_dict: Diccionario original
            filtered_dict: Diccionario filtrado
            stopwords: Stop words utilizadas
            
        Returns:
            Path del archivo de análisis
        """
        analysis_file = self.output_dir / "stop_list_analysis.txt"
        
        print("Generando análisis comparativo...")
        
        # Calcular estadísticas
        original_total_freq = sum(data['repetitions'] for data in original_dict.values())
        filtered_total_freq = sum(data['repetitions'] for data in filtered_dict.values())
        removed_freq = original_total_freq - filtered_total_freq
        
        # Top tokens removidos
        removed_tokens_data = [(token, original_dict[token]) for token in stopwords 
                              if token in original_dict]
        removed_sorted = sorted(removed_tokens_data, 
                               key=lambda x: x[1]['repetitions'], reverse=True)
        
        # Top tokens restantes
        filtered_sorted = sorted(filtered_dict.items(), 
                               key=lambda x: x[1]['repetitions'], reverse=True)
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write("ANÁLISIS COMPARATIVO - STOP LIST\n")
            f.write("=" * 60 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("ESTADÍSTICAS GENERALES:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Tokens originales: {len(original_dict):,}\n")
            f.write(f"Tokens filtrados: {len(filtered_dict):,}\n")
            f.write(f"Tokens removidos: {len(stopwords):,}\n")
            f.write(f"Porcentaje removido: {len(stopwords)/len(original_dict)*100:.1f}%\n")
            f.write("\n")
            
            f.write("ESTADÍSTICAS DE FRECUENCIA:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Frecuencia total original: {original_total_freq:,}\n")
            f.write(f"Frecuencia total filtrada: {filtered_total_freq:,}\n")
            f.write(f"Frecuencia removida: {removed_freq:,}\n")
            f.write(f"Porcentaje de frecuencia removida: {removed_freq/original_total_freq*100:.1f}%\n")
            f.write("\n")
            
            f.write("TOP 20 TOKENS REMOVIDOS (MÁS FRECUENTES):\n")
            f.write("-" * 40 + "\n")
            for i, (token, data) in enumerate(removed_sorted[:20], 1):
                f.write(f"{i:2d}. {token}: {data['repetitions']:,} veces "
                       f"({data['documents']} docs)\n")
            f.write("\n")
            
            f.write("TOP 20 TOKENS RESTANTES (MÁS FRECUENTES):\n")
            f.write("-" * 40 + "\n")
            for i, (token, data) in enumerate(filtered_sorted[:20], 1):
                f.write(f"{i:2d}. {token}: {data['repetitions']:,} veces "
                       f"({data['documents']} docs)\n")
            f.write("\n")
            
            # Distribución por categorías
            f.write("IMPACTO POR CATEGORÍAS:\n")
            f.write("-" * 40 + "\n")
            
            categories = {
                'Muy frecuentes (>1000)': 0,
                'Frecuentes (100-1000)': 0,
                'Moderados (10-100)': 0,
                'Raros (<10)': 0
            }
            
            for token in stopwords:
                if token in original_dict:
                    freq = original_dict[token]['repetitions']
                    if freq > 1000:
                        categories['Muy frecuentes (>1000)'] += 1
                    elif freq > 100:
                        categories['Frecuentes (100-1000)'] += 1
                    elif freq > 10:
                        categories['Moderados (10-100)'] += 1
                    else:
                        categories['Raros (<10)'] += 1
            
            for category, count in categories.items():
                f.write(f"{category}: {count} tokens\n")
        
        print(f"✓ Análisis comparativo generado: {analysis_file}")
        return analysis_file
    
    def generate_report(self, processing_time: float) -> Path:
        """
        Genera reporte académico de la actividad
        
        Args:
            processing_time: Tiempo de procesamiento
            
        Returns:
            Path del archivo de reporte
        """
        report_file = self.output_dir / f"a9_{MATRICULA}.txt"
        
        reduction_percentage = ((self.original_count - self.filtered_count) / 
                               self.original_count * 100)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE ACADÉMICO - ACTIVIDAD 9: STOP LIST\n")
            f.write("=" * 60 + "\n")
            f.write(f"Matrícula: {MATRICULA}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Actividad: Filtrado de Stop Words\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("METODOLOGÍA IMPLEMENTADA:\n")
            f.write("-" * 40 + "\n")
            f.write("• Stop words predefinidas (inglés/español)\n")
            f.write("• Stop words basadas en frecuencia y distribución\n")
            f.write("• Stop words basadas en patrones y características\n")
            f.write("• Filtrado de tokens técnicos y basura\n")
            f.write("• Análisis comparativo antes/después\n")
            f.write("\n")
            
            f.write("RESULTADOS DEL PROCESAMIENTO:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Tokens originales: {self.original_count:,}\n")
            f.write(f"Tokens filtrados: {self.filtered_count:,}\n")
            f.write(f"Tokens removidos: {len(self.removed_tokens):,}\n")
            f.write(f"Reducción: {reduction_percentage:.1f}%\n")
            f.write(f"Tiempo de procesamiento: {processing_time:.3f} segundos\n")
            f.write("\n")
            
            f.write("BENEFICIOS OBTENIDOS:\n")
            f.write("-" * 40 + "\n")
            f.write("• Diccionario más limpio y relevante\n")
            f.write("• Eliminación de ruido y términos irrelevantes\n")
            f.write("• Mejor calidad para análisis posteriores\n")
            f.write("• Reducción significativa de tamaño\n")
            f.write("• Base optimizada para TF-IDF\n")
            f.write("\n")
            
            f.write("ARCHIVOS GENERADOS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. stop_words_list.txt - Lista completa de stop words\n")
            f.write("2. dictionary_filtered.txt - Diccionario limpio\n")
            f.write("3. stop_list_analysis.txt - Análisis comparativo\n")
            f.write("4. a9_matricula.txt - Este reporte académico\n")
        
        print(f"✓ Reporte académico generado: {report_file}")
        return report_file


def main():
    """Función principal de la Actividad 9"""
    start_time = time.time()
    
    print("=" * 60)
    print("ACTIVIDAD 9: STOP LIST")
    print("Fase 3: Weight Tokens")
    print("=" * 60)
    
    # Configurar directorios
    if len(sys.argv) > 2:
        dict_file = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        dict_file = "data/output/activity7/dictionary_posting.txt"
        output_dir = "data/output/activity9"
    
    try:
        # Crear procesador
        processor = StopListProcessor(output_dir)
        
        # Cargar datos del diccionario
        original_dict = processor.load_dictionary_data(dict_file)
        
        if not original_dict:
            print("❌ No se pudieron cargar datos del diccionario")
            return 1
        
        # Crear lista comprehensiva de stop words
        stopwords = processor.create_comprehensive_stoplist(original_dict)
        
        # Filtrar diccionario
        filtered_dict = processor.filter_dictionary(original_dict, stopwords)
        
        # Guardar archivos
        stoplist_file = processor.save_stopwords_list(stopwords)
        filtered_file = processor.save_filtered_dictionary(filtered_dict)
        analysis_file = processor.generate_comparison_analysis(
            original_dict, filtered_dict, stopwords
        )
        
        # Calcular tiempo total
        processing_time = time.time() - start_time
        
        # Generar reporte académico
        report_file = processor.generate_report(processing_time)
        
        print("\n" + "=" * 60)
        print("ACTIVIDAD 9 COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print(f"Tiempo total: {processing_time:.3f} segundos")
        print(f"Tokens originales: {processor.original_count:,}")
        print(f"Tokens filtrados: {processor.filtered_count:,}")
        print(f"Reducción: {((processor.original_count - processor.filtered_count)/processor.original_count*100):.1f}%")
        print(f"Archivos generados en: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error en Actividad 9: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())