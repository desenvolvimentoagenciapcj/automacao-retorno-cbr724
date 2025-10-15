@echo off
chcp 65001 > nul

REM Verificar se está executando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permissões de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  🗑️  REMOVER INICIALIZAÇÃO AUTOMÁTICA
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Remove as tarefas agendadas do Windows.
echo  O sistema NÃO iniciará mais automaticamente.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

echo.
echo ─────────────────────────────────────────────────────────────
echo  Removendo tarefas...
echo ─────────────────────────────────────────────────────────────
schtasks /Delete /TN "AutomacaoRetorno\Monitor" /F
schtasks /Delete /TN "AutomacaoRetorno\Agendador" /F
echo.

echo ═══════════════════════════════════════════════════════════════
echo  ✅ Tarefas removidas!
echo ═══════════════════════════════════════════════════════════════
echo.
echo  O sistema não iniciará mais automaticamente com o Windows.
echo  Para iniciar manualmente, execute: .\INICIAR.bat
echo.
pause
