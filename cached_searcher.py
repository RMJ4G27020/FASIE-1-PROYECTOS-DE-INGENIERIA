"""
Optimización adicional para web_app.py - Caché de búsquedas más populares
"""

from functools import lru_cache
from retrieve_optimized import OptimizedDictionarySearcher
from typing import List, Dict
from collections import defaultdict

class CachedSearcher(OptimizedDictionarySearcher):
    """Versión mejorada con caché LRU para búsquedas repetidas"""
    
    @lru_cache(maxsize=1000)
    def _search_token_cached(self, token: str):
        """Búsqueda con caché para tokens frecuentes (retorna tupla para cache)"""
        # Llamar al método de la clase padre para evitar recursión
        results = super().search_token(token)
        return tuple(results) if results else ()
    
    def search_token(self, token: str) -> List[Dict]:
        """Override para usar versión cacheada"""
        cached_results = self._search_token_cached(token)
        return list(cached_results) if cached_results else []
    
    def search_multiple_tokens(self, tokens: List[str]) -> List[Dict]:
        """Sobrescribe para usar versión cacheada"""
        doc_scores = defaultdict(lambda: {'doc_name': '', 'total_tfidf': 0.0, 'token_count': 0})
        
        for token in tokens:
            results = self.search_token(token)  # Usa versión cacheada
            
            for doc in results:
                doc_id = doc['doc_id']
                doc_name = doc['doc_name']
                tfidf = doc['tfidf']
                
                doc_scores[doc_id]['doc_id'] = doc_id
                doc_scores[doc_id]['doc_name'] = doc_name
                doc_scores[doc_id]['total_tfidf'] += tfidf
                doc_scores[doc_id]['token_count'] += 1
        
        results_list = list(doc_scores.values())
        results_list.sort(key=lambda x: x['total_tfidf'], reverse=True)
        
        return results_list
