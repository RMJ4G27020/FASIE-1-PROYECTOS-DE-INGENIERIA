@echo off
echo ========================================
echo BUSCADOR HTML - MEDICION DE TIEMPOS
echo ========================================
echo.
echo Ejecutando el programa...
echo.

python buscador_html.py

echo.
echo Presiona cualquier tecla para ver el reporte...
pause > nul

if exist "a1_*.txt" (
    for %%f in (a1_*.txt) do (
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
pause
