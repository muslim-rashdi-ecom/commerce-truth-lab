# start-api.ps1 — Start the Commerce Truth Lab v1 API server
# Usage: .\scripts\start-api.ps1

$Root = Split-Path -Parent $PSScriptRoot
$ApiDir = Join-Path $Root "apps\api"
$PackagesDir = Join-Path $Root "packages"

# Check if DB exists; if not, seed it
$DbPath = Join-Path $Root "data\demo.db"
if (-not (Test-Path $DbPath)) {
    Write-Host "Seeding database..." -ForegroundColor Yellow
    Set-Location $ApiDir
    $env:PYTHONPATH = "$PackagesDir;$ApiDir"
    python seed.py
}

Write-Host "Starting API server at http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Set-Location $ApiDir
$env:PYTHONPATH = "$PackagesDir;$ApiDir"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
