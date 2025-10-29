@echo off
REM ============================================================================
REM SCRIPT DE LIMPEZA V5 - Remove arquivos desnecessarios
REM ============================================================================
REM Data: 29/10/2025
REM Objetivo: Deixar projeto enxuto, profissional e funcionando

cls
color 0A
echo.
echo ================================================================================
echo          LIMPEZA DO PROJETO - VERSAO 5
echo          Remove arquivos obsoletos e documentacao historica
echo ================================================================================
echo.

REM Ir para pasta do projeto
cd /d "%~dp0"

REM ============================================================================
REM ANALISE PRE-LIMPEZA
REM ============================================================================

echo Analisando arquivos atuais...
echo.

REM Contar arquivos antes
setlocal enabledelayedexpansion
set CONTADOR=0
for /r %%A in (*) do (
    set /a CONTADOR+=1
)

echo Arquivos atuais: !CONTADOR!
echo.

REM ============================================================================
REM ARQUIVOS A SEREM DELETADOS
REM ============================================================================

echo Deletando arquivos obsoletos...
echo.

REM Resumos e analises
if exist "RESUMO_FINAL.txt" (
    del /q "RESUMO_FINAL.txt"
    echo   OK Deletado: RESUMO_FINAL.txt
)

if exist "RESUMO_ADICAO_EMAILS.txt" (
    del /q "RESUMO_ADICAO_EMAILS.txt"
    echo   OK Deletado: RESUMO_ADICAO_EMAILS.txt
)

if exist "RESUMO_IMPLEMENTACAO.md" (
    del /q "RESUMO_IMPLEMENTACAO.md"
    echo   OK Deletado: RESUMO_IMPLEMENTACAO.md
)

if exist "RESUMO_MUDANCAS_VISUAL.md" (
    del /q "RESUMO_MUDANCAS_VISUAL.md"
    echo   OK Deletado: RESUMO_MUDANCAS_VISUAL.md
)

if exist "DETALHES_CODIGO_MODIFICADO.txt" (
    del /q "DETALHES_CODIGO_MODIFICADO.txt"
    echo   OK Deletado: DETALHES_CODIGO_MODIFICADO.txt
)

if exist "DIFF_MUDANCAS.txt" (
    del /q "DIFF_MUDANCAS.txt"
    echo   OK Deletado: DIFF_MUDANCAS.txt
)

REM Instrucoes de teste
if exist "INSTRUCOES_TESTE.bat" (
    del /q "INSTRUCOES_TESTE.bat"
    echo   OK Deletado: INSTRUCOES_TESTE.bat
)

if exist "LEIA-ME_PRIMEIRO.txt" (
    del /q "LEIA-ME_PRIMEIRO.txt"
    echo   OK Deletado: LEIA-ME_PRIMEIRO.txt
)

REM Documentacao de alteracoes
if exist "ADICAO_EMAILS_ALERTA.md" (
    del /q "ADICAO_EMAILS_ALERTA.md"
    echo   OK Deletado: ADICAO_EMAILS_ALERTA.md
)

if exist "ALTERACOES_NOTIFICACAO_ARQUIVOS.md" (
    del /q "ALTERACOES_NOTIFICACAO_ARQUIVOS.md"
    echo   OK Deletado: ALTERACOES_NOTIFICACAO_ARQUIVOS.md
)

if exist "CORRECAO_AUTOSTART_20102025.md" (
    del /q "CORRECAO_AUTOSTART_20102025.md"
    echo   OK Deletado: CORRECAO_AUTOSTART_20102025.md
)

if exist "REORGANIZACAO_COMPLETA.md" (
    del /q "REORGANIZACAO_COMPLETA.md"
    echo   OK Deletado: REORGANIZACAO_COMPLETA.md
)

if exist "README_NOTIFICACAO_ARQUIVOS.md" (
    del /q "README_NOTIFICACAO_ARQUIVOS.md"
    echo   OK Deletado: README_NOTIFICACAO_ARQUIVOS.md
)

if exist "GUIA_BACKUP_ONEDRIVE.md" (
    del /q "GUIA_BACKUP_ONEDRIVE.md"
    echo   OK Deletado: GUIA_BACKUP_ONEDRIVE.md
)

REM Scripts obsoletos
if exist "teste_novo_agendador.py" (
    del /q "teste_novo_agendador.py"
    echo   OK Deletado: teste_novo_agendador.py
)

REM Scripts BAT obsoletos
if exist "AGENDADOR.bat" (
    del /q "AGENDADOR.bat"
    echo   OK Deletado: AGENDADOR.bat
)

if exist "CONFIGURAR_INICIO_AUTOMATICO.bat" (
    del /q "CONFIGURAR_INICIO_AUTOMATICO.bat"
    echo   OK Deletado: CONFIGURAR_INICIO_AUTOMATICO.bat
)

if exist "CONFIGURAR_INICIO_RAPIDO.bat" (
    del /q "CONFIGURAR_INICIO_RAPIDO.bat"
    echo   OK Deletado: CONFIGURAR_INICIO_RAPIDO.bat
)

if exist "RECRIAR_TASK_MONITOR_SYSTEM.bat" (
    del /q "RECRIAR_TASK_MONITOR_SYSTEM.bat"
    echo   OK Deletado: RECRIAR_TASK_MONITOR_SYSTEM.bat
)

if exist "REMOVER_INICIO_AUTOMATICO.bat" (
    del /q "REMOVER_INICIO_AUTOMATICO.bat"
    echo   OK Deletado: REMOVER_INICIO_AUTOMATICO.bat
)

if exist "TESTAR_EMAIL.bat" (
    del /q "TESTAR_EMAIL.bat"
    echo   OK Deletado: TESTAR_EMAIL.bat
)

if exist "TESTAR_RECUPERACAO.bat" (
    del /q "TESTAR_RECUPERACAO.bat"
    echo   OK Deletado: TESTAR_RECUPERACAO.bat
)

if exist "TESTAR_VERIFICACAO_ARQUIVOS.bat" (
    del /q "TESTAR_VERIFICACAO_ARQUIVOS.bat"
    echo   OK Deletado: TESTAR_VERIFICACAO_ARQUIVOS.bat
)

REM Scripts PowerShell obsoletos
if exist "configurar_registro_startup.ps1" (
    del /q "configurar_registro_startup.ps1"
    echo   OK Deletado: configurar_registro_startup.ps1
)

if exist "criar_tarefas.ps1" (
    del /q "criar_tarefas.ps1"
    echo   OK Deletado: criar_tarefas.ps1
)

if exist "diagnostico_autostart.ps1" (
    del /q "diagnostico_autostart.ps1"
    echo   OK Deletado: diagnostico_autostart.ps1
)

if exist "reconfigurar_agendador.ps1" (
    del /q "reconfigurar_agendador.ps1"
    echo   OK Deletado: reconfigurar_agendador.ps1
)

if exist "reconfigurar_monitor_boot.ps1" (
    del /q "reconfigurar_monitor_boot.ps1"
    echo   OK Deletado: reconfigurar_monitor_boot.ps1
)

if exist "reconfigurar_monitor_boot_sys_v2.ps1" (
    del /q "reconfigurar_monitor_boot_sys_v2.ps1"
    echo   OK Deletado: reconfigurar_monitor_boot_sys_v2.ps1
)

if exist "reconfigurar_monitor_boot_user.ps1" (
    del /q "reconfigurar_monitor_boot_user.ps1"
    echo   OK Deletado: reconfigurar_monitor_boot_user.ps1
)

REM Backups antigos
if exist "Backup_Limpeza_Final_20251013_093912" (
    rmdir /s /q "Backup_Limpeza_Final_20251013_093912"
    echo   OK Deletado: Backup_Limpeza_Final_20251013_093912
)

if exist "Backup_Limpeza_V4_20251013_092753" (
    rmdir /s /q "Backup_Limpeza_V4_20251013_092753"
    echo   OK Deletado: Backup_Limpeza_V4_20251013_092753
)

REM Scripts auxiliares
if exist "BACKUP_ONEDRIVE.bat" (
    del /q "BACKUP_ONEDRIVE.bat"
    echo   OK Deletado: BACKUP_ONEDRIVE.bat
)

if exist "GIT_BACKUP_COMPLETO.bat" (
    del /q "GIT_BACKUP_COMPLETO.bat"
    echo   OK Deletado: GIT_BACKUP_COMPLETO.bat
)

echo.
echo ================================================================================
echo Limpeza concluida!
echo ================================================================================
echo.
echo Arquivos restantes:
dir /b | find /v /c "::"

echo.
echo Agora faca:
echo   git add .
echo   git commit -m "Limpeza V5: Removidos arquivos obsoletos"
echo   git push
echo.

pause
