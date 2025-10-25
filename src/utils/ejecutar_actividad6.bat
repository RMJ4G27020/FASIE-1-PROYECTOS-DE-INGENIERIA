@echo off
if "%~2"=="" (
    echo Uso: ejecutar_actividad6.bat input-directory output-directory
    exit /b 1
)

python actividad6_dictionary.py "%~1" "%~2"
if errorlevel 1 (
    echo Error al ejecutar el script
    exit /b 1
)

echo.
echo Proceso completado. Revise a6_matricula.txt para ver el reporte.