@echo off
chcp 65001 > nul
color 0B

echo.
echo ═══════════════════════════════════════════════════════════════
echo  🚀 CONFIGURAR INÍCIO AUTOMÁTICO COM WINDOWS
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Este script configura o sistema para iniciar automaticamente
echo  quando o Windows é ligado ou reiniciado.
echo.
echo  ⚠️  Requer privilégios de Administrador!
echo.
echo ═══════════════════════════════════════════════════════════════
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  VERIFICANDO PRIVILÉGIOS...
echo ═══════════════════════════════════════════════════════════════

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ❌ ERRO: Este script precisa ser executado como Administrador!
    echo.
    echo 📝 Como executar como Administrador:
    echo    1. Clique com botão direito neste arquivo
    echo    2. Selecione "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo ✅ Privilégios OK
echo.

echo ═══════════════════════════════════════════════════════════════
echo  REMOVENDO TAREFA ANTIGA (se existir)...
echo ═══════════════════════════════════════════════════════════════

schtasks /Delete /TN "AutomacaoRetorno\Monitor" /F >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Tarefa antiga removida
) else (
    echo ℹ️  Nenhuma tarefa antiga encontrada
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  CRIANDO TAREFA AGENDADA...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Criar XML da tarefa
set "XML_FILE=%TEMP%\monitor_task.xml"

(
echo ^<?xml version="1.0" encoding="UTF-16"?^>
echo ^<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^>
echo   ^<RegistrationInfo^>
echo     ^<Description^>Inicia automaticamente o Monitor de Retornos CBR724 ao iniciar o Windows^</Description^>
echo     ^<Author^>Sistema de Automação^</Author^>
echo   ^</RegistrationInfo^>
echo   ^<Triggers^>
echo     ^<BootTrigger^>
echo       ^<Delay^>PT2M^</Delay^>
echo       ^<Enabled^>true^</Enabled^>
echo     ^</BootTrigger^>
echo   ^</Triggers^>
echo   ^<Principals^>
echo     ^<Principal id="Author"^>
echo       ^<UserId^>%USERNAME%^</UserId^>
echo       ^<LogonType^>InteractiveToken^</LogonType^>
echo       ^<RunLevel^>HighestAvailable^</RunLevel^>
echo     ^</Principal^>
echo   ^</Principals^>
echo   ^<Settings^>
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^>
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^>
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^>
echo     ^<AllowHardTerminate^>false^</AllowHardTerminate^>
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^>
echo     ^<RunOnlyIfNetworkAvailable^>true^</RunOnlyIfNetworkAvailable^>
echo     ^<IdleSettings^>
echo       ^<StopOnIdleEnd^>false^</StopOnIdleEnd^>
echo       ^<RestartOnIdle^>false^</RestartOnIdle^>
echo     ^</IdleSettings^>
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^>
echo     ^<Enabled^>true^</Enabled^>
echo     ^<Hidden^>false^</Hidden^>
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^>
echo     ^<DisallowStartOnRemoteAppSession^>false^</DisallowStartOnRemoteAppSession^>
echo     ^<UseUnifiedSchedulingEngine^>true^</UseUnifiedSchedulingEngine^>
echo     ^<WakeToRun^>false^</WakeToRun^>
echo     ^<ExecutionTimeLimit^>PT0S^</ExecutionTimeLimit^>
echo     ^<Priority^>7^</Priority^>
echo   ^</Settings^>
echo   ^<Actions Context="Author"^>
echo     ^<Exec^>
echo       ^<Command^>"%~dp0scripts\bat\INICIAR_MONITOR_OCULTO.bat"^</Command^>
echo       ^<WorkingDirectory^>%~dp0^</WorkingDirectory^>
echo     ^</Exec^>
echo   ^</Actions^>
echo ^</Task^>
) > "%XML_FILE%"

REM Importar tarefa
schtasks /Create /XML "%XML_FILE%" /TN "AutomacaoRetorno\MonitorAutoInicio" /F

if %errorLevel% equ 0 (
    echo ✅ Tarefa criada com sucesso!
    echo.
    echo 📋 Detalhes da Tarefa:
    echo    Nome: AutomacaoRetorno\MonitorAutoInicio
    echo    Gatilho: Ao iniciar o Windows
    echo    Atraso: 2 minutos após boot
    echo    Executar: %~dp0scripts\bat\INICIAR_MONITOR_OCULTO.bat
    echo    Requer Rede: Sim
) else (
    echo ❌ Erro ao criar tarefa!
    del "%XML_FILE%" >nul 2>&1
    pause
    exit /b 1
)

REM Limpar arquivo XML
del "%XML_FILE%" >nul 2>&1

echo.
echo ═══════════════════════════════════════════════════════════════
echo  CONFIGURANDO VERIFICAÇÃO DE REINICIALIZAÇÃO...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar se já existe tarefa de verificação
schtasks /Query /TN "AutomacaoRetorno\VerificacaoAposReinicio" >nul 2>&1
if %errorLevel% equ 0 (
    echo ℹ️  Tarefa de verificação já existe
) else (
    REM Criar tarefa que roda 10 minutos após boot para verificar se monitor iniciou
    set "XML_FILE2=%TEMP%\verificacao_task.xml"
    
    (
    echo ^<?xml version="1.0" encoding="UTF-16"?^>
    echo ^<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^>
    echo   ^<RegistrationInfo^>
    echo     ^<Description^>Verifica se o monitor iniciou corretamente após reinicialização^</Description^>
    echo   ^</RegistrationInfo^>
    echo   ^<Triggers^>
    echo     ^<BootTrigger^>
    echo       ^<Delay^>PT10M^</Delay^>
    echo       ^<Enabled^>true^</Enabled^>
    echo     ^</BootTrigger^>
    echo   ^</Triggers^>
    echo   ^<Principals^>
    echo     ^<Principal id="Author"^>
    echo       ^<UserId^>%USERNAME%^</UserId^>
    echo       ^<LogonType^>InteractiveToken^</LogonType^>
    echo       ^<RunLevel^>HighestAvailable^</RunLevel^>
    echo     ^</Principal^>
    echo   ^</Principals^>
    echo   ^<Settings^>
    echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^>
    echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^>
    echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^>
    echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^>
    echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^>
    echo     ^<RunOnlyIfNetworkAvailable^>true^</RunOnlyIfNetworkAvailable^>
    echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^>
    echo     ^<Enabled^>true^</Enabled^>
    echo     ^<ExecutionTimeLimit^>PT5M^</ExecutionTimeLimit^>
    echo   ^</Settings^>
    echo   ^<Actions Context="Author"^>
    echo     ^<Exec^>
    echo       ^<Command^>"%~dp0scripts\bat\VERIFICAR_APOS_BOOT.bat"^</Command^>
    echo       ^<WorkingDirectory^>%~dp0^</WorkingDirectory^>
    echo     ^</Exec^>
    echo   ^</Actions^>
    echo ^</Task^>
    ) > "%XML_FILE2%"
    
    schtasks /Create /XML "%XML_FILE2%" /TN "AutomacaoRetorno\VerificacaoAposReinicio" /F >nul 2>&1
    if %errorLevel% equ 0 (
        echo ✅ Verificação após boot configurada
    )
    del "%XML_FILE2%" >nul 2>&1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  TESTANDO CONFIGURAÇÃO...
echo ═══════════════════════════════════════════════════════════════
echo.

schtasks /Query /TN "AutomacaoRetorno\MonitorAutoInicio" /V /FO LIST | findstr /C:"Estado da tarefa" /C:"Próxima execução"

echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✅ CONFIGURAÇÃO CONCLUÍDA!
echo ═══════════════════════════════════════════════════════════════
echo.
echo  O sistema agora irá:
echo  1. ✅ Iniciar automaticamente ao ligar/reiniciar Windows
echo  2. ✅ Aguardar 2 minutos para rede estabilizar
echo  3. ✅ Verificar após 10 minutos se iniciou corretamente
echo  4. ✅ Enviar notificação se houver problemas
echo.
echo  📝 Para testar agora:
echo     schtasks /Run /TN "AutomacaoRetorno\MonitorAutoInicio"
echo.
echo  📝 Para desabilitar:
echo     schtasks /Change /TN "AutomacaoRetorno\MonitorAutoInicio" /DISABLE
echo.
echo  📝 Para remover:
echo     schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F
echo.
echo ═══════════════════════════════════════════════════════════════
pause
