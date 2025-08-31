@echo off
echo ========================================
echo PROYECTO ING - PROCESAMIENTO DE HTML
echo ========================================
echo.
echo Selecciona la actividad a ejecutar:
echo.
echo 1. Actividad 1 - Medicion de tiempos de apertura
echo 2. Actividad 2 - Eliminacion de etiquetas HTML  
echo 3. Ejecutar ambas actividades
echo 4. Ver reportes generados
echo 5. Salir
echo.
set /p choice="Ingresa tu opcion (1-5): "

if "%choice%"=="1" goto actividad1
if "%choice%"=="2" goto actividad2
if "%choice%"=="3" goto ambas
if "%choice%"=="4" goto reportes
if "%choice%"=="5" goto salir
goto menu

:actividad1
echo.
echo ========================================
echo EJECUTANDO ACTIVIDAD 1
echo ========================================
python buscador_html.py
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:actividad2
echo.
echo ========================================
echo EJECUTANDO ACTIVIDAD 2
echo ========================================
python actividad2_html_cleaner.py
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:ambas
echo.
echo ========================================
echo EJECUTANDO AMBAS ACTIVIDADES
echo ========================================
echo.
echo --- Ejecutando Actividad 1 ---
python buscador_html.py
echo.
echo --- Ejecutando Actividad 2 ---
python actividad2_html_cleaner.py
echo.
echo Ambas actividades completadas!
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:reportes
echo.
echo ========================================
echo REPORTES GENERADOS
echo ========================================
echo.
if exist "a1_*.txt" (
    echo === ACTIVIDAD 1 - REPORTE DE TIEMPOS ===
    for %%f in (a1_*.txt) do type "%%f" | head -20
    echo ... (truncado)
    echo.
)

if exist "a2_*.txt" (
    echo === ACTIVIDAD 2 - REPORTE DE ELIMINACION HTML ===
    for %%f in (a2_*.txt) do type "%%f" | head -20
    echo ... (truncado)
    echo.
)

echo === ARCHIVOS LIMPIOS GENERADOS ===
if exist "Clean_Files" (
    dir Clean_Files /b | head -10
    echo ... (506 archivos totales en Clean_Files/)
) else (
    echo No se encontraron archivos limpios
)

echo.
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:salir
echo.
echo Gracias por usar el programa!
echo.
exit

:menu
cls
goto inicio

:inicio
echo ========================================
echo PROYECTO ING - PROCESAMIENTO DE HTML
echo ========================================
echo.
echo Selecciona la actividad a ejecutar:
echo.
echo 1. Actividad 1 - Medicion de tiempos de apertura
echo 2. Actividad 2 - Eliminacion de etiquetas HTML  
echo 3. Ejecutar ambas actividades
echo 4. Ver reportes generados
echo 5. Salir
echo.
set /p choice="Ingresa tu opcion (1-5): "

if "%choice%"=="1" goto actividad1
if "%choice%"=="2" goto actividad2
if "%choice%"=="3" goto ambas
if "%choice%"=="4" goto reportes
if "%choice%"=="5" goto salir

echo Opcion invalida. Presiona cualquier tecla para intentar de nuevo...
pause > nul
goto menu
