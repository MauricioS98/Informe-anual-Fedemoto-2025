@echo off
chcp 65001 >nul
REM Script para generar un informe completo desde un Excel
REM Uso: generar_informe_completo.bat <ruta_excel> [nombre_valida]

if "%~1"=="" (
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   Generador de Informes FEDEMOTO
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Uso: generar_informe_completo.bat ^<ruta_excel^> [nombre_valida]
    echo.
    echo Ejemplos:
    echo   generar_informe_completo.bat "Informes\Modalidad de ejemplo\valejempo.xlsx"
    echo   generar_informe_completo.bat "Informes\Motocross\Primer semestre\valejempo.xlsx" "Motocross 1er semestre"
    echo.
    echo Si no especificas el nombre de la válida, se usará el nombre del archivo Excel.
    echo.
    pause
    exit /b 1
)

set EXCEL_PATH=%~1
set NOMBRE_VALIDA=%~2

REM Verificar que el archivo Excel existe
if not exist "%EXCEL_PATH%" (
    echo.
    echo [ERROR] No se encontró el archivo Excel: %EXCEL_PATH%
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   Generador de Informes FEDEMOTO
echo ═══════════════════════════════════════════════════════════
echo.

REM Obtener el directorio del Excel y el nombre base
for %%F in ("%EXCEL_PATH%") do (
    set EXCEL_DIR=%%~dpF
    set EXCEL_NAME=%%~nF
)

REM Si no se especificó nombre de válida, usar el nombre del archivo
if "%NOMBRE_VALIDA%"=="" (
    set NOMBRE_VALIDA=%EXCEL_NAME%
)

REM Generar nombres de archivos JSON y HTML
set JSON_PATH=%EXCEL_DIR%datos_%EXCEL_NAME%.json
set HTML_PATH=%EXCEL_DIR%informe_%EXCEL_NAME%.html

echo [INFO] Archivo Excel: %EXCEL_PATH%
echo [INFO] Nombre de válida: %NOMBRE_VALIDA%
echo [INFO] JSON temporal: %JSON_PATH%
echo [INFO] HTML final: %HTML_PATH%
echo.

REM Paso 1: Analizar el Excel
echo ═══════════════════════════════════════════════════════════
echo   PASO 1: Analizando Excel...
echo ═══════════════════════════════════════════════════════════
echo.

python "Informes\analizar_valida.py" "%EXCEL_PATH%" "%JSON_PATH%"

if errorlevel 1 (
    echo.
    echo [ERROR] Falló el análisis del Excel. Verifica el archivo y vuelve a intentar.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Análisis completado. JSON generado: %JSON_PATH%
echo.

REM Paso 2: Generar el HTML
echo ═══════════════════════════════════════════════════════════
echo   PASO 2: Generando informe HTML...
echo ═══════════════════════════════════════════════════════════
echo.

python "Informes\generar_informe.py" "%JSON_PATH%" "%HTML_PATH%" "%NOMBRE_VALIDA%"

if errorlevel 1 (
    echo.
    echo [ERROR] Falló la generación del HTML. Verifica los datos y vuelve a intentar.
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   ¡PROCESO COMPLETADO!
echo ═══════════════════════════════════════════════════════════
echo.
echo [OK] Informe generado exitosamente: %HTML_PATH%
echo [OK] El menú ha sido actualizado en todos los archivos HTML
echo.
echo Puedes abrir el informe en tu navegador.
echo.
pause

