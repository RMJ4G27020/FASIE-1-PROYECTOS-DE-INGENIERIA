#!/usr/bin/env python3
"""
Actividad 8: Hash Table (Fase 3: Weight Tokens)
===============================================

Este módulo implementa una tabla hash personalizada para optimizar:
1. Búsquedas rápidas en el diccionario de tokens
2. Manejo de colisiones con encadenamiento separado
3. Análisis de rendimiento y distribución de hash
4. Casos de prueba y validación de la implementación

Autor: JOSE GPE RICO MORENO
Fecha: Septiembre 2025
Proyecto: FASIE-1-PROYECTOS-DE-INGENIERIA
"""

import os
import sys
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict

# Configuración de paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import MATRICULA

class HashNode:
    """Nodo para manejo de colisiones con encadenamiento"""
    
    def __init__(self, key: str, value: Dict[str, Any]):
        """
        Inicializa un nodo de la tabla hash
        
        Args:
            key: Token (palabra)
            value: Diccionario con datos del token
        """
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None

class CustomHashTable:
    """Implementación personalizada de tabla hash para tokens"""
    
    def __init__(self, initial_size: int = 1000):
        """
        Inicializa la tabla hash
        
        Args:
            initial_size: Tamaño inicial de la tabla
        """
        self.size = initial_size
        self.table: List[Optional[HashNode]] = [None] * self.size
        self.count = 0  # Número de elementos
        self.collisions = 0  # Contador de colisiones
        self.collision_chains = defaultdict(int)  # Longitud de cadenas
        
    def _hash_function(self, key: str) -> int:
        """
        Función hash personalizada usando SHA256
        
        Args:
            key: Clave a hashear
            
        Returns:
            Índice en la tabla hash
        """
        # Usar SHA256 para mejor distribución
        hash_bytes = hashlib.sha256(key.encode('utf-8')).digest()
        # Convertir primeros 4 bytes a entero
        hash_int = int.from_bytes(hash_bytes[:4], byteorder='big')
        return hash_int % self.size
    
    def _simple_hash(self, key: str) -> int:
        """
        Función hash simple para comparación
        
        Args:
            key: Clave a hashear
            
        Returns:
            Índice en la tabla hash
        """
        hash_val = 0
        for char in key:
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val
    
    def put(self, key: str, value: Dict[str, Any]) -> None:
        """
        Inserta un elemento en la tabla hash
        
        Args:
            key: Clave (token)
            value: Valor (datos del token)
        """
        index = self._hash_function(key)
        
        # Si la posición está vacía, insertar directamente
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.count += 1
        else:
            # Manejar colisión con encadenamiento
            current = self.table[index]
            
            # Buscar si la clave ya existe
            while current:
                if current.key == key:
                    current.value = value  # Actualizar valor existente
                    return
                if current.next is None:
                    break
                current = current.next
            
            # Insertar nuevo nodo al final de la cadena
            current.next = HashNode(key, value)
            self.count += 1
            self.collisions += 1
            
            # Contar longitud de la cadena
            chain_length = 1
            temp = self.table[index]
            while temp.next:
                chain_length += 1
                temp = temp.next
            self.collision_chains[index] = chain_length
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un elemento de la tabla hash
        
        Args:
            key: Clave a buscar
            
        Returns:
            Valor asociado o None si no existe
        """
        index = self._hash_function(key)
        current = self.table[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return None
    
    def contains(self, key: str) -> bool:
        """
        Verifica si una clave existe en la tabla
        
        Args:
            key: Clave a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.get(key) is not None
    
    def remove(self, key: str) -> bool:
        """
        Elimina un elemento de la tabla hash
        
        Args:
            key: Clave a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        index = self._hash_function(key)
        current = self.table[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next
        
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la tabla hash
        
        Returns:
            Diccionario con estadísticas
        """
        occupied_slots = sum(1 for slot in self.table if slot is not None)
        load_factor = self.count / self.size
        
        # Calcular distribución de cadenas
        chain_lengths = []
        for slot in self.table:
            if slot is not None:
                length = 1
                current = slot
                while current.next:
                    length += 1
                    current = current.next
                chain_lengths.append(length)
        
        avg_chain_length = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
        max_chain_length = max(chain_lengths) if chain_lengths else 0
        
        return {
            'total_elements': self.count,
            'table_size': self.size,
            'occupied_slots': occupied_slots,
            'load_factor': load_factor,
            'collisions': self.collisions,
            'avg_chain_length': avg_chain_length,
            'max_chain_length': max_chain_length,
            'chain_distribution': chain_lengths
        }
    
    def keys(self) -> List[str]:
        """
        Obtiene todas las claves de la tabla
        
        Returns:
            Lista de claves
        """
        keys = []
        for slot in self.table:
            current = slot
            while current:
                keys.append(current.key)
                current = current.next
        return keys


class HashTableAnalyzer:
    """Analizador de rendimiento de tabla hash"""
    
    def __init__(self, output_dir: str):
        """
        Inicializa el analizador
        
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        print(f"✓ Cargados {len(dictionary_data)} tokens del diccionario")
        return dictionary_data
    
    def create_hash_table(self, dictionary_data: Dict[str, Dict[str, Any]], 
                         table_size: int = 10000) -> CustomHashTable:
        """
        Crea y pobla la tabla hash
        
        Args:
            dictionary_data: Datos del diccionario
            table_size: Tamaño de la tabla hash
            
        Returns:
            Tabla hash poblada
        """
        print(f"Creando tabla hash con tamaño: {table_size}")
        
        hash_table = CustomHashTable(table_size)
        
        for token, data in dictionary_data.items():
            hash_table.put(token, data)
        
        print(f"✓ Tabla hash creada con {hash_table.count} elementos")
        return hash_table
    
    def run_performance_tests(self, hash_table: CustomHashTable, 
                            test_tokens: List[str]) -> Dict[str, float]:
        """
        Ejecuta pruebas de rendimiento
        
        Args:
            hash_table: Tabla hash a probar
            test_tokens: Tokens para probar
            
        Returns:
            Resultados de las pruebas
        """
        print("Ejecutando pruebas de rendimiento...")
        
        # Prueba de búsqueda
        start_time = time.time()
        found_count = 0
        for token in test_tokens:
            if hash_table.contains(token):
                found_count += 1
        search_time = time.time() - start_time
        
        # Prueba de inserción
        start_time = time.time()
        test_hash = CustomHashTable(1000)
        for i, token in enumerate(test_tokens[:1000]):  # Solo primeros 1000
            test_hash.put(f"test_{token}_{i}", {'test': True})
        insert_time = time.time() - start_time
        
        return {
            'search_time': search_time,
            'search_rate': len(test_tokens) / search_time,
            'found_ratio': found_count / len(test_tokens),
            'insert_time': insert_time,
            'insert_rate': 1000 / insert_time
        }
    
    def compare_hash_functions(self, dictionary_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compara diferentes funciones hash
        
        Args:
            dictionary_data: Datos del diccionario
            
        Returns:
            Comparación de funciones hash
        """
        print("Comparando funciones hash...")
        
        # Probar con función SHA256
        hash_table_sha = CustomHashTable(5000)
        for token, data in dictionary_data.items():
            hash_table_sha.put(token, data)
        
        # Crear tabla con función simple
        hash_table_simple = CustomHashTable(5000)
        # Cambiar temporalmente la función hash
        original_hash = hash_table_simple._hash_function
        hash_table_simple._hash_function = hash_table_simple._simple_hash
        
        for token, data in dictionary_data.items():
            hash_table_simple.put(token, data)
        
        # Restaurar función original
        hash_table_simple._hash_function = original_hash
        
        return {
            'sha256': hash_table_sha.get_statistics(),
            'simple': hash_table_simple.get_statistics()
        }
    
    def generate_hash_analysis_report(self, hash_table: CustomHashTable, 
                                    performance_results: Dict[str, float],
                                    comparison_results: Dict[str, Any]) -> Path:
        """
        Genera reporte de análisis de hash table
        
        Args:
            hash_table: Tabla hash analizada
            performance_results: Resultados de rendimiento
            comparison_results: Comparación de funciones
            
        Returns:
            Path del archivo de reporte
        """
        report_file = self.output_dir / "hash_table_analysis.txt"
        stats = hash_table.get_statistics()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("ANÁLISIS DE TABLA HASH - ACTIVIDAD 8\n")
            f.write("=" * 60 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("ESTADÍSTICAS DE LA TABLA HASH:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de elementos: {stats['total_elements']:,}\n")
            f.write(f"Tamaño de la tabla: {stats['table_size']:,}\n")
            f.write(f"Slots ocupados: {stats['occupied_slots']:,}\n")
            f.write(f"Factor de carga: {stats['load_factor']:.3f}\n")
            f.write(f"Colisiones: {stats['collisions']:,}\n")
            f.write(f"Longitud promedio de cadena: {stats['avg_chain_length']:.2f}\n")
            f.write(f"Longitud máxima de cadena: {stats['max_chain_length']}\n")
            f.write("\n")
            
            f.write("RESULTADOS DE RENDIMIENTO:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Tiempo de búsqueda: {performance_results['search_time']:.4f} segundos\n")
            f.write(f"Velocidad de búsqueda: {performance_results['search_rate']:.0f} búsquedas/seg\n")
            f.write(f"Ratio de encontrados: {performance_results['found_ratio']:.3f}\n")
            f.write(f"Tiempo de inserción: {performance_results['insert_time']:.4f} segundos\n")
            f.write(f"Velocidad de inserción: {performance_results['insert_rate']:.0f} inserciones/seg\n")
            f.write("\n")
            
            f.write("COMPARACIÓN DE FUNCIONES HASH:\n")
            f.write("-" * 40 + "\n")
            for func_name, func_stats in comparison_results.items():
                f.write(f"\n{func_name.upper()}:\n")
                f.write(f"  Colisiones: {func_stats['collisions']:,}\n")
                f.write(f"  Factor de carga: {func_stats['load_factor']:.3f}\n")
                f.write(f"  Longitud promedio de cadena: {func_stats['avg_chain_length']:.2f}\n")
                f.write(f"  Longitud máxima de cadena: {func_stats['max_chain_length']}\n")
            
            f.write("\n")
            f.write("DISTRIBUCIÓN DE LONGITUDES DE CADENA:\n")
            f.write("-" * 40 + "\n")
            chain_dist = {}
            for length in stats['chain_distribution']:
                chain_dist[length] = chain_dist.get(length, 0) + 1
            
            for length in sorted(chain_dist.keys()):
                count = chain_dist[length]
                f.write(f"  Longitud {length}: {count} cadenas\n")
        
        print(f"✓ Reporte de análisis generado: {report_file}")
        return report_file
    
    def generate_test_cases(self, hash_table: CustomHashTable) -> Path:
        """
        Genera casos de prueba para la tabla hash
        
        Args:
            hash_table: Tabla hash
            
        Returns:
            Path del archivo de casos de prueba
        """
        test_file = self.output_dir / "hash_table_tests.txt"
        
        # Obtener algunos tokens para probar
        all_keys = hash_table.keys()
        test_keys = all_keys[:20] if len(all_keys) >= 20 else all_keys
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("CASOS DE PRUEBA - TABLA HASH\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("PRUEBAS DE FUNCIONALIDAD:\n")
            f.write("-" * 30 + "\n")
            
            # Prueba de inserción y búsqueda
            f.write("1. PRUEBA DE INSERCIÓN Y BÚSQUEDA:\n")
            success_count = 0
            for key in test_keys:
                value = hash_table.get(key)
                if value is not None:
                    success_count += 1
                    f.write(f"   ✓ '{key}': {value}\n")
                else:
                    f.write(f"   ✗ '{key}': No encontrado\n")
            
            f.write(f"\n   Resultado: {success_count}/{len(test_keys)} pruebas exitosas\n")
            f.write(f"   Tasa de éxito: {success_count/len(test_keys)*100:.1f}%\n\n")
            
            # Prueba de colisiones
            f.write("2. PRUEBA DE MANEJO DE COLISIONES:\n")
            collision_examples = []
            for i, slot in enumerate(hash_table.table[:100]):  # Solo primeros 100 slots
                if slot is not None:
                    chain_length = 1
                    current = slot
                    chain_keys = [current.key]
                    while current.next:
                        chain_length += 1
                        current = current.next
                        chain_keys.append(current.key)
                    
                    if chain_length > 1:
                        collision_examples.append((i, chain_length, chain_keys))
                        if len(collision_examples) >= 5:  # Solo mostrar primeros 5
                            break
            
            for slot_idx, length, keys in collision_examples:
                f.write(f"   Slot {slot_idx}: {length} elementos en cadena\n")
                for key in keys:
                    f.write(f"     - {key}\n")
                f.write("\n")
            
            # Prueba de eliminación
            f.write("3. PRUEBA DE ELIMINACIÓN:\n")
            test_key = test_keys[0] if test_keys else None
            if test_key:
                original_value = hash_table.get(test_key)
                removed = hash_table.remove(test_key)
                after_removal = hash_table.get(test_key)
                
                f.write(f"   Token a eliminar: '{test_key}'\n")
                f.write(f"   Valor original: {original_value}\n")
                f.write(f"   Eliminación exitosa: {removed}\n")
                f.write(f"   Valor después de eliminar: {after_removal}\n")
                f.write(f"   Resultado: {'✓ CORRECTO' if removed and after_removal is None else '✗ ERROR'}\n")
                
                # Restaurar el elemento
                if removed and original_value:
                    hash_table.put(test_key, original_value)
                    f.write(f"   Elemento restaurado para integridad de datos\n")
        
        print(f"✓ Casos de prueba generados: {test_file}")
        return test_file
    
    def generate_report(self, processing_time: float, hash_table: CustomHashTable) -> Path:
        """
        Genera reporte académico de la actividad
        
        Args:
            processing_time: Tiempo de procesamiento
            hash_table: Tabla hash creada
            
        Returns:
            Path del archivo de reporte
        """
        report_file = self.output_dir / f"a8_{MATRICULA}.txt"
        stats = hash_table.get_statistics()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE ACADÉMICO - ACTIVIDAD 8: HASH TABLE\n")
            f.write("=" * 60 + "\n")
            f.write(f"Matrícula: {MATRICULA}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Actividad: Implementación de Tabla Hash\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("IMPLEMENTACIÓN REALIZADA:\n")
            f.write("-" * 40 + "\n")
            f.write("• Tabla hash personalizada con encadenamiento separado\n")
            f.write("• Función hash usando SHA256 para mejor distribución\n")
            f.write("• Manejo automático de colisiones\n")
            f.write("• Análisis de rendimiento y estadísticas\n")
            f.write("• Casos de prueba automatizados\n")
            f.write("\n")
            
            f.write("RESULTADOS DEL PROCESAMIENTO:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Elementos en la tabla: {stats['total_elements']:,}\n")
            f.write(f"Tamaño de la tabla: {stats['table_size']:,}\n")
            f.write(f"Factor de carga: {stats['load_factor']:.3f}\n")
            f.write(f"Colisiones detectadas: {stats['collisions']:,}\n")
            f.write(f"Tiempo de procesamiento: {processing_time:.3f} segundos\n")
            f.write("\n")
            
            f.write("EFICIENCIA DEL HASH:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Slots ocupados: {stats['occupied_slots']:,} de {stats['table_size']:,}\n")
            f.write(f"Utilización de memoria: {stats['occupied_slots']/stats['table_size']*100:.1f}%\n")
            f.write(f"Longitud promedio de cadena: {stats['avg_chain_length']:.2f}\n")
            f.write(f"Longitud máxima de cadena: {stats['max_chain_length']}\n")
            f.write("\n")
            
            f.write("ARCHIVOS GENERADOS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. hash_table_analysis.txt - Análisis detallado de la tabla\n")
            f.write("2. hash_table_tests.txt - Casos de prueba y validación\n")
            f.write("3. hash_table_implementation.txt - Detalles de implementación\n")
            f.write("4. a8_matricula.txt - Este reporte académico\n")
        
        print(f"✓ Reporte académico generado: {report_file}")
        return report_file


def main():
    """Función principal de la Actividad 8"""
    start_time = time.time()
    
    print("=" * 60)
    print("ACTIVIDAD 8: HASH TABLE")
    print("Fase 3: Weight Tokens")
    print("=" * 60)
    
    # Configurar directorios
    if len(sys.argv) > 2:
        dict_file = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        dict_file = "data/output/activity7/dictionary_posting.txt"
        output_dir = "data/output/activity8"
    
    try:
        # Crear analizador
        analyzer = HashTableAnalyzer(output_dir)
        
        # Cargar datos del diccionario
        dictionary_data = analyzer.load_dictionary_data(dict_file)
        
        if not dictionary_data:
            print("❌ No se pudieron cargar datos del diccionario")
            return 1
        
        # Crear tabla hash
        hash_table = analyzer.create_hash_table(dictionary_data)
        
        # Ejecutar pruebas de rendimiento
        test_tokens = list(dictionary_data.keys())[:1000]  # Probar con 1000 tokens
        performance_results = analyzer.run_performance_tests(hash_table, test_tokens)
        
        # Comparar funciones hash
        comparison_results = analyzer.compare_hash_functions(dictionary_data)
        
        # Generar archivos de análisis
        analysis_file = analyzer.generate_hash_analysis_report(
            hash_table, performance_results, comparison_results
        )
        
        # Generar casos de prueba
        test_file = analyzer.generate_test_cases(hash_table)
        
        # Generar documentación de implementación
        impl_file = analyzer.output_dir / "hash_table_implementation.txt"
        with open(impl_file, 'w', encoding='utf-8') as f:
            f.write("DOCUMENTACIÓN DE IMPLEMENTACIÓN - TABLA HASH\n")
            f.write("=" * 60 + "\n")
            f.write("CARACTERÍSTICAS IMPLEMENTADAS:\n")
            f.write("• Función hash SHA256 para distribución uniforme\n")
            f.write("• Manejo de colisiones con encadenamiento separado\n")
            f.write("• Operaciones: insertar, buscar, eliminar, verificar existencia\n")
            f.write("• Estadísticas de rendimiento y análisis de distribución\n")
            f.write("• Redimensionamiento dinámico (preparado para implementar)\n")
            f.write("• Comparación de diferentes funciones hash\n")
        
        # Calcular tiempo total
        processing_time = time.time() - start_time
        
        # Generar reporte académico
        report_file = analyzer.generate_report(processing_time, hash_table)
        
        print("\n" + "=" * 60)
        print("ACTIVIDAD 8 COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print(f"Tiempo total: {processing_time:.3f} segundos")
        print(f"Elementos en tabla hash: {hash_table.count:,}")
        print(f"Factor de carga: {hash_table.get_statistics()['load_factor']:.3f}")
        print(f"Archivos generados en: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error en Actividad 8: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())