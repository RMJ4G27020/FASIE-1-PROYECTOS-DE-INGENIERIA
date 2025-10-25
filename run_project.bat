@echo off
REM Script para ejecutar las actividades con la nueva estructura
echo === Sistema de Procesamiento HTML ===
echo.
echo Estructura reorganizada del proyecto:
echo - src/activities/    : Modulos principales
echo - src/config/       : Configuracion
echo - data/input/       : Archivos HTML de entrada
echo - data/output/      : Resultados procesados
echo.

:menu
echo 1. Ejecutar Actividad 4 (Consolidacion)
echo 2. Ejecutar Actividad 5 (Tokenizacion)
echo 3. Ejecutar Actividad 6 (Diccionario)
echo 4. Ejecutar todas las actividades
echo 5. Abrir launcher interactivo
echo 0. Salir
echo.
set /p choice="Seleccione una opcion: "

if "%choice%"=="1" goto activity4
if "%choice%"=="2" goto activity5
if "%choice%"=="3" goto activity6
if "%choice%"=="4" goto all_activities
if "%choice%"=="5" goto launcher
if "%choice%"=="0" goto exit
goto menu

:activity4
echo Ejecutando Actividad 4...
python src/activities/actividad4_consolidate_words.py
pause
goto menu

:activity5
echo Ejecutando Actividad 5...
python src/activities/actividad5_tokenize.py
pause
goto menu

:activity6
echo Ejecutando Actividad 6...
python src/activities/actividad6_dictionary.py
pause
goto menu

:all_activities
echo Ejecutando todas las actividades...
python src/activities/actividad4_consolidate_words.py
python src/activities/actividad5_tokenize.py
python src/activities/actividad6_dictionary.py
pause
goto menu

:launcher
echo Iniciando launcher interactivo...
python launcher.py
pause
goto menu

:exit
echo Saliendo...
exit /b 0