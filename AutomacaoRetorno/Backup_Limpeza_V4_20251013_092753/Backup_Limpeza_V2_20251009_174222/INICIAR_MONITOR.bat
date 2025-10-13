@echo off
REM ============================================================================
REM Monitor Automático de Retornos Bancários - INICIAR
REM ============================================================================

title Monitor de Retornos Bancários - CBR724
cd /d "%~dp0"
color 0A

echo.
echo ================================================================================
echo             MONITOR AUTOMÁTICO DE RETORNOS BANCÁRIOS
echo ================================================================================
echo.
echo   Este monitor processa automaticamente arquivos CBR724 que chegam em:
echo   D:\Teste_Cobrança_Acess\Retorno
echo.
echo   - Arquivos processados: movidos para Processados\
echo   - Arquivos com erro: movidos para Erro\
echo   - Logs: monitor_retornos.log
echo.
echo ================================================================================
echo.
echo   Como deseja iniciar o monitor?
echo.
echo   [1] Janela VISÍVEL (padrão - vê o processamento em tempo real)
echo   [2] Janela MINIMIZADA (fica na barra de tarefas)
echo   [3] OCULTO em segundo plano (totalmente invisível)
echo.
set /p MODO="   Digite 1, 2 ou 3 (Enter = 1): "

if "%MODO%"=="" set MODO=1
if "%MODO%"=="2" goto MINIMIZADO
if "%MODO%"=="3" goto OCULTO

:VISIVEL
echo.
echo ================================================================================
echo.
echo   Iniciando monitor em modo VISÍVEL...
echo.
cd /d "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
python monitor_retornos.py
pause
exit

:MINIMIZADO
echo.
echo ✅ Iniciando monitor MINIMIZADO na barra de tarefas...
timeout /t 2 /nobreak >nul
start /min cmd /k "cd /d D:\Teste_Cobrança_Acess\AutomacaoRetorno && title Monitor de Retornos - Rodando && color 0A && python monitor_retornos.py"
echo.
echo ✅ Monitor iniciado! A janela está minimizada na barra de tarefas.
echo.
timeout /t 3
exit

:OCULTO
echo.
echo ✅ Iniciando monitor OCULTO em segundo plano...
cd /d "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\RunHidden.vbs"
echo WshShell.Run "cmd /c cd /d ""D:\Teste_Cobrança_Acess\AutomacaoRetorno"" ^&^& python monitor_retornos.py", 0, False >> "%TEMP%\RunHidden.vbs"
cscript //nologo "%TEMP%\RunHidden.vbs"
del "%TEMP%\RunHidden.vbs"
echo.
echo ✅ Monitor rodando em segundo plano (totalmente oculto)!
echo.
echo 💡 Use STATUS_MONITOR.bat para verificar se está rodando
echo 💡 Use PARAR_MONITOR.bat para parar
echo.
timeout /t 4
exit
