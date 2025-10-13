# ============================================================================
# Processa arquivos .ret que já estavam na pasta antes do monitor iniciar
# ============================================================================

# Ler configurações do config.ini
function Get-ConfigValue {
    param(
        [string]$Secao,
        [string]$Chave
    )
    
    $configPath = Join-Path $PSScriptRoot "config.ini"
    $conteudo = Get-Content $configPath -Encoding UTF8
    
    $dentroSecao = $false
    foreach ($linha in $conteudo) {
        $linha = $linha.Trim()
        if ($linha -match "^#" -or $linha -eq "") { continue }
        
        if ($linha -match "^\[(.+)\]$") {
            if ($matches[1] -eq $Secao) { $dentroSecao = $true }
            else { $dentroSecao = $false }
            continue
        }
        
        if ($dentroSecao -and $linha -match "^([^=]+)=(.*)$") {
            if ($matches[1].Trim() -eq $Chave) {
                return $matches[2].Trim()
            }
        }
    }
    return $null
}

$pastaRetorno = Get-ConfigValue -Secao "CAMINHOS" -Chave "pasta_retorno"
$pastaTemp = Split-Path $pastaRetorno -Parent
$pastaTemp = Join-Path $pastaTemp "RetornoTemp"

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "            PROCESSAMENTO DE ARQUIVOS EXISTENTES" -ForegroundColor White
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  O watchdog so detecta NOVOS arquivos criados apos o monitor iniciar." -ForegroundColor Gray
Write-Host "  Este script processa arquivos que ja estavam na pasta." -ForegroundColor Gray
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Passo 1: Deletar IEDCBR
Write-Host "[Passo 1/3] Procurando arquivos IEDCBR para deletar..." -ForegroundColor Yellow
Write-Host ""

$iedFiles = Get-ChildItem "$pastaRetorno\IEDCBR*.ret" -ErrorAction SilentlyContinue

if ($iedFiles) {
    foreach ($file in $iedFiles) {
        Write-Host "  Deletando: $($file.Name)" -ForegroundColor White
        Remove-Item $file.FullName -Force -ErrorAction SilentlyContinue
    }
    Write-Host ""
    Write-Host "  Deletados: $($iedFiles.Count) arquivo(s) IEDCBR" -ForegroundColor Green
} else {
    Write-Host "  Nenhum arquivo IEDCBR encontrado" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[Passo 2/3] Procurando arquivos CBR724 para processar..." -ForegroundColor Yellow
Write-Host ""

$cbrFiles = Get-ChildItem "$pastaRetorno\CBR*.ret" -ErrorAction SilentlyContinue

if (-not $cbrFiles) {
    Write-Host "  Nenhum arquivo CBR724 encontrado." -ForegroundColor Gray
    Write-Host ""
    if (-not $iedFiles) {
        Write-Host "  Nenhum arquivo para processar." -ForegroundColor Yellow
    } else {
        Write-Host "  Apenas arquivos IEDCBR foram deletados." -ForegroundColor Green
    }
    Write-Host ""
    Start-Sleep -Seconds 3
    exit
}

Write-Host "  Encontrados: $($cbrFiles.Count) arquivo(s) CBR724" -ForegroundColor Green
Write-Host ""
Write-Host "[Passo 3/3] Movendo CBR724 para reprocessamento..." -ForegroundColor Yellow
Write-Host ""

# Criar pasta temp
if (-not (Test-Path $pastaTemp)) {
    New-Item -ItemType Directory -Path $pastaTemp -Force | Out-Null
}

# Mover para temp
foreach ($file in $cbrFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor White
    Move-Item $file.FullName -Destination "$pastaTemp\$($file.Name)" -Force
}

Write-Host ""
Write-Host "  Aguardando 3 segundos..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "  Movendo de volta (monitor vai detectar como 'novos')..." -ForegroundColor Gray
Write-Host ""

# Mover de volta (gera evento on_created)
$tempFiles = Get-ChildItem "$pastaTemp\CBR*.ret" -ErrorAction SilentlyContinue
foreach ($file in $tempFiles) {
    Write-Host "  + $($file.Name)" -ForegroundColor Green
    Move-Item $file.FullName -Destination "$pastaRetorno\$($file.Name)" -Force
    Start-Sleep -Seconds 1
}

# Limpar pasta temp
Remove-Item $pastaTemp -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  Processamento concluido!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

if ($iedFiles) {
    Write-Host "  Deletados: $($iedFiles.Count) arquivo(s) IEDCBR" -ForegroundColor Yellow
}
if ($cbrFiles) {
    Write-Host "  Reprocessados: $($cbrFiles.Count) arquivo(s) CBR724" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Verifique o log em: monitor_retornos.log" -ForegroundColor Gray
Write-Host ""
Start-Sleep -Seconds 3
