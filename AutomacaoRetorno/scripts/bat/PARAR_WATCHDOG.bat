@echo off
REM ============================================================================
REM Para o Watchdog do Monitor
REM ============================================================================

cd /d "%~dp0\..\.."

echo.
echo ================================================================================
echo             PARANDO WATCHDOG DO MONITOR
echo ================================================================================
echo.

powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match 'watchdog' -or ($_.CommandLine -and $_.CommandLine -match 'watchdog_monitor\.py') } | ForEach-Object { Write-Host \"  Parando processo PID: $($_.Id)\"; Stop-Process -Id $_.Id -Force }"

echo.
echo   Watchdog parado!
echo.
timeout /t 3
