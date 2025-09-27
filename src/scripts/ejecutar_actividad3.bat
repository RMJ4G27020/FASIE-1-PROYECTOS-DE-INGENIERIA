@echo off
chcp 65001 >nul
echo ========================================
echo    ACTIVIDAD 3 - EXTRACCIÓN DE PALABRAS
echo ========================================
echo.
echo Este script procesará los archivos HTML limpios
echo para extraer y ordenar palabras alfabéticamente.
echo.
echo Requisitos previos:
echo - Haber ejecutado la Actividad 2 (archivos limpios)
echo - Directorio Clean_Files/ debe existir
echo.
echo Los archivos de palabras se guardarán en Words_Files/
echo.
pause

echo.
echo Iniciando procesamiento de extracción de palabras...
echo.

python actividad3_word_extractor.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo   PROCESAMIENTO COMPLETADO CON ÉXITO
    echo ========================================
    echo.
    echo Archivos generados:
    echo - Words_Files/         ^(archivos de palabras^)
    echo - a3_matricula.txt     ^(reporte de la actividad^)
    echo.
) else (
    echo ========================================
    echo      ERROR EN EL PROCESAMIENTO
    echo ========================================
    echo.
    echo Por favor revisa los mensajes de error anteriores.
    echo Asegúrate de haber ejecutado la Actividad 2 primero.
    echo.
)

echo Presiona cualquier tecla para continuar...
pause >nul
