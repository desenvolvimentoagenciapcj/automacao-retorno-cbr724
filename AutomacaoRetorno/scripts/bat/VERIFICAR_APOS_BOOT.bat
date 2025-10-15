@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM Script executado 10 minutos após boot para verificar se monitor iniciou

cd /d "%~dp0..\.."

REM Verificar se monitor está rodando
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH ^| find "python.exe"') do (
    for /f "tokens=*" %%a in ('wmic process where "ProcessId=%%~i" get CommandLine /format:list ^| find "monitor_retornos.py"') do (
        REM Monitor está rodando - tudo OK
        echo %date% %time% - Monitor verificado apos boot - OK >> "%~dp0..\..\logs\boot_check.log"
        exit /b 0
    )
)

REM Monitor NÃO está rodando - problema!
echo %date% %time% - ALERTA: Monitor NAO iniciou apos boot! >> "%~dp0..\..\logs\boot_check.log"

REM Tentar iniciar manualmente
echo %date% %time% - Tentando iniciar monitor... >> "%~dp0..\..\logs\boot_check.log"
call "%~dp0INICIAR_MONITOR_OCULTO.bat"

timeout /t 5 /nobreak >nul

REM Verificar novamente
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH ^| find "python.exe"') do (
    for /f "tokens=*" %%a in ('wmic process where "ProcessId=%%~i" get CommandLine /format:list ^| find "monitor_retornos.py"') do (
        echo %date% %time% - Monitor iniciado com sucesso apos tentativa manual >> "%~dp0..\..\logs\boot_check.log"
        
        REM Notificar sucesso
        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "Add-Type -AssemblyName System.Windows.Forms; ^
        $notification = New-Object System.Windows.Forms.NotifyIcon; ^
        $notification.Icon = [System.Drawing.SystemIcons]::Information; ^
        $notification.BalloonTipTitle = 'Monitor Iniciado'; ^
        $notification.BalloonTipText = 'Sistema recuperado após reinicialização do Windows'; ^
        $notification.Visible = $true; ^
        $notification.ShowBalloonTip(5000); ^
        Start-Sleep -Seconds 6; ^
        $notification.Dispose()"
        
        exit /b 0
    )
)

REM Falhou - notificar erro crítico
echo %date% %time% - ERRO CRITICO: Falha ao iniciar monitor mesmo apos tentativa manual >> "%~dp0..\..\logs\boot_check.log"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Add-Type -AssemblyName System.Windows.Forms; ^
$notification = New-Object System.Windows.Forms.NotifyIcon; ^
$notification.Icon = [System.Drawing.SystemIcons]::Error; ^
$notification.BalloonTipTitle = 'ERRO: Monitor Não Iniciou'; ^
$notification.BalloonTipText = 'Sistema não iniciou após reinicialização. Execute INICIAR.bat manualmente!'; ^
$notification.Visible = $true; ^
$notification.ShowBalloonTip(10000); ^
Start-Sleep -Seconds 11; ^
$notification.Dispose()"

REM Enviar email de alerta se configurado
python "%~dp0..\python\notificar_erro_boot.py" >nul 2>&1

exit /b 1
