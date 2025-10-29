@echo off
REM ============================================================================
REM Inicia o Watchdog do Monitor (monitora se o monitor caiu e reinicia)
REM ============================================================================

cd /d "%~dp0\..\.."

echo.
echo ================================================================================
echo             INICIANDO WATCHDOG DO MONITOR
echo ================================================================================
echo.
echo   O watchdog monitora se o monitor de retornos esta rodando.
echo   Se detectar que o monitor caiu, reinicia automaticamente.
echo.
echo   Intervalo de verificacao: 60 segundos
echo   Maximo de tentativas: 3
echo.
echo ================================================================================
echo.

REM Iniciar em segundo plano usando PowerShell
powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "Set-Location (Get-Location); python scripts\python\watchdog_monitor.py"

echo.
echo   Watchdog iniciado em segundo plano!
echo.
echo   Para verificar logs: watchdog.log
echo   Para parar: PARAR_WATCHDOG.bat
echo.
timeout /t 3
