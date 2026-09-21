# start-web.ps1 — Start the Commerce Truth Lab v1 frontend dev server
# Usage: .\scripts\start-web.ps1

$Root = Split-Path -Parent $PSScriptRoot
$WebDir = Join-Path $Root "apps\web"

Write-Host "Starting frontend dev server at http://localhost:5173" -ForegroundColor Cyan
Write-Host "Make sure the API server is running at http://localhost:8000" -ForegroundColor Yellow
Write-Host ""

Set-Location $WebDir
npm run dev
