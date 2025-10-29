Write-Host "`n===================================================================="
Write-Host "     DIAGNOSTICO AUTO-START DO MONITOR"
Write-Host "===================================================================="

# Verificar Registry Startup
Write-Host "`n1. REGISTRY STARTUP:" -ForegroundColor Cyan
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$regEntry = Get-ItemProperty -Path $regPath -Name "MonitorAutoInicio" -ErrorAction SilentlyContinue
if ($regEntry) {
    Write-Host "   [OK] Configurado no Registro" -ForegroundColor Green
    Write-Host "   Local: $regPath" -ForegroundColor Yellow
} else {
    Write-Host "   [ERRO] NAO encontrado no Registro" -ForegroundColor Red
}

# Verificar Task Scheduler
Write-Host "`n2. TASK SCHEDULER:" -ForegroundColor Cyan
$task = Get-ScheduledTask -TaskPath "\AutomacaoRetorno\" -TaskName "MonitorAutoInicio" -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "   [OK] Task existe" -ForegroundColor Green
    Write-Host "   Estado: $($task.State)" -ForegroundColor Yellow
} else {
    Write-Host "   [INFO] Task nao existe (Registry Startup eh suficiente)" -ForegroundColor Cyan
}

# Verificar monitor
Write-Host "`n3. MONITOR RODANDO:" -ForegroundColor Cyan
$proc = Get-Process -Name python, pythonw -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*monitor*" }
if ($proc) {
    Write-Host "   [OK] Monitor ativo (PID: $($proc.Id))" -ForegroundColor Green
} else {
    Write-Host "   [PARADO] Monitor nao encontrado" -ForegroundColor Yellow
}

Write-Host "`n===================================================================="
Write-Host "PRONTO: Reinicie o PC para testar a auto-inicializacao"
Write-Host "====================================================================`n"

