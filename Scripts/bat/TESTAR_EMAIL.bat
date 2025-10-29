@echo off
chcp 65001 >nul
cd /d "%~dp0\..\.."

echo.
echo ========================================
echo    TESTE DE NOTIFICAÇÃO POR E-MAIL
echo ========================================
echo.

REM Lê o caminho do Python do config.ini
for /f "tokens=2 delims==" %%a in ('findstr /i "^executavel" "config\config.ini"') do set PYTHON_PATH=%%a
set PYTHON_PATH=%PYTHON_PATH: =%

echo 📧 Testando configuração de e-mail...
echo.

"%PYTHON_PATH%" "scripts\python\notificador_email.py"

echo.
pause
