# Script de Reorganizacao - Estrutura Profissional
# Organiza arquivos em pastas por categoria
# Data: 13/10/2025

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "REORGANIZACAO - ESTRUTURA PROFISSIONAL" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Criando estrutura de pastas...`n" -ForegroundColor Yellow

# Criar estrutura
$pastas = @(
    "scripts\python",
    "scripts\powershell", 
    "scripts\bat",
    "config",
    "logs",
    "docs"
)

foreach ($pasta in $pastas) {
    New-Item -ItemType Directory -Force -Path $pasta | Out-Null
    Write-Host "   OK: $pasta" -ForegroundColor Green
}

Write-Host "`nMovendo arquivos para pastas apropriadas...`n" -ForegroundColor Yellow

$movidos = 0

# Funcao para mover arquivo
function MoverArquivo {
    param([string]$Arquivo, [string]$Destino, [string]$Categoria)
    
    if (Test-Path $Arquivo) {
        try {
            Move-Item $Arquivo -Destination $Destino -Force -ErrorAction Stop
            Write-Host "   [$Categoria] $Arquivo" -ForegroundColor White
            $script:movidos++
        } catch {
            Write-Host "   ERRO: $Arquivo" -ForegroundColor Red
        }
    }
}

# PYTHON
Write-Host "PYTHON SCRIPTS:" -ForegroundColor Cyan
MoverArquivo "config_manager.py" "scripts\python\" "PY"
MoverArquivo "monitor_retornos.py" "scripts\python\" "PY"
MoverArquivo "processador_cbr724.py" "scripts\python\" "PY"
MoverArquivo "integrador_access.py" "scripts\python\" "PY"
MoverArquivo "gerar_pdfs_simples.py" "scripts\python\" "PY"
MoverArquivo "notificador_windows.py" "scripts\python\" "PY"
MoverArquivo "watchdog_monitor.py" "scripts\python\" "PY"

# POWERSHELL
Write-Host "`nPOWERSHELL SCRIPTS:" -ForegroundColor Cyan
MoverArquivo "_read_config.ps1" "scripts\powershell\" "PS1"
MoverArquivo "_start_monitor_hidden.ps1" "scripts\powershell\" "PS1"
MoverArquivo "_stop_all_monitors.ps1" "scripts\powershell\" "PS1"
MoverArquivo "_check_monitor.ps1" "scripts\powershell\" "PS1"
MoverArquivo "BACKUP_ONEDRIVE.ps1" "scripts\powershell\" "PS1"
MoverArquivo "PROCESSAR_EXISTENTES.ps1" "scripts\powershell\" "PS1"

# BAT
Write-Host "`nBAT SCRIPTS:" -ForegroundColor Cyan
MoverArquivo "INICIAR_MONITOR_OCULTO.bat" "scripts\bat\" "BAT"
MoverArquivo "PARAR_MONITOR.bat" "scripts\bat\" "BAT"
MoverArquivo "STATUS_MONITOR.bat" "scripts\bat\" "BAT"
MoverArquivo "PROCESSAR_EXISTENTES.bat" "scripts\bat\" "BAT"
MoverArquivo "INICIAR_WATCHDOG.bat" "scripts\bat\" "BAT"
MoverArquivo "PARAR_WATCHDOG.bat" "scripts\bat\" "BAT"

# CONFIGURACAO
Write-Host "`nCONFIGURACOES:" -ForegroundColor Cyan
MoverArquivo "config.ini" "config\" "CFG"
MoverArquivo "requirements.txt" "config\" "CFG"
MoverArquivo ".gitignore" "config\" "CFG"

# LOGS
Write-Host "`nLOGS:" -ForegroundColor Cyan
MoverArquivo "monitor_retornos.log" "logs\" "LOG"
MoverArquivo "watchdog.log" "logs\" "LOG"

# DOCUMENTACAO
Write-Host "`nDOCUMENTACAO:" -ForegroundColor Cyan
MoverArquivo "DOCUMENTACAO_SISTEMA.md" "docs\" "DOC"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "REORGANIZACAO CONCLUIDA!" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Total de arquivos movidos: $movidos`n" -ForegroundColor Cyan

Write-Host "ESTRUTURA FINAL:`n" -ForegroundColor Yellow
Write-Host "AutomacaoRetorno/" -ForegroundColor White
Write-Host "  scripts/" -ForegroundColor Cyan
Write-Host "    python/     - 7 arquivos .py" -ForegroundColor White
Write-Host "    powershell/ - 6 arquivos .ps1" -ForegroundColor White
Write-Host "    bat/        - 6 arquivos .bat" -ForegroundColor White
Write-Host "  config/       - 3 arquivos" -ForegroundColor Cyan
Write-Host "  logs/         - 2 arquivos" -ForegroundColor Cyan
Write-Host "  docs/         - 1 arquivo`n" -ForegroundColor Cyan

Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "Os scripts BAT agora precisam dos caminhos atualizados!" -ForegroundColor White
Write-Host "Aguarde o proximo script...`n" -ForegroundColor Green

Write-Host "Sistema reorganizado com sucesso!" -ForegroundColor Green
Write-Host ""
