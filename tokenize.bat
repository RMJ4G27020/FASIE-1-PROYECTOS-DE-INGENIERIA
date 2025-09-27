@echo off
if "%~2"=="" (
    echo Uso: tokenize.bat input-directory output-directory
    exit /b 1
)

python actividad5_tokenize.py "%~1" "%~2"
if errorlevel 1 (
    echo Error al ejecutar el script
    exit /b 1
)

echo.
echo Proceso completado. Revise a5_matricula.txt para ver el reporte.