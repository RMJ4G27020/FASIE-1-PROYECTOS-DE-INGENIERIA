#!/usr/bin/env python3
"""
Actividad 10: Weight Tokens - TF-IDF (Fase 3: Weight Tokens)
============================================================

Este módulo implementa el cálculo de pesos TF-IDF para:
1. Calcular Term Frequency (TF) para cada token en cada documento
2. Calcular Inverse Document Frequency (IDF) para cada token
3. Combinar TF-IDF para obtener pesos de relevancia
4. Generar ranking de documentos más relevantes por token
5. Análisis de tokens más discriminativos

Autor: JOSE GPE RICO MORENO
Fecha: Septiembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set
from collections import defaultdict, Counter

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA

class TFIDFCalculator:
    """Calculadora de pesos TF-IDF para tokens"""
    
    def __init__(self, html_dir: str, output_dir: str):
        """
        Inicializa el calculador TF-IDF
        
        Args:
            html_dir: Directorio con archivos HTML
            output_dir: Directorio de salida
        """
        self.html_dir = Path(html_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Estructuras de datos
        self.document_tokens = {}  # doc_id -> {token: freq}
        self.token_documents = defaultdict(set)  # token -> {doc_ids}
        self.total_documents = 0
        self.filtered_tokens = set()  # Tokens del diccionario filtrado
        
        # Estadísticas TF-IDF
        self.tf_scores = {}     # doc_id -> {token: tf_score}
        self.idf_scores = {}    # token -> idf_score
        self.tfidf_scores = {}  # doc_id -> {token: tfidf_score}
        
    def load_filtered_dictionary(self, dict_file: str) -> Set[str]:
        """
        Carga tokens del diccionario filtrado
        
        Args:
            dict_file: Archivo de diccionario filtrado
            
        Returns:
            Set de tokens filtrados
        """
        dict_path = Path(dict_file)
        
        if not dict_path.exists():
            print(f"❌ No se encontró el archivo: {dict_file}")
            return set()
        
        print(f"Cargando diccionario filtrado desde: {dict_file}")
        
        filtered_tokens = set()
        with open(dict_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar encabezado
        for line in lines[2:]:  # Saltar líneas de encabezado
            line = line.strip()
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 1:
                    token = parts[0]
                    filtered_tokens.add(token)
        
        self.filtered_tokens = filtered_tokens
        print(f"✓ Cargados {len(filtered_tokens)} tokens filtrados")
        return filtered_tokens
    
    def clean_html_content(self, html_content: str) -> str:
        """Limpia contenido HTML y extrae texto"""
        # Remover etiquetas HTML
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # Remover caracteres especiales y normalizar espacios
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def extract_tokens(self, text: str) -> List[str]:
        """Extrae tokens alfabéticos del texto"""
        tokens = re.findall(r'[a-zA-Z]+', text)
        return [token.lower() for token in tokens if len(token) >= 2]
    
    def process_documents(self) -> None:
        """Procesa todos los documentos HTML"""
        html_files = sorted([f for f in self.html_dir.glob('*.html')])
        self.total_documents = len(html_files)
        
        print(f"Procesando {self.total_documents} documentos para TF-IDF...")
        
        for i, html_file in enumerate(html_files, 1):
            if i % 50 == 0:
                print(f"  Procesado: {i}/{self.total_documents} documentos")
            
            try:
                # Leer archivo HTML
                content = self._read_html_file(html_file)
                
                # Limpiar y extraer tokens
                clean_text = self.clean_html_content(content)
                tokens = self.extract_tokens(clean_text)
                
                # Filtrar solo tokens del diccionario filtrado
                filtered_tokens = [token for token in tokens if token in self.filtered_tokens]
                
                # Contar frecuencias
                token_counts = Counter(filtered_tokens)
                doc_id = html_file.stem  # nombre sin extensión
                
                # Almacenar datos
                self.document_tokens[doc_id] = dict(token_counts)
                
                # Actualizar índice inverso
                for token in token_counts.keys():
                    self.token_documents[token].add(doc_id)
                    
            except Exception as e:
                print(f"Error procesando {html_file.name}: {e}")
                continue
        
        print(f"✓ Procesamiento completado: {len(self.document_tokens)} documentos")
    
    def _read_html_file(self, file_path: Path) -> str:
        """Lee archivo HTML con manejo robusto de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # Si falla todo, usar errors='ignore'
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def calculate_tf_scores(self) -> None:
        """Calcula scores TF (Term Frequency) para todos los documentos"""
        print("Calculando scores TF (Term Frequency)...")
        
        for doc_id, token_counts in self.document_tokens.items():
            total_tokens = sum(token_counts.values())
            
            if total_tokens > 0:
                tf_scores = {}
                for token, count in token_counts.items():
                    # TF = (frecuencia del término) / (total de términos en el documento)
                    tf_scores[token] = count / total_tokens
                
                self.tf_scores[doc_id] = tf_scores
        
        print(f"✓ Calculados scores TF para {len(self.tf_scores)} documentos")
    
    def calculate_idf_scores(self) -> None:
        """Calcula scores IDF (Inverse Document Frequency) para todos los tokens"""
        print("Calculando scores IDF (Inverse Document Frequency)...")
        
        for token in self.filtered_tokens:
            # Número de documentos que contienen el token
            docs_with_token = len(self.token_documents[token])
            
            if docs_with_token > 0:
                # IDF = log(total_documentos / documentos_con_término)
                self.idf_scores[token] = math.log(self.total_documents / docs_with_token)
            else:
                self.idf_scores[token] = 0
        
        print(f"✓ Calculados scores IDF para {len(self.idf_scores)} tokens")
    
    def calculate_tfidf_scores(self) -> None:
        """Calcula scores TF-IDF combinando TF e IDF"""
        print("Calculando scores TF-IDF...")
        
        for doc_id in self.document_tokens.keys():
            tfidf_scores = {}
            
            if doc_id in self.tf_scores:
                for token, tf_score in self.tf_scores[doc_id].items():
                    if token in self.idf_scores:
                        # TF-IDF = TF * IDF
                        tfidf_scores[token] = tf_score * self.idf_scores[token]
                
                self.tfidf_scores[doc_id] = tfidf_scores
        
        print(f"✓ Calculados scores TF-IDF para {len(self.tfidf_scores)} documentos")
    
    def generate_tfidf_dictionary(self) -> Path:
        """Genera diccionario con pesos TF-IDF en lugar de frecuencias"""
        tfidf_dict_file = self.output_dir / "dictionary_tfidf.txt"
        
        print("Generando diccionario con pesos TF-IDF...")
        
        # Calcular estadísticas TF-IDF por token
        token_tfidf_stats = {}
        
        for token in self.filtered_tokens:
            tfidf_values = []
            documents_with_token = 0
            
            for doc_id, doc_tfidf in self.tfidf_scores.items():
                if token in doc_tfidf:
                    tfidf_values.append(doc_tfidf[token])
                    documents_with_token += 1
            
            if tfidf_values:
                token_tfidf_stats[token] = {
                    'max_tfidf': max(tfidf_values),
                    'avg_tfidf': sum(tfidf_values) / len(tfidf_values),
                    'total_tfidf': sum(tfidf_values),
                    'documents': documents_with_token,
                    'idf': self.idf_scores.get(token, 0)
                }
        
        with open(tfidf_dict_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("Token\tMax_TF-IDF\tAvg_TF-IDF\tTotal_TF-IDF\t#Documentos\tIDF\n")
            f.write("-" * 80 + "\n")
            
            # Ordenar por TF-IDF total descendente
            sorted_tokens = sorted(
                token_tfidf_stats.items(),
                key=lambda x: x[1]['total_tfidf'],
                reverse=True
            )
            
            for token, stats in sorted_tokens:
                f.write(f"{token}\t{stats['max_tfidf']:.6f}\t{stats['avg_tfidf']:.6f}\t"
                       f"{stats['total_tfidf']:.6f}\t{stats['documents']}\t{stats['idf']:.6f}\n")
        
        print(f"✓ Diccionario TF-IDF generado: {tfidf_dict_file}")
        return tfidf_dict_file
    
    def generate_document_rankings(self) -> Path:
        """Genera rankings de documentos más relevantes por token"""
        rankings_file = self.output_dir / "document_rankings.txt"
        
        print("Generando rankings de documentos por token...")
        
        with open(rankings_file, 'w', encoding='utf-8') as f:
            f.write("RANKINGS DE DOCUMENTOS POR TOKEN (TF-IDF)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total de tokens analizados: {len(self.filtered_tokens)}\n")
            f.write(f"Total de documentos: {self.total_documents}\n")
            f.write("=" * 80 + "\n\n")
            
            # Seleccionar top tokens por IDF (más discriminativos)
            top_tokens = sorted(
                self.idf_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:50]  # Top 50 tokens más discriminativos
            
            for token, idf_score in top_tokens:
                f.write(f"TOKEN: {token} (IDF: {idf_score:.4f})\n")
                f.write("-" * 60 + "\n")
                
                # Obtener documentos con este token y sus scores TF-IDF
                doc_scores = []
                for doc_id, doc_tfidf in self.tfidf_scores.items():
                    if token in doc_tfidf:
                        doc_scores.append((doc_id, doc_tfidf[token]))
                
                # Ordenar por TF-IDF descendente
                doc_scores.sort(key=lambda x: x[1], reverse=True)
                
                f.write(f"Aparece en {len(doc_scores)} documentos:\n")
                
                # Mostrar top 10 documentos más relevantes
                for i, (doc_id, tfidf_score) in enumerate(doc_scores[:10], 1):
                    tf_score = self.tf_scores.get(doc_id, {}).get(token, 0)
                    f.write(f"  {i:2d}. {doc_id}: TF-IDF={tfidf_score:.6f} "
                           f"(TF={tf_score:.6f})\n")
                
                f.write("\n")
        
        print(f"✓ Rankings de documentos generados: {rankings_file}")
        return rankings_file
    
    def generate_discriminative_analysis(self) -> Path:
        """Genera análisis de tokens más discriminativos"""
        analysis_file = self.output_dir / "discriminative_analysis.txt"
        
        print("Generando análisis de tokens discriminativos...")
        
        # Calcular diferentes métricas de discriminación
        discrimination_metrics = {}
        
        for token in self.filtered_tokens:
            if token in self.idf_scores and len(self.token_documents[token]) > 0:
                idf = self.idf_scores[token]
                doc_freq = len(self.token_documents[token])
                doc_ratio = doc_freq / self.total_documents
                
                # Obtener valores TF-IDF para este token
                tfidf_values = []
                for doc_id, doc_tfidf in self.tfidf_scores.items():
                    if token in doc_tfidf:
                        tfidf_values.append(doc_tfidf[token])
                
                if tfidf_values:
                    max_tfidf = max(tfidf_values)
                    avg_tfidf = sum(tfidf_values) / len(tfidf_values)
                    variance = sum((x - avg_tfidf) ** 2 for x in tfidf_values) / len(tfidf_values)
                    
                    discrimination_metrics[token] = {
                        'idf': idf,
                        'doc_freq': doc_freq,
                        'doc_ratio': doc_ratio,
                        'max_tfidf': max_tfidf,
                        'avg_tfidf': avg_tfidf,
                        'variance': variance,
                        'discrimination_score': idf * (1 - doc_ratio) * max_tfidf
                    }
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write("ANÁLISIS DE TOKENS DISCRIMINATIVOS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Top tokens por IDF
            f.write("TOP 20 TOKENS POR IDF (MÁS RAROS):\n")
            f.write("-" * 50 + "\n")
            top_idf = sorted(discrimination_metrics.items(), 
                           key=lambda x: x[1]['idf'], reverse=True)[:20]
            
            for i, (token, metrics) in enumerate(top_idf, 1):
                f.write(f"{i:2d}. {token}: IDF={metrics['idf']:.4f} "
                       f"({metrics['doc_freq']} docs, {metrics['doc_ratio']:.1%})\n")
            
            f.write("\n")
            
            # Top tokens por TF-IDF máximo
            f.write("TOP 20 TOKENS POR TF-IDF MÁXIMO:\n")
            f.write("-" * 50 + "\n")
            top_tfidf = sorted(discrimination_metrics.items(), 
                             key=lambda x: x[1]['max_tfidf'], reverse=True)[:20]
            
            for i, (token, metrics) in enumerate(top_tfidf, 1):
                f.write(f"{i:2d}. {token}: Max_TF-IDF={metrics['max_tfidf']:.6f} "
                       f"(IDF={metrics['idf']:.4f})\n")
            
            f.write("\n")
            
            # Top tokens por score de discriminación
            f.write("TOP 20 TOKENS MÁS DISCRIMINATIVOS:\n")
            f.write("-" * 50 + "\n")
            top_discriminative = sorted(discrimination_metrics.items(), 
                                      key=lambda x: x[1]['discrimination_score'], 
                                      reverse=True)[:20]
            
            for i, (token, metrics) in enumerate(top_discriminative, 1):
                f.write(f"{i:2d}. {token}: Score={metrics['discrimination_score']:.6f} "
                       f"(IDF={metrics['idf']:.4f}, Max_TF-IDF={metrics['max_tfidf']:.6f})\n")
            
            f.write("\n")
            
            # Estadísticas generales
            f.write("ESTADÍSTICAS GENERALES:\n")
            f.write("-" * 50 + "\n")
            all_idfs = [m['idf'] for m in discrimination_metrics.values()]
            all_tfidf_max = [m['max_tfidf'] for m in discrimination_metrics.values()]
            
            f.write(f"Tokens analizados: {len(discrimination_metrics)}\n")
            f.write(f"IDF promedio: {sum(all_idfs)/len(all_idfs):.4f}\n")
            f.write(f"IDF máximo: {max(all_idfs):.4f}\n")
            f.write(f"TF-IDF máximo promedio: {sum(all_tfidf_max)/len(all_tfidf_max):.6f}\n")
            f.write(f"TF-IDF máximo global: {max(all_tfidf_max):.6f}\n")
        
        print(f"✓ Análisis discriminativo generado: {analysis_file}")
        return analysis_file
    
    def generate_report(self, processing_time: float) -> Path:
        """
        Genera reporte académico de la actividad
        
        Args:
            processing_time: Tiempo de procesamiento
            
        Returns:
            Path del archivo de reporte
        """
        report_file = self.output_dir / f"a10_{MATRICULA}.txt"
        
        # Calcular estadísticas
        total_tf_calculations = sum(len(tf_dict) for tf_dict in self.tf_scores.values())
        total_tfidf_calculations = sum(len(tfidf_dict) for tfidf_dict in self.tfidf_scores.values())
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE ACADÉMICO - ACTIVIDAD 10: TF-IDF WEIGHT TOKENS\n")
            f.write("=" * 70 + "\n")
            f.write(f"Matrícula: {MATRICULA}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Actividad: Cálculo de Pesos TF-IDF\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("METODOLOGÍA TF-IDF IMPLEMENTADA:\n")
            f.write("-" * 50 + "\n")
            f.write("• Term Frequency (TF): freq_término / total_términos_documento\n")
            f.write("• Inverse Document Frequency (IDF): log(total_docs / docs_con_término)\n")
            f.write("• TF-IDF: TF × IDF para medir relevancia de términos\n")
            f.write("• Análisis de tokens discriminativos y rankings de documentos\n")
            f.write("• Diccionario con pesos en lugar de frecuencias simples\n")
            f.write("\n")
            
            f.write("RESULTADOS DEL PROCESAMIENTO:\n")
            f.write("-" * 50 + "\n")
            f.write(f"Documentos procesados: {len(self.document_tokens)}\n")
            f.write(f"Tokens únicos analizados: {len(self.filtered_tokens)}\n")
            f.write(f"Cálculos TF realizados: {total_tf_calculations:,}\n")
            f.write(f"Cálculos IDF realizados: {len(self.idf_scores):,}\n")
            f.write(f"Cálculos TF-IDF realizados: {total_tfidf_calculations:,}\n")
            f.write(f"Tiempo de procesamiento: {processing_time:.3f} segundos\n")
            f.write("\n")
            
            f.write("BENEFICIOS DEL TF-IDF:\n")
            f.write("-" * 50 + "\n")
            f.write("• Identificación de términos más relevantes por documento\n")
            f.write("• Penalización de términos muy comunes (bajo IDF)\n")
            f.write("• Promoción de términos específicos y discriminativos\n")
            f.write("• Base para sistemas de recuperación de información\n")
            f.write("• Mejora significativa sobre frecuencias simples\n")
            f.write("\n")
            
            f.write("ARCHIVOS GENERADOS:\n")
            f.write("-" * 50 + "\n")
            f.write("1. dictionary_tfidf.txt - Diccionario con pesos TF-IDF\n")
            f.write("2. document_rankings.txt - Rankings de documentos por token\n")
            f.write("3. discriminative_analysis.txt - Análisis de tokens discriminativos\n")
            f.write("4. tfidf_statistics.txt - Estadísticas detalladas\n")
            f.write("5. a10_matricula.txt - Este reporte académico\n")
            f.write("\n")
            
            # Agregar top 5 tokens más discriminativos
            if self.idf_scores:
                top_discriminative = sorted(self.idf_scores.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]
                f.write("TOP 5 TOKENS MÁS DISCRIMINATIVOS:\n")
                f.write("-" * 50 + "\n")
                for i, (token, idf) in enumerate(top_discriminative, 1):
                    docs_with_token = len(self.token_documents[token])
                    f.write(f"{i}. '{token}': IDF={idf:.4f} ({docs_with_token} documentos)\n")
        
        print(f"✓ Reporte académico generado: {report_file}")
        return report_file
    
    def generate_detailed_statistics(self) -> Path:
        """Genera estadísticas detalladas del procesamiento TF-IDF"""
        stats_file = self.output_dir / "tfidf_statistics.txt"
        
        print("Generando estadísticas detalladas...")
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS DETALLADAS TF-IDF\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Estadísticas de documentos
            f.write("ESTADÍSTICAS DE DOCUMENTOS:\n")
            f.write("-" * 30 + "\n")
            doc_sizes = [len(tokens) for tokens in self.document_tokens.values()]
            if doc_sizes:
                f.write(f"Total documentos: {len(doc_sizes)}\n")
                f.write(f"Tokens promedio por documento: {sum(doc_sizes)/len(doc_sizes):.1f}\n")
                f.write(f"Documento más largo: {max(doc_sizes)} tokens\n")
                f.write(f"Documento más corto: {min(doc_sizes)} tokens\n")
            f.write("\n")
            
            # Estadísticas de IDF
            f.write("ESTADÍSTICAS DE IDF:\n")
            f.write("-" * 30 + "\n")
            idf_values = list(self.idf_scores.values())
            if idf_values:
                f.write(f"Total tokens con IDF: {len(idf_values)}\n")
                f.write(f"IDF promedio: {sum(idf_values)/len(idf_values):.4f}\n")
                f.write(f"IDF máximo: {max(idf_values):.4f}\n")
                f.write(f"IDF mínimo: {min(idf_values):.4f}\n")
            f.write("\n")
            
            # Estadísticas de TF-IDF
            f.write("ESTADÍSTICAS DE TF-IDF:\n")
            f.write("-" * 30 + "\n")
            all_tfidf = []
            for doc_tfidf in self.tfidf_scores.values():
                all_tfidf.extend(doc_tfidf.values())
            
            if all_tfidf:
                f.write(f"Total cálculos TF-IDF: {len(all_tfidf):,}\n")
                f.write(f"TF-IDF promedio: {sum(all_tfidf)/len(all_tfidf):.6f}\n")
                f.write(f"TF-IDF máximo: {max(all_tfidf):.6f}\n")
                f.write(f"TF-IDF mínimo: {min(all_tfidf):.6f}\n")
        
        print(f"✓ Estadísticas detalladas generadas: {stats_file}")
        return stats_file


def main():
    """Función principal de la Actividad 10"""
    start_time = time.time()
    
    print("=" * 70)
    print("ACTIVIDAD 10: TF-IDF WEIGHT TOKENS")
    print("Fase 3: Weight Tokens")
    print("=" * 70)
    
    # Configurar directorios
    if len(sys.argv) > 3:
        filtered_dict_file = sys.argv[1]
        html_dir = sys.argv[2]
        output_dir = sys.argv[3]
    else:
        filtered_dict_file = "data/output/activity9/dictionary_filtered.txt"
        html_dir = "data/input/Files"
        output_dir = "data/output/activity10"
    
    try:
        # Crear calculador TF-IDF
        calculator = TFIDFCalculator(html_dir, output_dir)
        
        # Cargar diccionario filtrado
        filtered_tokens = calculator.load_filtered_dictionary(filtered_dict_file)
        
        if not filtered_tokens:
            print("❌ No se pudieron cargar tokens del diccionario filtrado")
            return 1
        
        # Procesar documentos
        calculator.process_documents()
        
        # Calcular scores TF, IDF y TF-IDF
        calculator.calculate_tf_scores()
        calculator.calculate_idf_scores()
        calculator.calculate_tfidf_scores()
        
        # Generar archivos de salida
        tfidf_dict_file = calculator.generate_tfidf_dictionary()
        rankings_file = calculator.generate_document_rankings()
        analysis_file = calculator.generate_discriminative_analysis()
        stats_file = calculator.generate_detailed_statistics()
        
        # Calcular tiempo total
        processing_time = time.time() - start_time
        
        # Generar reporte académico
        report_file = calculator.generate_report(processing_time)
        
        print("\n" + "=" * 70)
        print("ACTIVIDAD 10 COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print(f"Tiempo total: {processing_time:.3f} segundos")
        print(f"Documentos procesados: {calculator.total_documents}")
        print(f"Tokens analizados: {len(calculator.filtered_tokens):,}")
        print(f"Cálculos TF-IDF: {sum(len(d) for d in calculator.tfidf_scores.values()):,}")
        print(f"Archivos generados en: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error en Actividad 10: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())