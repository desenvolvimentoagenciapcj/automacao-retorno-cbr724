@echo off
chcp 65001 >nul
cd /d "%~dp0\..\.."

echo.
echo ========================================
echo   AGENDADOR DE VERIFICAÇÃO - INICIAR
echo ========================================
echo.

REM Lê o caminho do Python do config.ini
for /f "tokens=2 delims==" %%a in ('findstr /i "^executavel" "config\config.ini"') do set PYTHON_PATH=%%a
set PYTHON_PATH=%PYTHON_PATH: =%

REM Verifica se já está rodando
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2^>nul | findstr /i "agendador_verificacao.py" ^>nul
    if not errorlevel 1 (
        echo ⚠️  Agendador já está rodando!
        echo.
        pause
        exit /b 0
    )
)

echo 📅 Iniciando agendador de verificação...
echo.
echo ⏰ Horário: Segunda a Sexta às 8h
echo 🔍 Função: Verifica se o monitor está ativo
echo 🔄 Ação: Reinicia automaticamente se necessário
echo.

REM Inicia o agendador em modo oculto
start "" /min "%PYTHON_PATH%" "scripts\python\agendador_verificacao.py"

timeout /t 3 >nul

echo ✅ Agendador iniciado!
echo.
pause
