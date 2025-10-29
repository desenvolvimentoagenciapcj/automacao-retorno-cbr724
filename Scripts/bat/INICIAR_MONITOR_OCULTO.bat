@echo off
REM ============================================================================
REM Monitor Automático de Retornos Bancários - INICIAR EM SEGUNDO PLANO
REM ============================================================================

cd /d "%~dp0\..\.."

REM Ler diretório de trabalho do config.ini
for /f "delims=" %%i in ('powershell -ExecutionPolicy Bypass -File "scripts\powershell\_read_config.ps1" -Secao "DIRETORIOS" -Chave "dir_trabalho"') do set DIR_TRABALHO=%%i

echo.
echo ================================================================================
echo             INICIANDO MONITOR EM SEGUNDO PLANO
echo ================================================================================
echo.
echo   O monitor vai rodar OCULTO em segundo plano
echo.
echo   Para verificar se esta rodando: STATUS_MONITOR.bat
echo   Para parar o monitor: PARAR_MONITOR.bat
echo.
echo ================================================================================
echo.

cd /d "%DIR_TRABALHO%" 2>nul

REM PASSO 1: Parar todos os monitores antigos (evita processos órfãos)
echo [1/2] Verificando monitores antigos...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "scripts\powershell\_stop_all_monitors.ps1"

REM PASSO 2: Iniciar monitor usando PowerShell (mais confiável que VBScript)
echo [2/2] Iniciando novo monitor...
echo.
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "scripts\powershell\_start_monitor_hidden.ps1"

REM Aguardar 3 segundos para o monitor iniciar
timeout /t 3 /nobreak >nul

echo.
echo ✅ Monitor iniciado em segundo plano!
echo.
echo 💡 Dicas:
echo    - Execute STATUS_MONITOR.bat para verificar se está rodando
echo    - Execute PARAR_MONITOR.bat para parar o monitor
echo    - Veja o log em: monitor_retornos.log
echo.
timeout /t 3
