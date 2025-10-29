@echo off
REM Processa arquivos .ret que ja estavam na pasta antes do monitor iniciar
cd /d "%~dp0\..\.."
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "scripts\powershell\PROCESSAR_EXISTENTES.ps1"
