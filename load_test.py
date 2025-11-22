"""
Fase 5 - Activity 15: Load Testing Script
Pruebas de carga para el motor de búsqueda web

Requisitos de la prueba:
- 25 usuarios concurrentes
- Duración: 15 minutos
- Tiempo de respuesta objetivo: < 2 segundos
- Registrar hasta que CPU o I/O alcance 100%
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
# CONFIGURACIÓN DE LA PRUEBA
# =============================================================================

BASE_URL = "http://localhost:5000"
NUM_USERS = 25
DURATION_MINUTES = 15
MAX_RESPONSE_TIME = 2.0  # segundos

# Directorio para resultados
OUTPUT_DIR = Path("activity15")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consultas de prueba (simulando búsquedas reales)
TEST_QUERIES = [
    "arkansas",
    "lawyer",
    "consumers",
    "United States",
    "laws",
    "court",
    "insurance",
    "government",
    "health",
    "business",
    "tax",
    "education",
    "employment",
    "property",
    "contract",
    "civil rights",
    "criminal law",
    "family law",
    "bankruptcy",
    "immigration"
]

# =============================================================================
# CLASE PARA ESTADÍSTICAS
# =============================================================================

class LoadTestStats:
    """Recolecta y analiza estadísticas de las pruebas de carga"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.requests_sent = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.response_times = []
        self.errors = []
        self.start_time = None
        self.end_time = None
        
        # Métricas por segundo para gráficas
        self.metrics_timeline = defaultdict(lambda: {
            'requests': 0,
            'response_times': [],
            'cpu_percent': 0,
            'memory_percent': 0,
            'io_read': 0,
            'io_write': 0
        })
        
    def record_request(self, success, response_time, error=None):
        """Registra una petición HTTP"""
        with self.lock:
            self.requests_sent += 1
            if success:
                self.requests_success += 1
                self.response_times.append(response_time)
            else:
                self.requests_failed += 1
                if error:
                    self.errors.append(error)
            
            # Registrar en timeline
            current_second = int(time.time() - self.start_time)
            self.metrics_timeline[current_second]['requests'] += 1
            if success:
                self.metrics_timeline[current_second]['response_times'].append(response_time)
    
    def record_system_metrics(self):
        """Registra métricas del sistema"""
        current_second = int(time.time() - self.start_time)
        
        # CPU y memoria
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # I/O (disk)
        io_counters = psutil.disk_io_counters()
        
        with self.lock:
            self.metrics_timeline[current_second]['cpu_percent'] = cpu_percent
            self.metrics_timeline[current_second]['memory_percent'] = memory.percent
            self.metrics_timeline[current_second]['io_read'] = io_counters.read_bytes
            self.metrics_timeline[current_second]['io_write'] = io_counters.write_bytes
    
    def get_summary(self):
        """Genera resumen de estadísticas"""
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
            summary['response_times'] = {
                'min': min(self.response_times),
                'max': max(self.response_times),
                'mean': statistics.mean(self.response_times),
                'median': statistics.median(self.response_times),
                'stdev': statistics.stdev(self.response_times) if len(self.response_times) > 1 else 0,
                'percentile_95': sorted(self.response_times)[int(len(self.response_times) * 0.95)] if self.response_times else 0,
                'percentile_99': sorted(self.response_times)[int(len(self.response_times) * 0.99)] if self.response_times else 0,
                'below_2s': sum(1 for t in self.response_times if t < 2.0) / len(self.response_times) * 100
            }
        
        # Métricas del sistema
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
    """Simula un usuario realizando búsquedas"""
    
    def __init__(self, user_id, stats, stop_event):
        super().__init__()
        self.user_id = user_id
        self.stats = stats
        self.stop_event = stop_event
        self.daemon = True
    
    def run(self):
        """Ejecuta búsquedas hasta que se indique parar"""
        print(f"[Usuario {self.user_id}] Iniciado")
        
        while not self.stop_event.is_set():
            # Seleccionar query aleatoria
            query = random.choice(TEST_QUERIES)
            
            # Realizar búsqueda
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
            
            # Esperar un tiempo aleatorio entre búsquedas (simular usuario real)
            # Entre 1 y 5 segundos
            time.sleep(random.uniform(1, 5))
        
        print(f"[Usuario {self.user_id}] Finalizado")

# =============================================================================
# MONITOR DE SISTEMA
# =============================================================================

class SystemMonitor(threading.Thread):
    """Monitorea CPU, memoria y I/O del sistema"""
    
    def __init__(self, stats, stop_event):
        super().__init__()
        self.stats = stats
        self.stop_event = stop_event
        self.daemon = True
        self.max_cpu_reached = False
        self.max_io_reached = False
    
    def run(self):
        """Monitorea métricas del sistema cada segundo"""
        print("[Monitor] Iniciado")
        
        while not self.stop_event.is_set():
            self.stats.record_system_metrics()
            
            # Verificar si se alcanzó 100% CPU o I/O
            cpu = psutil.cpu_percent(interval=0.1)
            if cpu >= 95:  # Consideramos >= 95% como "100%"
                if not self.max_cpu_reached:
                    print(f"\n[ALERTA] CPU alcanzó {cpu}% - registrando pico")
                    self.max_cpu_reached = True
            
            time.sleep(1)
        
        print("[Monitor] Finalizado")

# =============================================================================
# FUNCIÓN PRINCIPAL DE TESTING
# =============================================================================

def run_load_test():
    """Ejecuta la prueba de carga completa"""
    
    print("="*80)
    print("FASE 5 - ACTIVITY 15: PRUEBA DE CARGA")
    print("="*80)
    print(f"Configuración:")
    print(f"  - Usuarios concurrentes: {NUM_USERS}")
    print(f"  - Duración: {DURATION_MINUTES} minutos")
    print(f"  - Tiempo respuesta máximo: {MAX_RESPONSE_TIME} segundos")
    print(f"  - URL base: {BASE_URL}")
    print("="*80)
    
    # Verificar que el servidor está disponible
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"ERROR: Servidor no responde correctamente en {BASE_URL}")
            return
        print("✓ Servidor web verificado y funcionando")
    except Exception as e:
        print(f"ERROR: No se pudo conectar al servidor: {e}")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        return
    
    # Inicializar estadísticas
    stats = LoadTestStats()
    stats.start_time = time.time()
    
    # Evento para detener threads
    stop_event = threading.Event()
    
    # Iniciar monitor de sistema
    monitor = SystemMonitor(stats, stop_event)
    monitor.start()
    
    # Iniciar usuarios virtuales
    users = []
    for i in range(NUM_USERS):
        user = VirtualUser(i + 1, stats, stop_event)
        user.start()
        users.append(user)
        time.sleep(0.1)  # Pequeña pausa entre inicios
    
    print(f"\n✓ {NUM_USERS} usuarios virtuales iniciados")
    print(f"Ejecutando prueba por {DURATION_MINUTES} minutos...")
    print("Presiona Ctrl+C para detener anticipadamente")
    print("-"*80)
    
    # Ejecutar por la duración especificada
    duration_seconds = DURATION_MINUTES * 60
    start = time.time()
    
    try:
        while time.time() - start < duration_seconds:
            elapsed = int(time.time() - start)
            remaining = duration_seconds - elapsed
            
            # Mostrar progreso cada 10 segundos
            if elapsed % 10 == 0:
                with stats.lock:
                    rps = stats.requests_sent / elapsed if elapsed > 0 else 0
                    success_rate = (stats.requests_success / stats.requests_sent * 100) if stats.requests_sent > 0 else 0
                    
                    print(f"[{elapsed}s] Peticiones: {stats.requests_sent} | RPS: {rps:.2f} | "
                          f"Éxito: {success_rate:.1f}% | Restante: {remaining}s")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario")
    
    # Detener todos los threads
    print("\nDeteniendo usuarios virtuales...")
    stop_event.set()
    
    # Esperar que terminen
    for user in users:
        user.join(timeout=5)
    monitor.join(timeout=5)
    
    stats.end_time = time.time()
    
    # Generar reporte
    print("\n" + "="*80)
    print("GENERANDO REPORTE DE RESULTADOS")
    print("="*80)
    
    summary = stats.get_summary()
    
    # Guardar JSON con resultados completos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = OUTPUT_DIR / f"load_test_{timestamp}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': summary,
            'timeline': dict(stats.metrics_timeline),
            'errors': stats.errors[:100]  # Primeros 100 errores
        }, f, indent=2)
    
    print(f"✓ Resultados guardados en: {json_file}")
    
    # Mostrar resumen en consola
    print("\n" + "="*80)
    print("RESUMEN DE RESULTADOS")
    print("="*80)
    print(f"\nDuración total: {summary['duration_seconds']:.2f} segundos")
    print(f"Peticiones totales: {summary['total_requests']}")
    print(f"Peticiones exitosas: {summary['successful_requests']}")
    print(f"Peticiones fallidas: {summary['failed_requests']}")
    print(f"Tasa de éxito: {summary['success_rate']:.2f}%")
    print(f"Peticiones por segundo: {summary['requests_per_second']:.2f}")
    
    if 'response_times' in summary:
        rt = summary['response_times']
        print(f"\nTiempos de respuesta:")
        print(f"  Mínimo: {rt['min']:.3f}s")
        print(f"  Máximo: {rt['max']:.3f}s")
        print(f"  Promedio: {rt['mean']:.3f}s")
        print(f"  Mediana: {rt['median']:.3f}s")
        print(f"  Desv. estándar: {rt['stdev']:.3f}s")
        print(f"  Percentil 95: {rt['percentile_95']:.3f}s")
        print(f"  Percentil 99: {rt['percentile_99']:.3f}s")
        print(f"  Bajo 2 segundos: {rt['below_2s']:.1f}%")
    
    if 'system_metrics' in summary:
        sm = summary['system_metrics']
        print(f"\nMétricas del sistema:")
        print(f"  CPU promedio: {sm['cpu_avg']:.1f}%")
        print(f"  CPU máxima: {sm['cpu_max']:.1f}%")
        print(f"  Memoria promedio: {sm['memory_avg']:.1f}%")
        print(f"  Memoria máxima: {sm['memory_max']:.1f}%")
    
    print("\n" + "="*80)
    print("PRUEBA COMPLETADA")
    print("="*80)
    
    # Crear archivo de log adicional
    log_file = OUTPUT_DIR / f"load_test_{timestamp}.txt"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FASE 5 - ACTIVITY 15: RESULTADOS DE PRUEBA DE CARGA\n")
        f.write("="*80 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(json.dumps(summary, indent=2))
    
    print(f"✓ Log guardado en: {log_file}")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_load_test()
