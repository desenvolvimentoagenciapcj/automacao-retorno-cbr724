@echo off
REM Script silencioso para criar tarefas - executa via PowerShell elevado

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%~dp0criar_tarefas.ps1\"' -Verb RunAs -Wait"

echo.
echo Verificando se tarefas foram criadas...
timeout /t 3 /nobreak >nul

schtasks /Query /TN "AutomacaoRetorno\MonitorAutoInicio" >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Tarefa MonitorAutoInicio criada
) else (
    echo [ERRO] Tarefa MonitorAutoInicio NAO foi criada
)

schtasks /Query /TN "AutomacaoRetorno\VerificacaoAposReinicio" >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Tarefa VerificacaoAposReinicio criada
) else (
    echo [ERRO] Tarefa VerificacaoAposReinicio NAO foi criada
)

echo.
pause
