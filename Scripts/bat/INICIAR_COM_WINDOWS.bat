@echo off
chcp 65001 > nul

REM Verificar se está executando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permissões de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

color 0B

echo.
echo ═══════════════════════════════════════════════════════════════
echo  🚀 CONFIGURAR INICIALIZAÇÃO AUTOMÁTICA COM WINDOWS
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Este script configura o monitor para iniciar automaticamente
echo  quando o Windows inicia (após login do usuário).
echo.
echo  📋 O que será configurado:
echo     • Monitor de Retornos: inicia em segundo plano
echo     • Agendador de Verificação: verifica às 8h30
echo.
echo  ⚙️  Método: Agendador de Tarefas do Windows
echo     • Executa após login do usuário
echo     • Reinicia automaticamente se falhar
echo     • Logs em: logs\startup.log
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

echo.
echo ─────────────────────────────────────────────────────────────
echo  Removendo tarefas antigas (se existirem)...
echo ─────────────────────────────────────────────────────────────
schtasks /Delete /TN "AutomacaoRetorno\Monitor" /F 2>nul
schtasks /Delete /TN "AutomacaoRetorno\Agendador" /F 2>nul
echo.

echo ─────────────────────────────────────────────────────────────
echo  Criando tarefa: Monitor de Retornos
echo ─────────────────────────────────────────────────────────────
schtasks /Create /TN "AutomacaoRetorno\Monitor" ^
  /TR "\"%~dp0INICIAR_MONITOR_OCULTO.bat\"" ^
  /SC ONLOGON ^
  /DELAY 0001:00 ^
  /RL HIGHEST ^
  /F

if %errorlevel% equ 0 (
    echo ✅ Monitor configurado com sucesso!
) else (
    echo ❌ Erro ao configurar monitor
    pause
    exit /b 1
)
echo.

echo ─────────────────────────────────────────────────────────────
echo  Criando tarefa: Agendador de Verificação
echo ─────────────────────────────────────────────────────────────
schtasks /Create /TN "AutomacaoRetorno\Agendador" ^
  /TR "\"%~dp0INICIAR_AGENDADOR_OCULTO.bat\"" ^
  /SC ONLOGON ^
  /DELAY 0001:00 ^
  /RL HIGHEST ^
  /F

if %errorlevel% equ 0 (
    echo ✅ Agendador configurado com sucesso!
) else (
    echo ❌ Erro ao configurar agendador
    pause
    exit /b 1
)
echo.

echo ═══════════════════════════════════════════════════════════════
echo  ✅ CONFIGURAÇÃO CONCLUÍDA!
echo ═══════════════════════════════════════════════════════════════
echo.
echo  📋 Tarefas criadas:
echo     • AutomacaoRetorno\Monitor
echo     • AutomacaoRetorno\Agendador
echo.
echo  ⏰ Execução:
echo     • Ao fazer login no Windows (após 1 minuto)
echo     • Em segundo plano (invisível)
echo.
echo  🔍 Gerenciar tarefas:
echo     • Abra: Agendador de Tarefas do Windows
echo     • Procure: AutomacaoRetorno
echo.
echo  🧪 Testar agora:
echo     1. Execute: .\INICIAR.bat
echo     2. Ou reinicie o Windows
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
