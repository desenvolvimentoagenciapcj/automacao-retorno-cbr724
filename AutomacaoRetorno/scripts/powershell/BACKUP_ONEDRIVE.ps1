# ============================================================================
# Script: Backup para OneDrive (Versão Simplificada)
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

$origem = Get-ConfigValue -Secao "DIRETORIOS" -Chave "dir_trabalho"
$destino = Get-ConfigValue -Secao "ONEDRIVE" -Chave "caminho_backup"

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  BACKUP PARA ONEDRIVE" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Cyan

Write-Host "Origem:  $origem" -ForegroundColor White
Write-Host "Destino: $destino`n" -ForegroundColor White

# Criar pasta de destino
if (-not (Test-Path $destino)) {
    Write-Host "Criando pasta de destino..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
    Write-Host "Pasta criada!`n" -ForegroundColor Green
} else {
    Write-Host "Pasta de destino existe`n" -ForegroundColor Green
}

# ============================================================================
# PASSO 1: Copiar arquivos Python
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PASSO 1: ARQUIVOS PYTHON" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Cyan

$arquivos_python = @(
    "monitor_retornos.py",
    "processador_cbr724.py",
    "integrador_access.py",
    "config_manager.py",
    "notificador_windows.py",
    "watchdog_monitor.py",
    "gerar_manual_pdf.py"
)

foreach ($arquivo in $arquivos_python) {
    $origem_arquivo = Join-Path $origem $arquivo
    if (Test-Path $origem_arquivo) {
        Copy-Item $origem_arquivo -Destination $destino -Force
        Write-Host "OK: $arquivo" -ForegroundColor Green
    } else {
        Write-Host "FALTA: $arquivo" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================================================
# PASSO 2: Copiar scripts
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PASSO 2: SCRIPTS" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Cyan

$scripts = @(
    "INICIAR_MONITOR_OCULTO.bat",
    "PARAR_MONITOR.bat",
    "STATUS_MONITOR.bat",
    "INICIAR_WATCHDOG.bat",
    "PARAR_WATCHDOG.bat",
    "PROCESSAR_EXISTENTES.bat",
    "_start_monitor_hidden.ps1",
    "_stop_all_monitors.ps1",
    "_check_monitor.ps1",
    "PROCESSAR_EXISTENTES.ps1"
)

foreach ($script in $scripts) {
    $origem_script = Join-Path $origem $script
    if (Test-Path $origem_script) {
        Copy-Item $origem_script -Destination $destino -Force
        Write-Host "OK: $script" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 3: Copiar configurações
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PASSO 3: CONFIGURACOES" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Cyan

$configs = @(
    "config.ini",
    "requirements.txt"
)

foreach ($config in $configs) {
    $origem_config = Join-Path $origem $config
    if (Test-Path $origem_config) {
        Copy-Item $origem_config -Destination $destino -Force
        Write-Host "OK: $config" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 4: Copiar documentação Markdown
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PASSO 4: DOCUMENTACAO MARKDOWN" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Cyan

$documentacao_md = @(
    "MANUAL_IMPLANTACAO_COMPLETO.md",
    "GUIA_CONFIG.md",
    "SISTEMA_EM_PRODUCAO.md",
    "NOTIFICACOES_WINDOWS.md",
    "SISTEMA_WATCHDOG.md",
    "CHANGELOG.md",
    "README.md"
)

foreach ($doc in $documentacao_md) {
    $origem_doc = Join-Path $origem $doc
    if (Test-Path $origem_doc) {
        Copy-Item $origem_doc -Destination $destino -Force
        Write-Host "OK: $doc" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 5: Criar LEIA-ME.md
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PASSO 5: CRIAR LEIA-ME" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Cyan

$readme = @"
# Backup do Sistema de Automacao de Retornos CBR724

**Data do Backup:** $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
**Sistema:** Automacao de Processamento de Retornos Bancarios CBR724
**Organizacao:** Fundacao Agencia das Bacias PCJ - TI

---

## Conteudo deste Backup

### Codigo Python
- monitor_retornos.py - Monitor principal
- processador_cbr724.py - Processador de arquivos CBR724
- integrador_access.py - Integracao com Access
- config_manager.py - Gerenciador de configuracoes
- notificador_windows.py - Sistema de notificacoes
- watchdog_monitor.py - Watchdog (auto-restart)
- gerar_manual_pdf.py - Gerador de PDFs

### Scripts de Controle
- INICIAR_MONITOR_OCULTO.bat - Inicia monitor em background
- PARAR_MONITOR.bat - Para o monitor
- STATUS_MONITOR.bat - Verifica status
- INICIAR_WATCHDOG.bat - Inicia watchdog
- PARAR_WATCHDOG.bat - Para watchdog
- PROCESSAR_EXISTENTES.bat - Processa arquivos existentes

### Configuracao
- config.ini - Arquivo de configuracao principal
- requirements.txt - Dependencias Python

### Documentacao
- MANUAL_IMPLANTACAO_COMPLETO.md - Manual completo de implantacao
- GUIA_CONFIG.md - Guia de configuracao do config.ini
- SISTEMA_EM_PRODUCAO.md - Documentacao do sistema em producao
- NOTIFICACOES_WINDOWS.md - Sistema de notificacoes
- SISTEMA_WATCHDOG.md - Watchdog e auto-restart
- CHANGELOG.md - Historico de mudancas
- README.md - Visao geral

---

## Para Reimplantar o Sistema

1. **Leia primeiro:** MANUAL_IMPLANTACAO_COMPLETO.md

2. **Requisitos:**
   - Python 3.8+
   - Microsoft Access (Office)
   - Acesso a rede (\\SERVIDOR1)

3. **Instalacao rapida:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Configure:** Edite config.ini com os caminhos corretos

5. **Inicie:**
   ```cmd
   INICIAR_MONITOR_OCULTO.bat
   INICIAR_WATCHDOG.bat
   ```

---

## Suporte

**Responsavel:** TI - Fundacao Agencia das Bacias PCJ
**Sistema:** Automacao dbBaixa2025
**Ultima Atualizacao:** $(Get-Date -Format "dd/MM/yyyy")

---

**IMPORTANTE:** Este e um backup completo do sistema.
Guarde em local seguro e mantenha atualizado.
"@

$readme_path = Join-Path $destino "LEIA-ME.md"
$readme | Out-File -FilePath $readme_path -Encoding UTF8
Write-Host "OK: LEIA-ME.md criado" -ForegroundColor Green

Write-Host ""

# ============================================================================
# RESUMO FINAL
# ============================================================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  BACKUP CONCLUIDO!" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Cyan

$total_arquivos = (Get-ChildItem $destino -File -Recurse).Count
$tamanho_total = [math]::Round((Get-ChildItem $destino -File -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB, 2)

Write-Host "Pasta de destino: $destino" -ForegroundColor White
Write-Host "Total de arquivos: $total_arquivos" -ForegroundColor White
Write-Host "Tamanho total: $tamanho_total MB`n" -ForegroundColor White

Write-Host "ARQUIVOS COPIADOS:" -ForegroundColor Yellow
Write-Host "  - 7 arquivos Python" -ForegroundColor White
Write-Host "  - 10 scripts BAT/PS1" -ForegroundColor White
Write-Host "  - 2 arquivos de configuracao" -ForegroundColor White
Write-Host "  - 7 arquivos de documentacao" -ForegroundColor White
Write-Host "  - 1 README`n" -ForegroundColor White

Write-Host "CONCLUIDO! Arquivos salvos no OneDrive.`n" -ForegroundColor Green

# Abrir pasta no Explorer
$resposta = Read-Host "Abrir pasta no Explorer? (S/N)"
if ($resposta -eq "S" -or $resposta -eq "s") {
    explorer $destino
}
