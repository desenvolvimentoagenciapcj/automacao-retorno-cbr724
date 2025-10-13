# Script de Limpeza V4
# Remove arquivos desnecessarios
# Data: 13/10/2025

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "LIMPEZA V4 - ARQUIVOS DESNECESSARIOS" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Situacao atual
$totalAntes = (Get-ChildItem -File | Measure-Object).Count
Write-Host "Arquivos na pasta: $totalAntes" -ForegroundColor White
Write-Host "Recomendado: ~25-30 arquivos`n" -ForegroundColor Gray

# Criar pasta de backup
$backup = "Backup_Limpeza_V4_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Criando backup de seguranca..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Write-Host "Pasta criada: $backup`n" -ForegroundColor Green

Write-Host "REMOVENDO ARQUIVOS DESNECESSARIOS:`n" -ForegroundColor Yellow

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

# 1. PASTAS DE BACKUP ANTIGAS
Write-Host "1. Pastas de backup antigas:" -ForegroundColor Cyan
MoverParaBackup "Backup_Arquivos_Antigos_20251008_154735" "Backup_Arquivos_Antigos"
MoverParaBackup "Backup_Limpeza_V2_20251009_174222" "Backup_Limpeza_V2"
MoverParaBackup "Backup_Limpeza_V3_20251010_083334" "Backup_Limpeza_V3"
Write-Host ""

# 2. ARQUIVOS DUPLICADOS
Write-Host "2. Arquivos duplicados:" -ForegroundColor Cyan
MoverParaBackup "COPIAR_PARA_ONEDRIVE.bat" "COPIAR_PARA_ONEDRIVE.bat - duplicado"
MoverParaBackup "COPIAR_PARA_ONEDRIVE.ps1" "COPIAR_PARA_ONEDRIVE.ps1 - obsoleto"
MoverParaBackup "notificador_email.py" "notificador_email.py - nao usado"
Write-Host ""

# 3. LOGS ANTIGOS
Write-Host "3. Logs antigos:" -ForegroundColor Cyan
Get-ChildItem "monitor_retornos_OLD_*.log" -ErrorAction SilentlyContinue | ForEach-Object {
    MoverParaBackup $_.Name "Log antigo: $($_.Name)"
}
if (Test-Path "logs" -PathType Container) {
    $logsCount = (Get-ChildItem "logs" -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($logsCount -eq 0) {
        MoverParaBackup "logs" "Pasta logs vazia"
    }
}
Write-Host ""

# 4. DOCUMENTACAO REDUNDANTE
Write-Host "4. Documentacao redundante:" -ForegroundColor Cyan
MoverParaBackup "ANALISE_PROFUNDA_ARQUIVOS.md" "ANALISE_PROFUNDA_ARQUIVOS.md - analise antiga"
MoverParaBackup "CORRECAO_BUG_10102025.md" "CORRECAO_BUG_10102025.md - bug corrigido"
MoverParaBackup "RESULTADO_LIMPEZA_V3_FINAL.txt" "RESULTADO_LIMPEZA_V3_FINAL.txt - resultado antigo"
MoverParaBackup "SISTEMA_ANTI_ORFAOS.md" "SISTEMA_ANTI_ORFAOS.md - redundante"
MoverParaBackup "SISTEMA_NOTIFICACOES.md" "SISTEMA_NOTIFICACOES.md - redundante"
Write-Host ""

# 5. SCRIPTS OBSOLETOS
Write-Host "5. Scripts obsoletos:" -ForegroundColor Cyan
MoverParaBackup "IMPLANTAR.ps1" "IMPLANTAR.ps1 - nao usado"
MoverParaBackup "_start_monitor.bat" "_start_monitor.bat - obsoleto"
MoverParaBackup "_run_hidden.vbs" "_run_hidden.vbs - obsoleto"
MoverParaBackup "gerar_manual_pdf.py" "gerar_manual_pdf.py - tentativa falha"
Write-Host ""

# 6. DOCUMENTACAO PARA CONSOLIDAR
Write-Host "6. Documentacao para consolidar:" -ForegroundColor Cyan
if (Test-Path "CENTRALIZACAO_CONFIG.md") {
    Write-Host "   INFO: CENTRALIZACAO_CONFIG.md - Pode ser mesclado" -ForegroundColor Yellow
}
if (Test-Path "RESUMO_CENTRALIZACAO.md") {
    Write-Host "   INFO: RESUMO_CENTRALIZACAO.md - Pode ser mesclado" -ForegroundColor Yellow
}
Write-Host ""

# RESUMO
$totalDepois = (Get-ChildItem -File | Measure-Object).Count

Write-Host "========================================" -ForegroundColor Green
Write-Host "LIMPEZA CONCLUIDA!" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "RESULTADOS:`n" -ForegroundColor Cyan
Write-Host "   Arquivos antes:    $totalAntes" -ForegroundColor White
Write-Host "   Arquivos depois:   $totalDepois" -ForegroundColor Green
Write-Host "   Removidos:         $removidos" -ForegroundColor Yellow
$percentual = [math]::Round(($removidos / $totalAntes) * 100, 1)
Write-Host "   Reducao:           $percentual%`n" -ForegroundColor Green

Write-Host "BACKUP CRIADO:`n" -ForegroundColor Cyan
Write-Host "   Pasta: $backup" -ForegroundColor White
Write-Host "   Todos os arquivos removidos estao no backup" -ForegroundColor Gray
Write-Host "   Se tudo funcionar bem nos proximos 7 dias," -ForegroundColor Gray
Write-Host "   voce pode deletar essa pasta.`n" -ForegroundColor Gray

Write-Host "IMPORTANTE:`n" -ForegroundColor Yellow
Write-Host "   1. Teste o sistema completo agora" -ForegroundColor White
Write-Host "   2. Execute: INICIAR_MONITOR_OCULTO.bat" -ForegroundColor White
Write-Host "   3. Execute: PROCESSAR_EXISTENTES.bat" -ForegroundColor White
Write-Host "   4. Execute: STATUS_MONITOR.bat" -ForegroundColor White
Write-Host "   5. Verifique os logs`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Gray
Write-Host "Se algo nao funcionar, restaure do backup:" -ForegroundColor Yellow
Write-Host "Move-Item `"$backup\*`" -Destination . -Force" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Gray

# Listar arquivos restantes
Write-Host "ARQUIVOS RESTANTES (principais):`n" -ForegroundColor Cyan
Get-ChildItem -File | Where-Object { $_.Extension -in '.py', '.bat', '.ps1', '.ini', '.md' } | 
    Group-Object Extension | ForEach-Object {
        Write-Host "   $($_.Name): $($_.Count) arquivos" -ForegroundColor White
    }

Write-Host "`nLimpeza concluida com sucesso!" -ForegroundColor Green
Write-Host ""
