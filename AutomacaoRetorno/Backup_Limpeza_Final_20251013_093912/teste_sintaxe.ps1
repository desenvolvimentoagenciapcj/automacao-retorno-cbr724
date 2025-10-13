Write-Host "Teste 1" -ForegroundColor Cyan

if (Test-Path "config.ini") {
    Write-Host "   Config existe" -ForegroundColor Green
}

if (Test-Path "README.md") {
    Write-Host "   README existe" -ForegroundColor Green
}

Write-Host "Teste concluído" -ForegroundColor Yellow
