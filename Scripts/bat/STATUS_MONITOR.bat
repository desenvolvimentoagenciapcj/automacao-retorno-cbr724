@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

cd /d "%~dp0\..\.."

REM Ler configurações do config.ini
for /f "delims=" %%i in ('powershell -ExecutionPolicy Bypass -File "scripts\powershell\_read_config.ps1" -Secao "CAMINHOS" -Chave "pasta_retorno"') do set PASTA_RETORNO=%%i
for /f "delims=" %%i in ('powershell -ExecutionPolicy Bypass -File "scripts\powershell\_read_config.ps1" -Secao "CAMINHOS" -Chave "pasta_processados"') do set PASTA_PROCESSADOS=%%i

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  STATUS DO MONITOR DE RETORNOS                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se há processo rodando usando PowerShell
for /f "delims=" %%i in ('powershell -ExecutionPolicy Bypass -File "scripts\powershell\_check_monitor.ps1"') do (
    set FOUND=1
    set PID=%%i
    goto :SHOW_RUNNING
)

:SHOW_STOPPED
echo ⭕ STATUS: PARADO
echo.
echo 📂 Pasta monitorada: %PASTA_RETORNO%
echo 🔴 O monitor NÃO está processando arquivos automaticamente
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 Para iniciar: INICIAR_MONITOR.bat
echo.
goto :END

:SHOW_RUNNING
echo ✅ STATUS: RODANDO (Aguardando arquivos ou processando)
echo.
echo 📂 Pasta monitorada: %PASTA_RETORNO%
echo 🟢 Monitor ATIVO - Processa arquivos automaticamente quando detectados
echo 🆔 PID do processo: %PID%
echo.

REM Verificar tempo de execução
for /f "tokens=2,3" %%a in ('tasklist /FI "PID eq %PID%" /FO LIST ^| findstr /I "Tempo"') do (
    echo ⏱️  Tempo rodando: %%a %%b
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Verificar última atividade no log
if exist "monitor_retornos.log" (
    echo 📝 Última atividade registrada:
    echo.
    for /f "usebackq delims=" %%a in (`powershell -command "Get-Content 'monitor_retornos.log' -Tail 3 | Select-Object -First 1"`) do (
        echo    %%a
    )
    echo.
    echo    (Para ver mais detalhes, abra: monitor_retornos.log)
    echo.
) else (
    echo 📝 Nenhuma atividade registrada ainda (log não existe)
    echo.
)

echo ════════════════════════════════════════════════════════════════
echo.

REM Verificar arquivos processados recentemente
if exist "%PASTA_PROCESSADOS%\*.ret" (
    echo 📊 Últimos arquivos processados:
    echo.
    for /f "delims=" %%f in ('dir /b /o-d "%PASTA_PROCESSADOS%\*.ret" 2^>nul') do (
        echo    ✓ %%f
    )
    echo.
) else (
    echo 📊 Nenhum arquivo processado ainda
    echo.
)

echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 Para parar: PARAR_MONITOR.bat
echo 💡 Ver log: monitor_retornos.log
echo.

:END
pause
