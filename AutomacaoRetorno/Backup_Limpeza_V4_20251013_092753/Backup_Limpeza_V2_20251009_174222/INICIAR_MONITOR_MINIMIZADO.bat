@echo off
REM ============================================================================
REM Monitor Automático de Retornos Bancários - INICIAR MINIMIZADO
REM ============================================================================

echo.
echo ================================================================================
echo             INICIANDO MONITOR MINIMIZADO
echo ================================================================================
echo.
echo   O monitor vai rodar MINIMIZADO na barra de tarefas
echo.
echo   Para verificar: clique na janela minimizada
echo   Para parar: PARAR_MONITOR.bat ou Ctrl+C na janela
echo.
echo ================================================================================
echo.

REM Aguardar 2 segundos antes de minimizar
timeout /t 2

REM Minimizar esta janela e executar o monitor
start /min cmd /k "@echo off
cd /d "%~dp0" && title Monitor de Retornos - Rodando && color 0A && python monitor_retornos.py"

echo.
echo ✅ Monitor iniciado minimizado!
echo.
echo 💡 A janela está minimizada na barra de tarefas
echo    Clique nela para ver o progresso
echo.
timeout /t 2
