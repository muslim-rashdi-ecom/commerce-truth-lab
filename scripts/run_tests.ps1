# run_tests.ps1 — Run all engine tests with correct Python path
# Usage: .\scripts\run_tests.ps1

$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$Root\packages;$Root\apps\api"

Write-Host "=== Commerce Truth Lab v1 — Engine Tests ===" -ForegroundColor Cyan
Write-Host "PYTHONPATH: $env:PYTHONPATH"
Write-Host ""

Set-Location $Root
python -m pytest tests/engine/ -v --tb=short

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
