@echo off
echo ========================================
echo ACTIVIDAD 2 - REMOVER ETIQUETAS HTML
echo ========================================
echo.
echo Ejecutando el programa...
echo.

python actividad2_html_cleaner.py

echo.
echo Presiona cualquier tecla para ver el reporte...
pause > nul

if exist "a2_*.txt" (
    for %%f in (a2_*.txt) do (
        echo.
        echo === CONTENIDO DEL REPORTE ===
        type "%%f"
        echo.
        echo === FIN DEL REPORTE ===
    )
) else (
    echo No se encontro archivo de reporte
)

echo.
echo Presiona cualquier tecla para ver algunos archivos limpios...
pause > nul

if exist "Clean_Files" (
    echo.
    echo === ARCHIVOS GENERADOS ===
    dir Clean_Files /b | head -10
    echo.
    echo === EJEMPLO DE CONTENIDO LIMPIO ===
    if exist "Clean_Files\002_clean.txt" (
        echo --- Contenido de 002_clean.txt (primeras 10 lineas) ---
        type "Clean_Files\002_clean.txt" | head -10
        echo --- (truncado) ---
    )
) else (
    echo No se encontro directorio Clean_Files
)

echo.
pause
