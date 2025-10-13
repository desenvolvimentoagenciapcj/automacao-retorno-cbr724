@echo off
chcp 65001 >nul

echo.
echo ========================================
echo   AGENDADOR DE VERIFICAÇÃO - PARAR
echo ========================================
echo.

REM Para todos os processos Python rodando agendador_verificacao.py
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2^>nul | findstr /i "agendador_verificacao.py" ^>nul
    if not errorlevel 1 (
        echo 🛑 Parando agendador... PID: %%a
        taskkill /PID %%a /F >nul 2>&1
        echo ✅ Agendador parado!
        echo.
        pause
        exit /b 0
    )
)

echo ℹ️  Agendador não está rodando.
echo.
pause
