"""
Fase 5 - Activity 15: Quick Load Test (1 minuto de prueba)
Versión corta para validar que el sistema funciona correctamente
"""

import requests
import time
import threading
import random
import statistics
import psutil
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# =============================================================================
# CONFIGURACIÓN DE LA PRUEBA - VERSIÓN CORTA
# =============================================================================

BASE_URL = "http://localhost:5000"
NUM_USERS = 5  # Empezar con 5 usuarios
DURATION_MINUTES = 1  # Solo 1 minuto
MAX_RESPONSE_TIME = 2.0  # segundos

# Directorio para resultados
OUTPUT_DIR = Path("activity15")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consultas de prueba
TEST_QUERIES = [
    "arkansas", "lawyer", "consumers", "United States", "laws",
    "court", "insurance", "government", "health", "business"
]

# =============================================================================
# CLASE PARA ESTADÍSTICAS
# =============================================================================

class LoadTestStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.requests_sent = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.response_times = []
        self.errors = []
        self.start_time = None
        self.end_time = None
        self.metrics_timeline = defaultdict(lambda: {
            'requests': 0,
            'response_times': [],
            'cpu_percent': 0,
            'memory_percent': 0
        })
        
    def record_request(self, success, response_time, error=None):
        with self.lock:
            self.requests_sent += 1
            if success:
                self.requests_success += 1
                self.response_times.append(response_time)
            else:
                self.requests_failed += 1
                if error:
                    self.errors.append(error)
            
            current_second = int(time.time() - self.start_time)
            self.metrics_timeline[current_second]['requests'] += 1
            if success:
                self.metrics_timeline[current_second]['response_times'].append(response_time)
    
    def record_system_metrics(self):
        current_second = int(time.time() - self.start_time)
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        with self.lock:
            self.metrics_timeline[current_second]['cpu_percent'] = cpu_percent
            self.metrics_timeline[current_second]['memory_percent'] = memory.percent
    
    def get_summary(self):
        duration = self.end_time - self.start_time if self.end_time else time.time() - self.start_time
        
        summary = {
            'test_config': {
                'num_users': NUM_USERS,
                'duration_minutes': DURATION_MINUTES,
                'max_response_time': MAX_RESPONSE_TIME
            },
            'duration_seconds': duration,
            'total_requests': self.requests_sent,
            'successful_requests': self.requests_success,
            'failed_requests': self.requests_failed,
            'success_rate': (self.requests_success / self.requests_sent * 100) if self.requests_sent > 0 else 0,
            'requests_per_second': self.requests_sent / duration if duration > 0 else 0
        }
        
        if self.response_times:
            sorted_times = sorted(self.response_times)
            summary['response_times'] = {
                'min': min(self.response_times),
                'max': max(self.response_times),
                'mean': statistics.mean(self.response_times),
                'median': statistics.median(self.response_times),
                'stdev': statistics.stdev(self.response_times) if len(self.response_times) > 1 else 0,
                'percentile_95': sorted_times[int(len(sorted_times) * 0.95)],
                'percentile_99': sorted_times[int(len(sorted_times) * 0.99)],
                'below_2s': sum(1 for t in self.response_times if t < 2.0) / len(self.response_times) * 100
            }
        
        cpu_values = [m['cpu_percent'] for m in self.metrics_timeline.values() if m['cpu_percent'] > 0]
        memory_values = [m['memory_percent'] for m in self.metrics_timeline.values() if m['memory_percent'] > 0]
        
        if cpu_values:
            summary['system_metrics'] = {
                'cpu_avg': statistics.mean(cpu_values),
                'cpu_max': max(cpu_values),
                'memory_avg': statistics.mean(memory_values),
                'memory_max': max(memory_values)
            }
        
        return summary

# =============================================================================
# CLASE PARA SIMULAR USUARIOS
# =============================================================================

class VirtualUser(threading.Thread):
    def __init__(self, user_id, stats, stop_event):
        super().__init__()
        self.user_id = user_id
        self.stats = stats
        self.stop_event = stop_event
        self.daemon = True
    
    def run(self):
        while not self.stop_event.is_set():
            query = random.choice(TEST_QUERIES)
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{BASE_URL}/search",
                    data={'query': query},
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.stats.record_request(True, response_time)
                else:
                    self.stats.record_request(False, 0, f"HTTP {response.status_code}")
            
            except Exception as e:
                response_time = time.time() - start_time
                self.stats.record_request(False, response_time, str(e))
            
            time.sleep(random.uniform(0.5, 2))  # Búsquedas más frecuentes para prueba rápida

# =============================================================================
# MONITOR DE SISTEMA
# =============================================================================

class SystemMonitor(threading.Thread):
    def __init__(self, stats, stop_event):
        super().__init__()
        self.stats = stats
        self.stop_event = stop_event
        self.daemon = True
    
    def run(self):
        while not self.stop_event.is_set():
            self.stats.record_system_metrics()
            time.sleep(1)

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def run_load_test():
    print("="*80)
    print("PRUEBA RÁPIDA DE CARGA (1 MINUTO)")
    print("="*80)
    print(f"Usuarios: {NUM_USERS} | Duración: {DURATION_MINUTES} min | Max RT: {MAX_RESPONSE_TIME}s")
    print("="*80)
    
    # Verificar servidor
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"ERROR: Servidor no responde en {BASE_URL}")
            return
        print("✓ Servidor verificado")
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    stats = LoadTestStats()
    stats.start_time = time.time()
    stop_event = threading.Event()
    
    # Iniciar monitor
    monitor = SystemMonitor(stats, stop_event)
    monitor.start()
    
    # Iniciar usuarios
    users = []
    for i in range(NUM_USERS):
        user = VirtualUser(i + 1, stats, stop_event)
        user.start()
        users.append(user)
        time.sleep(0.1)
    
    print(f"✓ {NUM_USERS} usuarios iniciados\n")
    
    # Ejecutar prueba
    duration_seconds = DURATION_MINUTES * 60
    start = time.time()
    
    try:
        while time.time() - start < duration_seconds:
            elapsed = int(time.time() - start)
            remaining = duration_seconds - elapsed
            
            if elapsed % 5 == 0:
                with stats.lock:
                    rps = stats.requests_sent / elapsed if elapsed > 0 else 0
                    success_rate = (stats.requests_success / stats.requests_sent * 100) if stats.requests_sent > 0 else 0
                    avg_rt = statistics.mean(stats.response_times[-10:]) if len(stats.response_times) >= 10 else 0
                    
                    print(f"[{elapsed}s] Requests: {stats.requests_sent:4d} | RPS: {rps:5.2f} | "
                          f"Success: {success_rate:5.1f}% | Avg RT: {avg_rt:.3f}s | Remaining: {remaining}s")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario")
    
    # Detener
    stop_event.set()
    for user in users:
        user.join(timeout=5)
    monitor.join(timeout=5)
    
    stats.end_time = time.time()
    
    # Resultados
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80)
    
    summary = stats.get_summary()
    
    # Guardar JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = OUTPUT_DIR / f"quick_test_{timestamp}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': summary,
            'timeline': dict(stats.metrics_timeline),
            'errors': stats.errors
        }, f, indent=2)
    
    print(f"\n✓ Resultados: {json_file}")
    
    # Mostrar resumen
    print(f"\nDuración: {summary['duration_seconds']:.2f}s")
    print(f"Total requests: {summary['total_requests']}")
    print(f"Exitosos: {summary['successful_requests']}")
    print(f"Fallidos: {summary['failed_requests']}")
    print(f"Tasa éxito: {summary['success_rate']:.2f}%")
    print(f"RPS: {summary['requests_per_second']:.2f}")
    
    if 'response_times' in summary:
        rt = summary['response_times']
        print(f"\nTiempos de respuesta:")
        print(f"  Min: {rt['min']:.3f}s | Max: {rt['max']:.3f}s | Mean: {rt['mean']:.3f}s")
        print(f"  Median: {rt['median']:.3f}s | P95: {rt['percentile_95']:.3f}s | P99: {rt['percentile_99']:.3f}s")
        print(f"  Bajo 2s: {rt['below_2s']:.1f}%")
        
        # EVALUACIÓN DEL REQUISITO
        if rt['below_2s'] >= 95:
            print(f"\n✓ APROBADO: {rt['below_2s']:.1f}% de respuestas bajo 2 segundos")
        else:
            print(f"\n✗ NO CUMPLE: Solo {rt['below_2s']:.1f}% bajo 2 segundos (requerido: >95%)")
    
    if 'system_metrics' in summary:
        sm = summary['system_metrics']
        print(f"\nSistema:")
        print(f"  CPU: avg={sm['cpu_avg']:.1f}% max={sm['cpu_max']:.1f}%")
        print(f"  Memoria: avg={sm['memory_avg']:.1f}% max={sm['memory_max']:.1f}%")
    
    if stats.errors:
        print(f"\nErrores: {len(stats.errors)}")
        for err in stats.errors[:5]:
            print(f"  - {err}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    run_load_test()
