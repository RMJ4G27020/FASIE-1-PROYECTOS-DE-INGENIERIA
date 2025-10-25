@echo off
chcp 65001 >nul

:menu
cls
echo ========================================
echo PROYECTO ING - PROCESAMIENTO DE HTML
echo ========================================
echo.
echo Selecciona la actividad a ejecutar:
echo.
echo 1. Actividad 1 - Medicion de tiempos de apertura
echo 2. Actividad 2 - Eliminacion de etiquetas HTML  
echo 3. Actividad 3 - Extraccion y ordenamiento de palabras
echo 4. Ejecutar todas las actividades
echo 5. Ver reportes generados
echo 6. Salir
echo.
set /p choice="Ingresa tu opcion (1-6): "

if "%choice%"=="1" goto actividad1
if "%choice%"=="2" goto actividad2
if "%choice%"=="3" goto actividad3
if "%choice%"=="4" goto todas
if "%choice%"=="5" goto reportes
if "%choice%"=="6" goto salir
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

:actividad3
echo.
echo ========================================
echo EJECUTANDO ACTIVIDAD 3
echo ========================================
python actividad3_word_extractor.py
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:todas
echo.
echo ========================================
echo EJECUTANDO TODAS LAS ACTIVIDADES
echo ========================================
echo.
echo --- Ejecutando Actividad 1 ---
python buscador_html.py
echo.
echo --- Ejecutando Actividad 2 ---
python actividad2_html_cleaner.py
echo.
echo --- Ejecutando Actividad 3 ---
python actividad3_word_extractor.py
echo.
echo Todas las actividades completadas!
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
    for %%f in (a1_*.txt) do echo Archivo: %%f
    echo.
)
if exist "a2_*.txt" (
    echo === ACTIVIDAD 2 - REPORTE DE LIMPIEZA ===
    for %%f in (a2_*.txt) do echo Archivo: %%f
    echo.
)
if exist "a3_*.txt" (
    echo === ACTIVIDAD 3 - REPORTE DE PALABRAS ===
    for %%f in (a3_*.txt) do echo Archivo: %%f
    echo.
)
echo Directorios generados:
if exist "Clean_Files" echo - Clean_Files/ ^(archivos sin etiquetas HTML^)
if exist "Words_Files" echo - Words_Files/ ^(archivos de palabras ordenadas^)
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
goto menu

:salir
echo.
echo Gracias por usar el procesador de archivos HTML!
echo.
exit
