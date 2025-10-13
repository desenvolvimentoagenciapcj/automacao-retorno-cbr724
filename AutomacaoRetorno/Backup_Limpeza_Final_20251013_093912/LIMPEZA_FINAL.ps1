# Script de Limpeza Final - Consolidacao Completa
# Remove temporarios + Consolida documentacao
# Data: 13/10/2025

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "LIMPEZA FINAL - CONSOLIDACAO COMPLETA" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Situacao atual
$totalAntes = (Get-ChildItem -File | Measure-Object).Count
Write-Host "Arquivos atuais: $totalAntes" -ForegroundColor White
Write-Host "Meta final: 24 arquivos essenciais`n" -ForegroundColor Green

# Criar pasta de backup
$backup = "Backup_Limpeza_Final_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Criando backup de seguranca..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Write-Host "Pasta criada: $backup`n" -ForegroundColor Green

$removidos = 0

# Funcao para mover item
function MoverParaBackup {
    param([string]$Item, [string]$Descricao)
    
    if (Test-Path $Item) {
        try {
            Move-Item $Item -Destination $backup -Force -ErrorAction Stop
            Write-Host "   OK: $Descricao" -ForegroundColor Green
            $script:removidos++
        } catch {
            Write-Host "   ERRO: $Descricao" -ForegroundColor Yellow
        }
    }
}

Write-Host "ETAPA 1: Removendo arquivos temporarios`n" -ForegroundColor Yellow

# Arquivos temporarios de teste e limpeza
MoverParaBackup "teste_sintaxe.ps1" "Script de teste temporario"
MoverParaBackup "LIMPEZA_V4.ps1" "Script de limpeza ja executado"
MoverParaBackup "ANALISE_LIMPEZA_V4.md" "Analise ja concluida"

Write-Host "`nETAPA 2: Consolidando documentacao`n" -ForegroundColor Yellow

# Mover documentos que foram consolidados em DOCUMENTACAO_SISTEMA.md
MoverParaBackup "MANUAL_IMPLANTACAO_COMPLETO.md" "Consolidado"
MoverParaBackup "SISTEMA_EM_PRODUCAO.md" "Consolidado"
MoverParaBackup "SISTEMA_WATCHDOG.md" "Consolidado"
MoverParaBackup "GUIA_CONFIG.md" "Consolidado"
MoverParaBackup "NOTIFICACOES_WINDOWS.md" "Consolidado"
MoverParaBackup "CHANGELOG.md" "Consolidado"
MoverParaBackup "COMPORTAMENTO_MONITOR.md" "Consolidado"
MoverParaBackup "CENTRALIZACAO_CONFIG.md" "Consolidado"
MoverParaBackup "RESUMO_CENTRALIZACAO.md" "Consolidado"
MoverParaBackup "ANALISE_FINAL_POS_LIMPEZA.md" "Consolidado"

Write-Host ""

# RESUMO
$totalDepois = (Get-ChildItem -File | Measure-Object).Count

Write-Host "========================================" -ForegroundColor Green
Write-Host "CONSOLIDACAO CONCLUIDA!" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "RESULTADOS:`n" -ForegroundColor Cyan
Write-Host "   Arquivos antes:    $totalAntes" -ForegroundColor White
Write-Host "   Arquivos depois:   $totalDepois" -ForegroundColor Green
Write-Host "   Removidos:         $removidos" -ForegroundColor Yellow
$percentual = [math]::Round(($removidos / $totalAntes) * 100, 1)
Write-Host "   Reducao:           $percentual%`n" -ForegroundColor Green

Write-Host "DOCUMENTACAO CONSOLIDADA:`n" -ForegroundColor Cyan
Write-Host "   10 arquivos MD antigos -> 1 arquivo unico" -ForegroundColor White
Write-Host "   Arquivo: DOCUMENTACAO_SISTEMA.md" -ForegroundColor Green
Write-Host "   Conteudo: Manual completo do sistema`n" -ForegroundColor Gray

Write-Host "BACKUP CRIADO:`n" -ForegroundColor Cyan
Write-Host "   Pasta: $backup" -ForegroundColor White
Write-Host "   Todos os arquivos removidos estao no backup" -ForegroundColor Gray
Write-Host "   Pode ser deletado apos 7 dias de testes`n" -ForegroundColor Gray

Write-Host "ARQUIVOS RESTANTES (por tipo):`n" -ForegroundColor Cyan
Get-ChildItem -File | Where-Object { $_.Extension -in '.py', '.bat', '.ps1', '.ini', '.md', '.txt' } | 
    Group-Object Extension | ForEach-Object {
        Write-Host "   $($_.Name): $($_.Count) arquivos" -ForegroundColor White
    }

Write-Host "`nARQUIVOS ESSENCIAIS MANTIDOS:`n" -ForegroundColor Green
Write-Host "   [PYTHON]" -ForegroundColor Cyan
Write-Host "   - config_manager.py" -ForegroundColor White
Write-Host "   - monitor_retornos.py" -ForegroundColor White
Write-Host "   - processador_cbr724.py" -ForegroundColor White
Write-Host "   - integrador_access.py" -ForegroundColor White
Write-Host "   - gerar_pdfs_simples.py" -ForegroundColor White
Write-Host "   - notificador_windows.py" -ForegroundColor White
Write-Host "   - watchdog_monitor.py`n" -ForegroundColor White

Write-Host "   [POWERSHELL]" -ForegroundColor Cyan
Write-Host "   - _read_config.ps1" -ForegroundColor White
Write-Host "   - _start_monitor_hidden.ps1" -ForegroundColor White
Write-Host "   - _stop_all_monitors.ps1" -ForegroundColor White
Write-Host "   - _check_monitor.ps1" -ForegroundColor White
Write-Host "   - BACKUP_ONEDRIVE.ps1" -ForegroundColor White
Write-Host "   - PROCESSAR_EXISTENTES.ps1`n" -ForegroundColor White

Write-Host "   [INTERFACE BAT]" -ForegroundColor Cyan
Write-Host "   - INICIAR_MONITOR_OCULTO.bat" -ForegroundColor White
Write-Host "   - PARAR_MONITOR.bat" -ForegroundColor White
Write-Host "   - STATUS_MONITOR.bat" -ForegroundColor White
Write-Host "   - PROCESSAR_EXISTENTES.bat" -ForegroundColor White
Write-Host "   - INICIAR_WATCHDOG.bat" -ForegroundColor White
Write-Host "   - PARAR_WATCHDOG.bat`n" -ForegroundColor White

Write-Host "   [CONFIGURACAO]" -ForegroundColor Cyan
Write-Host "   - config.ini" -ForegroundColor White
Write-Host "   - requirements.txt" -ForegroundColor White
Write-Host "   - .gitignore`n" -ForegroundColor White

Write-Host "   [DOCUMENTACAO]" -ForegroundColor Cyan
Write-Host "   - DOCUMENTACAO_SISTEMA.md (NOVO - Manual completo)`n" -ForegroundColor Green

Write-Host "   [LOGS]" -ForegroundColor Cyan
Write-Host "   - monitor_retornos.log" -ForegroundColor White
Write-Host "   - watchdog.log`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Gray
Write-Host "Se algo nao funcionar, restaure:" -ForegroundColor Yellow
Write-Host "Move-Item `"$backup\*`" -Destination . -Force" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Gray

Write-Host "Sistema otimizado e pronto para producao!" -ForegroundColor Green
Write-Host ""
