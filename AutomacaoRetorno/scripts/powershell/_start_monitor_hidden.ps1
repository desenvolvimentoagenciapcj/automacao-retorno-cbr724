# ============================================================================
# Inicia o monitor em segundo plano (oculto - VERSAO SILENCIOSA)
# ============================================================================

$scriptPath = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
Set-Location $scriptPath

$pythonExe = "C:\Users\charles.oliveira.AGENCIAPCJ\AppData\Local\Programs\Python\Python313\python.exe"

# Iniciar processo oculto - SEM OUTPUT
$process = Start-Process -FilePath $pythonExe `
                         -ArgumentList "scripts\python\monitor_retornos.py" `
                         -WorkingDirectory $scriptPath `
                         -WindowStyle Hidden `
                         -RedirectStandardOutput ([System.IO.Path]::GetTempPath() + "monitor_null.log") `
                         -RedirectStandardError ([System.IO.Path]::GetTempPath() + "monitor_null.log") `
                         -PassThru
