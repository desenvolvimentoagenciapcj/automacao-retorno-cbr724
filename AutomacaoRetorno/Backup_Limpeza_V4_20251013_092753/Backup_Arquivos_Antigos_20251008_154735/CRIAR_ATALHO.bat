@echo off
REM ============================================================================
REM Criar Atalho na Área de Trabalho - Monitor de Retornos
REM ============================================================================

echo.
echo Criando atalho na área de trabalho...
echo.

set SCRIPT="%TEMP%\CreateShortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.SpecialFolders("Desktop") + "\Monitor de Retornos.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "D:\Teste_Cobrança_Acess\AutomacaoRetorno\INICIAR_MONITOR.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "D:\Teste_Cobrança_Acess\AutomacaoRetorno" >> %SCRIPT%
echo oLink.Description = "Monitor Automático de Retornos Bancários" >> %SCRIPT%
echo oLink.IconLocation = "shell32.dll,16" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo ✓ Atalho criado na área de trabalho!
echo.
pause
