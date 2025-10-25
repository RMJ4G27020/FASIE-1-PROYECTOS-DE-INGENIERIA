# Código Detallado - Actividades 4, 5 y 6

## Actividad 4: Consolidación de Palabras
### Código Completo (actividad4_consolidate_words.py)

```python
import os
from typing import List, Dict
from collections import Counter
import logging

class WordConsolidator:
    def __init__(self):
        self.word_frequencies: Dict[str, int] = Counter()
        self.processed_files = 0
        self.total_words = 0
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def process_file(self, input_file: str) -> None:
        """
        Procesa un archivo individual y actualiza el contador de frecuencias.
        
        Args:
            input_file: Ruta al archivo de entrada
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.word_frequencies[word] += 1
                        self.total_words += 1
            self.processed_files += 1
            self.logger.info(f"Procesado archivo: {input_file}")
        except Exception as e:
            self.logger.error(f"Error procesando {input_file}: {str(e)}")

    def consolidate_words(self, input_files: List[str], output_file: str) -> None:
        """
        Consolida palabras de múltiples archivos en uno solo.
        
        Args:
            input_files: Lista de rutas de archivos de entrada
            output_file: Ruta del archivo de salida
        """
        self.logger.info("Iniciando consolidación de palabras...")
        
        # Procesar todos los archivos
        for input_file in input_files:
            if os.path.exists(input_file):
                self.process_file(input_file)
            else:
                self.logger.warning(f"Archivo no encontrado: {input_file}")

        # Escribir resultados ordenados
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for word, count in sorted(self.word_frequencies.items()):
                    f.write(f"{word}: {count}\n")
            
            self.logger.info(f"Consolidación completada. "
                           f"Procesados {self.processed_files} archivos, "
                           f"total de palabras: {self.total_words}")
        except Exception as e:
            self.logger.error(f"Error escribiendo resultados: {str(e)}")

    def get_statistics(self) -> Dict:
        """
        Genera estadísticas del proceso de consolidación.
        
        Returns:
            Dict con estadísticas del proceso
        """
        return {
            'files_processed': self.processed_files,
            'total_words': self.total_words,
            'unique_words': len(self.word_frequencies),
            'most_common': self.word_frequencies.most_common(10)
        }
```

## Actividad 5: Tokenización y Análisis
### Código Completo (actividad5_tokenize.py)

```python
import re
from typing import Dict, List, Set, Optional
from collections import defaultdict
import json
import logging
from pathlib import Path

class HTMLTokenizer:
    def __init__(self):
        # Patrones de tokenización
        self.patterns = {
            'tag': r'<[^>]+>',
            'word': r'\b[a-zA-Z]+\b',
            'number': r'\b\d+\b',
            'special_char': r'[^\w\s]',
            'attribute': r'\s(\w+)="([^"]*)"',
            'comment': r'<!--[\s\S]*?-->'
        }
        
        # Configuración de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Inicializar contadores
        self.reset_counters()

    def reset_counters(self) -> None:
        """Reinicia todos los contadores internos."""
        self.token_counts = defaultdict(int)
        self.unique_tokens = defaultdict(set)
        self.tag_stack = []
        self.structure = []

    def tokenize(self, text: str) -> Dict[str, List[str]]:
        """
        Tokeniza el texto HTML y clasifica los tokens.
        
        Args:
            text: Texto HTML a tokenizar
            
        Returns:
            Diccionario con tokens clasificados por categoría
        """
        tokens = defaultdict(list)
        
        # Procesar cada tipo de patrón
        for category, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                token = match.group()
                tokens[category].append(token)
                self.token_counts[category] += 1
                self.unique_tokens[category].add(token)
                
                # Análisis especial para tags
                if category == 'tag':
                    self._analyze_tag_structure(token)
        
        return dict(tokens)

    def _analyze_tag_structure(self, tag: str) -> None:
        """
        Analiza la estructura de tags HTML.
        
        Args:
            tag: Tag HTML a analizar
        """
        if tag.startswith('</'):
            # Tag de cierre
            if self.tag_stack:
                opened_tag = self.tag_stack.pop()
                self.structure.append(f"Cerrado: {opened_tag}")
        elif not tag.endswith('/>'):
            # Tag de apertura
            tag_name = re.match(r'<(\w+)', tag).group(1)
            self.tag_stack.append(tag_name)
            self.structure.append(f"Abierto: {tag_name}")

    def analyze_document(self, file_path: str) -> Dict:
        """
        Realiza un análisis completo de un documento HTML.
        
        Args:
            file_path: Ruta al archivo HTML
            
        Returns:
            Dict con estadísticas del análisis
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
                
            self.reset_counters()
            content = path.read_text(encoding='utf-8')
            tokens = self.tokenize(content)
            
            stats = {
                'file_name': path.name,
                'file_size': path.stat().st_size,
                'token_counts': dict(self.token_counts),
                'unique_tokens': {
                    k: len(v) for k, v in self.unique_tokens.items()
                },
                'tag_structure': self.structure,
                'unclosed_tags': self.tag_stack.copy()
            }
            
            self.logger.info(f"Análisis completado para {path.name}")
            return stats
            
        except Exception as e:
            self.logger.error(f"Error analizando {file_path}: {str(e)}")
            raise

    def save_analysis(self, stats: Dict, output_file: str) -> None:
        """
        Guarda los resultados del análisis en formato JSON.
        
        Args:
            stats: Estadísticas a guardar
            output_file: Ruta del archivo de salida
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Resultados guardados en {output_file}")
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {str(e)}")
```

## Actividad 6: Diccionario y Análisis de Frecuencias
### Código Completo (actividad6_dictionary.py)

```python
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter, defaultdict
import json
import logging
from pathlib import Path
from datetime import datetime

class WordAnalyzer:
    def __init__(self):
        # Inicialización de estructuras de datos
        self.dictionary: Dict[str, Dict] = {}
        self.frequency = Counter()
        self.word_categories: Dict[str, Set[str]] = defaultdict(set)
        
        # Configuración de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def categorize_word(self, word: str) -> List[str]:
        """
        Categoriza una palabra según diferentes criterios.
        
        Args:
            word: Palabra a categorizar
            
        Returns:
            Lista de categorías a las que pertenece la palabra
        """
        categories = []
        
        # Categorización por longitud
        if len(word) < 5:
            categories.append('corta')
        elif len(word) < 8:
            categories.append('media')
        else:
            categories.append('larga')
            
        # Categorización por tipo
        if word.isupper():
            categories.append('mayúsculas')
        elif word.islower():
            categories.append('minúsculas')
        elif word.istitle():
            categories.append('título')
            
        return categories

    def analyze_word(self, word: str) -> Dict:
        """
        Realiza un análisis detallado de una palabra.
        
        Args:
            word: Palabra a analizar
            
        Returns:
            Dict con información detallada de la palabra
        """
        return {
            'length': len(word),
            'first_char': word[0],
            'last_char': word[-1],
            'vowels': sum(1 for c in word.lower() if c in 'aeiouáéíóú'),
            'consonants': sum(1 for c in word.lower() 
                            if c.isalpha() and c not in 'aeiouáéíóú'),
            'categories': self.categorize_word(word)
        }

    def build_dictionary(self, input_files: List[str]) -> None:
        """
        Construye el diccionario a partir de los archivos de entrada.
        
        Args:
            input_files: Lista de rutas de archivos de entrada
        """
        for file_path in input_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split(':')
                        if len(parts) >= 1:
                            word = parts[0].strip()
                            if word:
                                # Analizar la palabra
                                self.dictionary[word] = self.analyze_word(word)
                                self.frequency[word] += 1
                                
                                # Categorizar la palabra
                                categories = self.categorize_word(word)
                                for category in categories:
                                    self.word_categories[category].add(word)
                                    
            except Exception as e:
                self.logger.error(f"Error procesando {file_path}: {str(e)}")

    def generate_statistics(self) -> Dict:
        """
        Genera estadísticas detalladas del diccionario.
        
        Returns:
            Dict con estadísticas completas
        """
        stats = {
            'general': {
                'total_words': len(self.dictionary),
                'unique_words': len(set(self.dictionary.keys())),
                'most_common': self.frequency.most_common(10)
            },
            'length_distribution': defaultdict(int),
            'first_char_distribution': defaultdict(int),
            'categories': {
                category: len(words)
                for category, words in self.word_categories.items()
            },
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Calcular distribuciones
        for word in self.dictionary:
            length = len(word)
            first_char = word[0]
            stats['length_distribution'][length] += 1
            stats['first_char_distribution'][first_char] += 1
        
        # Convertir defaultdicts a diccionarios regulares
        stats['length_distribution'] = dict(stats['length_distribution'])
        stats['first_char_distribution'] = dict(stats['first_char_distribution'])
        
        return stats

    def save_dictionary(self, output_file: str) -> None:
        """
        Guarda el diccionario y estadísticas en formato JSON.
        
        Args:
            output_file: Ruta del archivo de salida
        """
        try:
            output = {
                'dictionary': self.dictionary,
                'statistics': self.generate_statistics()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Diccionario guardado en {output_file}")
            
        except Exception as e:
            self.logger.error(f"Error guardando diccionario: {str(e)}")

    def export_category_files(self, output_dir: str) -> None:
        """
        Exporta palabras por categoría a archivos separados.
        
        Args:
            output_dir: Directorio de salida
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            for category, words in self.word_categories.items():
                file_path = output_path / f"{category}_words.txt"
                with open(file_path, 'w', encoding='utf-8') as f:
                    for word in sorted(words):
                        frequency = self.frequency[word]
                        f.write(f"{word}: {frequency}\n")
                        
            self.logger.info(f"Archivos de categorías exportados a {output_dir}")
            
        except Exception as e:
            self.logger.error(f"Error exportando categorías: {str(e)}")
```

### Mejoras y Características Adicionales

1. **Gestión de Errores**
   - Manejo robusto de excepciones
   - Logging detallado de operaciones
   - Validación de archivos y directorios

2. **Optimización**
   - Uso de tipos tipados para mejor rendimiento
   - Estructuras de datos optimizadas
   - Procesamiento eficiente de archivos grandes

3. **Características Extra**
   - Categorización automática de palabras
   - Estadísticas detalladas y análisis
   - Exportación en múltiples formatos

4. **Documentación**
   - Docstrings completos
   - Tipos anotados
   - Ejemplos de uso

### Ejemplo de Uso Integrado

```python
def run_integrated_analysis(input_dir: str, output_dir: str):
    # Configurar rutas
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Actividad 4: Consolidación
    consolidator = WordConsolidator()
    html_files = list(input_path.glob('*.html'))
    consolidated_file = output_path / 'consolidated_words.txt'
    consolidator.consolidate_words(
        [str(f) for f in html_files], 
        str(consolidated_file)
    )
    
    # Actividad 5: Tokenización
    tokenizer = HTMLTokenizer()
    token_stats = {}
    for html_file in html_files:
        stats = tokenizer.analyze_document(str(html_file))
        token_stats[html_file.name] = stats
    
    # Guardar resultados de tokenización
    with open(output_path / 'token_analysis.json', 'w') as f:
        json.dump(token_stats, f, indent=4)
    
    # Actividad 6: Análisis de Palabras
    analyzer = WordAnalyzer()
    analyzer.build_dictionary([str(consolidated_file)])
    analyzer.save_dictionary(str(output_path / 'word_analysis.json'))
    analyzer.export_category_files(str(output_path / 'categories'))
    
    return {
        'consolidation': consolidator.get_statistics(),
        'tokenization': token_stats,
        'word_analysis': analyzer.generate_statistics()
    }
```

Este código proporciona una implementación completa y robusta de las actividades 4, 5 y 6, con características adicionales de manejo de errores, logging, y análisis detallado.