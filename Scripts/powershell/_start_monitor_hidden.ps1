# ============================================================================
# Inicia o monitor em segundo plano (oculto)
# ============================================================================

# Pegar caminho raiz do projeto
$scriptPath = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
Set-Location $scriptPath

$pythonExe = "C:\Users\charles.oliveira.AGENCIAPCJ\AppData\Local\Programs\Python\Python313\python.exe"

# Iniciar processo oculto
$process = Start-Process -FilePath $pythonExe `
                         -ArgumentList "scripts\python\monitor_retornos.py" `
                         -WorkingDirectory $scriptPath `
                         -WindowStyle Hidden `
                         -PassThru

Write-Host "`n✅ Monitor iniciado em segundo plano!" -ForegroundColor Green
Write-Host "   PID: $($process.Id)" -ForegroundColor Yellow
Write-Host "`n💡 Use STATUS_MONITOR.bat para verificar`n" -ForegroundColor Cyan
