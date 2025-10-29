@echo off
REM Teste da nova funcionalidade de verificação de arquivos no agendador
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   TESTE: Verificação de Arquivos
echo   Agendador às 8h30
echo ========================================
echo.

REM Lê o caminho do Python do config.ini
for /f "tokens=2 delims==" %%a in ('findstr /i "^executavel" "config\config.ini"') do set PYTHON_PATH=%%a
set PYTHON_PATH=%PYTHON_PATH: =%

echo 🔍 Testando nova funcionalidade...
echo.

REM Executa o agendador em modo teste
"%PYTHON_PATH%" Scripts\python\agendador_verificacao.py --testar

echo.
echo ========================================
echo   Teste concluído!
echo ========================================
echo.
pause
