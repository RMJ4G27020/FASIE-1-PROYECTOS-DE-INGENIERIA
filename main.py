"""
Script principal para ejecutar las actividades del proyecto
Análisis de Archivos HTML - Proyectos de Ingeniería
FASIE-1-PROYECTOS-DE-INGENIERIA
"""
import os
import sys

def show_menu():
    """Muestra el menú principal del proyecto"""
    print("\n" + "=" * 60)
    print("🎓 PROYECTO DE ANÁLISIS DE ARCHIVOS HTML")
    print("   Proyectos de Ingeniería - FASIE")
    print("=" * 60)
    print("📋 ACTIVIDADES DISPONIBLES:")
    print("   1️⃣  Actividad 1 - Medición de tiempos de apertura")
    print("   2️⃣  Actividad 2 - Eliminación de etiquetas HTML") 
    print("   3️⃣  Actividad 3 - Extracción y ordenamiento de palabras")
    print("   4️⃣  Ejecutar todas las actividades")
    print("   5️⃣  Ver reportes generados")
    print("   6️⃣  Configurar matrícula")
    print("   0️⃣  Salir")
    print("=" * 60)

def run_activity(activity_num):
    """Ejecuta una actividad específica"""
    activities = {
        1: "src/actividades/actividad1_file_timer.py",
        2: "src/actividades/actividad2_html_cleaner.py", 
        3: "src/actividades/actividad3_word_extractor.py"
    }
    
    if activity_num in activities:
        script_path = activities[activity_num]
        if os.path.exists(script_path):
            print(f"\n🚀 Ejecutando Actividad {activity_num}...")
            os.system(f"python {script_path}")
        else:
            print(f"❌ Error: No se encontró el archivo {script_path}")
    else:
        print("❌ Actividad no válida")

def run_all_activities():
    """Ejecuta todas las actividades en secuencia"""
    print("\n🚀 Ejecutando todas las actividades...")
    for i in range(1, 4):
        print(f"\n{'='*40}")
        print(f"📋 INICIANDO ACTIVIDAD {i}")
        print(f"{'='*40}")
        run_activity(i)
        input("\n⏸️  Presiona Enter para continuar con la siguiente actividad...")

def show_reports():
    """Muestra los reportes generados"""
    reports_dir = "data/output/reports"
    if os.path.exists(reports_dir):
        reports = [f for f in os.listdir(reports_dir) if f.endswith('.txt')]
        if reports:
            print(f"\n📊 REPORTES GENERADOS:")
            print("-" * 40)
            for report in sorted(reports):
                print(f"   📄 {report}")
            print("-" * 40)
            print(f"📁 Ubicación: {reports_dir}/")
        else:
            print("\n📭 No se encontraron reportes. Ejecuta primero las actividades.")
    else:
        print("\n❌ Directorio de reportes no encontrado.")

def configure_matricula():
    """Permite configurar la matrícula del estudiante"""
    config_path = "src/utils/config.py"
    if os.path.exists(config_path):
        print("\n⚙️  CONFIGURACIÓN DE MATRÍCULA")
        print("-" * 40)
        matricula = input("🎓 Ingresa tu matrícula: ").strip()
        
        if matricula:
            # Leer el archivo actual
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar la matrícula
            import re
            new_content = re.sub(
                r'MATRICULA = "[^"]*"',
                f'MATRICULA = "{matricula}"',
                content
            )
            
            # Escribir el archivo actualizado
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Matrícula actualizada a: {matricula}")
        else:
            print("❌ Matrícula no válida")
    else:
        print("❌ Archivo de configuración no encontrado")

def main():
    """Función principal del menú interactivo"""
    while True:
        show_menu()
        
        try:
            choice = input("\n🎯 Selecciona una opción: ").strip()
            
            if choice == "0":
                print("\n👋 ¡Hasta luego!")
                break
            elif choice == "1":
                run_activity(1)
            elif choice == "2":
                run_activity(2)
            elif choice == "3":
                run_activity(3)
            elif choice == "4":
                run_all_activities()
            elif choice == "5":
                show_reports()
            elif choice == "6":
                configure_matricula()
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\n⏸️  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
