@echo off
chcp 65001 >nul
cd /d "%~dp0\..\.."

REM Lê o caminho do Python do config.ini
for /f "tokens=2 delims==" %%a in ('findstr /i "^executavel" "config\config.ini"') do set PYTHON_PATH=%%a
set PYTHON_PATH=%PYTHON_PATH: =%

REM Aguarda 1 minuto para garantir que sistema operacional iniciou completamente
timeout /t 60 /nobreak >nul

REM Verifica se já está rodando
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2^>nul | findstr /i "agendador_verificacao.py" ^>nul
    if not errorlevel 1 (
        exit /b 0
    )
)

REM Inicia o agendador em modo totalmente oculto
start "" /min "%PYTHON_PATH%" "scripts\python\agendador_verificacao.py" >nul 2>&1

exit /b 0
