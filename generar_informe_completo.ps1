# Script PowerShell para generar un informe completo desde un Excel
# Uso: .\generar_informe_completo.ps1 <ruta_excel> [nombre_valida]

param(
    [Parameter(Mandatory=$true)]
    [string]$ExcelPath,
    
    [Parameter(Mandatory=$false)]
    [string]$NombreValida = ""
)

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Generador de Informes FEDEMOTO" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Verificar que el archivo Excel existe
if (-not (Test-Path $ExcelPath)) {
    Write-Host "[ERROR] No se encontró el archivo Excel: $ExcelPath" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Obtener el directorio y nombre del Excel
$excelFile = Get-Item $ExcelPath
$excelDir = $excelFile.DirectoryName
$excelName = $excelFile.BaseName

# Si no se especificó nombre de válida, usar el nombre del archivo
if ([string]::IsNullOrWhiteSpace($NombreValida)) {
    $NombreValida = $excelName
}

# Generar nombres de archivos JSON y HTML
$jsonPath = Join-Path $excelDir "datos_$excelName.json"
$htmlPath = Join-Path $excelDir "informe_$excelName.html"

Write-Host "[INFO] Archivo Excel: $ExcelPath" -ForegroundColor Yellow
Write-Host "[INFO] Nombre de válida: $NombreValida" -ForegroundColor Yellow
Write-Host "[INFO] JSON temporal: $jsonPath" -ForegroundColor Yellow
Write-Host "[INFO] HTML final: $htmlPath" -ForegroundColor Yellow
Write-Host ""

# Paso 1: Analizar el Excel
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PASO 1: Analizando Excel..." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Join-Path $PSScriptRoot "Informes\analizar_valida.py"
$result1 = & python $scriptPath $ExcelPath $jsonPath

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Falló el análisis del Excel. Verifica el archivo y vuelve a intentar." -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "[OK] Análisis completado. JSON generado: $jsonPath" -ForegroundColor Green
Write-Host ""

# Paso 2: Generar el HTML
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PASO 2: Generando informe HTML..." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$scriptPath2 = Join-Path $PSScriptRoot "Informes\generar_informe.py"
$result2 = & python $scriptPath2 $jsonPath $htmlPath $NombreValida

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Falló la generación del HTML. Verifica los datos y vuelve a intentar." -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ¡PROCESO COMPLETADO!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "[OK] Informe generado exitosamente: $htmlPath" -ForegroundColor Green
Write-Host "[OK] El menú ha sido actualizado en todos los archivos HTML" -ForegroundColor Green
Write-Host ""
Write-Host "Puedes abrir el informe en tu navegador." -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para salir"

