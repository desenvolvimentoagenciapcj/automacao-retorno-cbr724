@echo off
chcp 65001 >nul
cd /d "%~dp0\..\.."

REM Script silencioso para iniciar agendador em modo oculto (usado pela tarefa agendada)

REM Lê o caminho do Python do config.ini
for /f "tokens=2 delims==" %%a in ('findstr /i "^executavel" "config\config.ini"') do set PYTHON_PATH=%%a
set PYTHON_PATH=%PYTHON_PATH: =%

REM Verifica se já está rodando
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul') do (
    wmic process where "ProcessId=%%a" get CommandLine 2^>nul | findstr /i "agendador_verificacao.py" ^>nul
    if not errorlevel 1 (
        REM Agendador já está rodando - sair silenciosamente
        exit /b 0
    )
)

REM Iniciar agendador em modo oculto (sem janela visível)
start "" /min "%PYTHON_PATH%" "scripts\python\agendador_verificacao.py"

exit /b 0
