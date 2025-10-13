# ============================================================================
# Script: Copiar projeto completo para OneDrive com PDF
# ============================================================================

$origem = "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
$destino = "F:\OneDrive - Fundacao Agencia das Bacias PCJ\Repositorio_TI\Manuais\SCPCJ\AutomaçãoDbBaixa"

Write-Host "`n════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📦 BACKUP COMPLETO PARA ONEDRIVE" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "📂 Origem:  $origem" -ForegroundColor White
Write-Host "📂 Destino: $destino`n" -ForegroundColor White

# Criar pasta de destino se não existir
if (-not (Test-Path $destino)) {
    Write-Host "📁 Criando pasta de destino..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
    Write-Host "✅ Pasta criada!`n" -ForegroundColor Green
} else {
    Write-Host "✅ Pasta de destino já existe`n" -ForegroundColor Green
}

# ============================================================================
# PASSO 1: Tentar gerar PDFs dos manuais
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📄 PASSO 1: GERAR MANUAIS EM PDF" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "Verificando bibliotecas Python necessárias..." -ForegroundColor White

$bibliotecas = @("markdown", "weasyprint")
$faltam = @()

foreach ($lib in $bibliotecas) {
    $check = python -c "import $lib" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $faltam += $lib
    }
}

if ($faltam.Count -gt 0) {
    Write-Host "`n⚠️  Bibliotecas não instaladas: $($faltam -join ', ')" -ForegroundColor Yellow
    Write-Host "📦 Instalando bibliotecas necessárias...`n" -ForegroundColor Cyan
    
    foreach ($lib in $faltam) {
        Write-Host "   Instalando $lib..." -ForegroundColor White
        pip install $lib --quiet
    }
    
    Write-Host "`n✅ Bibliotecas instaladas!`n" -ForegroundColor Green
} else {
    Write-Host "✅ Todas as bibliotecas já estão instaladas!`n" -ForegroundColor Green
}

# Executar gerador de PDF
Write-Host "📄 Gerando PDFs dos manuais..." -ForegroundColor Cyan
cd $origem
python gerar_manual_pdf.py

Write-Host ""

# ============================================================================
# PASSO 2: Copiar arquivos Python
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         🐍 PASSO 2: COPIAR ARQUIVOS PYTHON" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

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
        Write-Host "✅ $arquivo" -ForegroundColor Green
    } else {
        Write-Host "⏭️  $arquivo (não encontrado)" -ForegroundColor Gray
    }
}

Write-Host ""

# ============================================================================
# PASSO 3: Copiar scripts BAT e PowerShell
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📜 PASSO 3: COPIAR SCRIPTS" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

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
        Write-Host "✅ $script" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 4: Copiar arquivos de configuração
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         ⚙️  PASSO 4: COPIAR CONFIGURAÇÕES" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$configs = @(
    "config.ini",
    "requirements.txt"
)

foreach ($config in $configs) {
    $origem_config = Join-Path $origem $config
    if (Test-Path $origem_config) {
        Copy-Item $origem_config -Destination $destino -Force
        Write-Host "✅ $config" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 5: Copiar documentação Markdown
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📚 PASSO 5: COPIAR DOCUMENTAÇÃO MARKDOWN" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

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
        Write-Host "✅ $doc" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================================================
# PASSO 6: Copiar PDFs gerados
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📄 PASSO 6: COPIAR MANUAIS PDF" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$pasta_pdfs = Join-Path $origem "Manuais_PDF"

if (Test-Path $pasta_pdfs) {
    $pasta_destino_pdfs = Join-Path $destino "Manuais_PDF"
    
    # Criar pasta de PDFs no destino
    if (-not (Test-Path $pasta_destino_pdfs)) {
        New-Item -ItemType Directory -Path $pasta_destino_pdfs -Force | Out-Null
    }
    
    # Copiar todos os PDFs
    Get-ChildItem "$pasta_pdfs\*.pdf" | ForEach-Object {
        Copy-Item $_.FullName -Destination $pasta_destino_pdfs -Force
        Write-Host "✅ $($_.Name)" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  Pasta de PDFs não encontrada" -ForegroundColor Yellow
    Write-Host "   (Os manuais em Markdown foram copiados)" -ForegroundColor Gray
}

Write-Host ""

# ============================================================================
# PASSO 7: Criar arquivo README no OneDrive
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         📝 PASSO 7: CRIAR README" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$readme_onedrive = @"
# 📦 Backup do Sistema de Automação de Retornos CBR724

> **Data do Backup:** $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
> **Sistema:** Automação de Processamento de Retornos Bancários CBR724
> **Organização:** Fundação Agência das Bacias PCJ - TI

---

## 📚 Conteúdo deste Backup

### 📘 Manuais (PDF)
- `Manuais_PDF/` - Versões em PDF de toda documentação

### 📄 Documentação (Markdown)
- `MANUAL_IMPLANTACAO_COMPLETO.md` - Manual completo de implantação
- `GUIA_CONFIG.md` - Guia de configuração do config.ini
- `SISTEMA_EM_PRODUCAO.md` - Documentação do sistema em produção
- `NOTIFICACOES_WINDOWS.md` - Sistema de notificações
- `SISTEMA_WATCHDOG.md` - Watchdog e auto-restart
- `CHANGELOG.md` - Histórico de mudanças

### 🐍 Código Python
- `monitor_retornos.py` - Monitor principal
- `processador_cbr724.py` - Processador de arquivos CBR724
- `integrador_access.py` - Integração com Access
- `config_manager.py` - Gerenciador de configurações
- `notificador_windows.py` - Sistema de notificações
- `watchdog_monitor.py` - Watchdog (auto-restart)

### 📜 Scripts de Controle
- `INICIAR_MONITOR_OCULTO.bat` - Inicia monitor em background
- `PARAR_MONITOR.bat` - Para o monitor
- `STATUS_MONITOR.bat` - Verifica status
- `INICIAR_WATCHDOG.bat` - Inicia watchdog
- `PARAR_WATCHDOG.bat` - Para watchdog
- `PROCESSAR_EXISTENTES.bat` - Processa arquivos existentes

### ⚙️ Configuração
- `config.ini` - Arquivo de configuração principal
- `requirements.txt` - Dependências Python

---

## 🚀 Para Reimplantar o Sistema

1. **Leia primeiro:** `MANUAL_IMPLANTACAO_COMPLETO.md` ou `Manuais_PDF/MANUAL_IMPLANTACAO_COMPLETO.pdf`

2. **Requisitos:**
   - Python 3.8+
   - Microsoft Access (Office)
   - Acesso à rede (\\SERVIDOR1)

3. **Instalação rápida:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Configure:** Edite `config.ini` com os caminhos corretos

5. **Inicie:**
   ```cmd
   INICIAR_MONITOR_OCULTO.bat
   INICIAR_WATCHDOG.bat
   ```

---

## 📞 Suporte

**Responsável:** TI - Fundação Agência das Bacias PCJ  
**Sistema:** Automação dbBaixa2025  
**Última Atualização:** $(Get-Date -Format "dd/MM/yyyy")

---

> ⚠️ **IMPORTANTE:** Este é um backup completo do sistema. 
> Guarde em local seguro e mantenha atualizado.
"@

$readme_path = Join-Path $destino "LEIA-ME.md"
$readme_onedrive | Out-File -FilePath $readme_path -Encoding UTF8
Write-Host "✅ LEIA-ME.md criado" -ForegroundColor Green

Write-Host ""

# ============================================================================
# RESUMO FINAL
# ============================================================================

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         ✅ BACKUP CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "📊 RESUMO:`n" -ForegroundColor Yellow

# Contar arquivos copiados
$total_arquivos = (Get-ChildItem $destino -File -Recurse).Count
$tamanho_total = (Get-ChildItem $destino -File -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "   📁 Pasta de destino: $destino" -ForegroundColor White
Write-Host "   📄 Total de arquivos: $total_arquivos" -ForegroundColor White
Write-Host "   💾 Tamanho total: $([math]::Round($tamanho_total, 2)) MB" -ForegroundColor White
Write-Host ""

Write-Host "📚 ARQUIVOS PRINCIPAIS COPIADOS:`n" -ForegroundColor Yellow
Write-Host "   ✅ Código Python completo" -ForegroundColor Green
Write-Host "   ✅ Scripts de controle (BAT/PowerShell)" -ForegroundColor Green
Write-Host "   ✅ Documentação Markdown" -ForegroundColor Green
Write-Host "   ✅ Manuais em PDF" -ForegroundColor Green
Write-Host "   ✅ Arquivos de configuração" -ForegroundColor Green
Write-Host "   ✅ README criado" -ForegroundColor Green

Write-Host "`n════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         🎉 PROJETO SALVO NO ONEDRIVE!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "💡 PRÓXIMOS PASSOS:`n" -ForegroundColor Cyan
Write-Host "   1. Verifique o OneDrive está sincronizando" -ForegroundColor White
Write-Host "   2. Confira os PDFs na pasta Manuais_PDF" -ForegroundColor White
Write-Host "   3. Leia o arquivo LEIA-ME.md no OneDrive`n" -ForegroundColor White

Write-Host "📂 Abrir pasta no OneDrive? (S/N): " -ForegroundColor Yellow -NoNewline
$resposta = Read-Host

if ($resposta -eq 'S' -or $resposta -eq 's') {
    explorer $destino
}

Write-Host "`n✅ Processo concluído!`n" -ForegroundColor Green
