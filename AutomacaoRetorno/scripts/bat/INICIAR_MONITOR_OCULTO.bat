@echo off
REM ============================================================================
REM Monitor Automático de Retornos Bancários - INICIAR EM SEGUNDO PLANO
REM MODO SILENCIOSO: Nenhuma janela visível
REM ============================================================================

cd /d "%~dp0\..\.."

REM PASSO 1: Parar todos os monitores antigos (evita processos órfãos) - SEM JANELA
powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File "scripts\powershell\_stop_all_monitors.ps1" >nul 2>&1

REM PASSO 2: Iniciar monitor usando PowerShell - SEM JANELA
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -NoProfile -File "scripts\powershell\_start_monitor_hidden.ps1" >nul 2>&1

REM Fim silencioso - nenhuma janela permanece aberta
exit /b 0
