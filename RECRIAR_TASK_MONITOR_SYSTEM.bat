@echo off
REM ============================================================================
REM Remover e recriar a task MonitorAutoInicio com SYSTEM user
REM ============================================================================
REM Este script deve ser executado como ADMINISTRADOR

echo.
echo ================================================================================
echo     RECONFIGURANDO TASK WINDOWS - MonitorAutoInicio (SYSTEM USER)
echo ================================================================================
echo.

REM Verificar se está rodando como admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Este script requer permissoes de ADMINISTRADOR!
    echo.
    echo Para executar como admin:
    echo   1. Abra o PowerShell como Administrador
    echo   2. Execute: cmd /c "%~0"
    echo.
    pause
    exit /b 1
)

echo ✅ Executando com permissoes de ADMINISTRADOR
echo.

REM Parar a task atual
echo [1/3] Parando task atual...
schtasks /End /TN "AutomacaoRetorno\MonitorAutoInicio" /F >nul 2>&1

REM Deletar task atual
echo [2/3] Deletando task...
schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F >nul 2>&1

REM Aguardar um pouco
timeout /t 2 /nobreak >nul

REM Recriar a task com SYSTEM user
echo [3/3] Recriando task com SYSTEM user...

schtasks /Create ^
    /TN "AutomacaoRetorno\MonitorAutoInicio" ^
    /TR "D:\Teste_Cobrança_Acess\AutomacaoRetorno\scripts\bat\INICIAR_MONITOR_OCULTO.bat" ^
    /SC ONSTART ^
    /DELAY 0000:02:00 ^
    /RU SYSTEM ^
    /RL HIGHEST ^
    /F

echo.
if %errorlevel% equ 0 (
    echo ================================================================================
    echo ✅ Task recriada com SUCESSO!
    echo ================================================================================
    echo.
    echo 📋 Configuração:
    echo    - Nome: AutomacaoRetorno\MonitorAutoInicio
    echo    - Trigger: ONSTART (Boot)
    echo    - Delay: 2 minutos
    echo    - User: SYSTEM (mais robusto)
    echo    - Nivel: HIGHEST (admin)
    echo.
) else (
    echo ================================================================================
    echo ❌ ERRO ao recriar a task!
    echo ================================================================================
    echo.
)

echo.
pause

