@echo off
REM ============================================================================
REM Monitor Automático de Retornos Bancários - PARAR TODOS OS MONITORES
REM ============================================================================

cd /d "%~dp0\..\.."

echo.
echo ================================================================================
echo             PARAR MONITOR DE RETORNOS
echo ================================================================================
echo.

REM Usar script PowerShell centralizado para parar monitores
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "scripts\powershell\_stop_all_monitors.ps1"

echo ================================================================================
echo   Monitor(es) parado(s) com sucesso!
echo ================================================================================
echo.
echo   Para reiniciar: INICIAR_MONITOR_OCULTO.bat
echo.
timeout /t 5
