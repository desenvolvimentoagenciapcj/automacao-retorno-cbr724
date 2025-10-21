$batFile = "D:\Teste_Cobrança_Acess\AutomacaoRetorno\scripts\bat\INICIAR_MONITOR_OCULTO.bat"
$startupFolder = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs\Startup")
$shortcutPath = [System.IO.Path]::Combine($startupFolder, "MonitorAutoInicio.lnk")

Write-Host "CONFIGURANDO INICIALIZACAO VIA STARTUP FOLDER" -ForegroundColor Cyan
Write-Host "BAT: $batFile"
Write-Host "Startup: $startupFolder`n"

if (-not (Test-Path $batFile)) {
    Write-Host "Erro: BAT nao encontrado`n" -ForegroundColor Red
    exit 1
}

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $batFile
    $shortcut.WorkingDirectory = (Split-Path $batFile -Parent)
    $shortcut.WindowStyle = 7
    $shortcut.Description = "Monitor Automatico de Retornos"
    $shortcut.Save()
    
    Write-Host "OK - Shortcut criado em: $shortcutPath`n" -ForegroundColor Green
    
} catch {
    Write-Host "Erro: $_`n" -ForegroundColor Red
    exit 1
}

if (Test-Path $shortcutPath) {
    Write-Host "Verificacao OK - Shortcut existe`n" -ForegroundColor Green
}
