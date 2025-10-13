# Cria atalhos na raiz para os scripts BAT principais
# Data: 13/10/2025

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CRIANDO ATALHOS DE ACESSO RAPIDO" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Criar atalhos BAT na raiz que chamam os scripts nas pastas
$atalhos = @{
    "INICIAR.bat" = "scripts\bat\INICIAR_MONITOR_OCULTO.bat"
    "PARAR.bat" = "scripts\bat\PARAR_MONITOR.bat"
    "STATUS.bat" = "scripts\bat\STATUS_MONITOR.bat"
    "PROCESSAR.bat" = "scripts\bat\PROCESSAR_EXISTENTES.bat"
}

foreach ($atalho in $atalhos.GetEnumerator()) {
    $conteudo = @"
@echo off
cd /d "%~dp0"
call "$($atalho.Value)"
"@
    
    $conteudo | Out-File -FilePath $atalho.Key -Encoding ASCII
    Write-Host "   OK: $($atalho.Key)" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "ATALHOS CRIADOS NA RAIZ!" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Agora voce pode usar diretamente:`n" -ForegroundColor Cyan
Write-Host "   INICIAR.bat  - Inicia o monitor" -ForegroundColor White
Write-Host "   PARAR.bat    - Para o monitor" -ForegroundColor White
Write-Host "   STATUS.bat   - Ver status" -ForegroundColor White
Write-Host "   PROCESSAR.bat - Processar existentes`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ESTRUTURA FINAL ORGANIZADA:" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "AutomacaoRetorno/" -ForegroundColor White
Write-Host "  INICIAR.bat, PARAR.bat, STATUS.bat  (atalhos rapidos)" -ForegroundColor Yellow
Write-Host "  scripts/" -ForegroundColor Cyan
Write-Host "    python/     - Scripts Python" -ForegroundColor White
Write-Host "    powershell/ - Scripts PowerShell" -ForegroundColor White
Write-Host "    bat/        - Scripts BAT" -ForegroundColor White
Write-Host "  config/" -ForegroundColor Cyan
Write-Host "    config.ini  - Configuracao central" -ForegroundColor White
Write-Host "  logs/" -ForegroundColor Cyan
Write-Host "    monitor_retornos.log - Log principal" -ForegroundColor White
Write-Host "  docs/" -ForegroundColor Cyan
Write-Host "    DOCUMENTACAO_SISTEMA.md - Manual completo`n" -ForegroundColor White

Write-Host "Sistema reorganizado e pronto!" -ForegroundColor Green
Write-Host ""
