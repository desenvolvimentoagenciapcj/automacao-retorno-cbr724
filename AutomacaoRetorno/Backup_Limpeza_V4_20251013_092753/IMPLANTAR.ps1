# =====================================================================
# SCRIPT DE IMPLANTACAO AUTOMATICA - PRODUCAO
# =====================================================================
# Servidor: \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ
# Data: 09/10/2025
# =====================================================================

param(
    [switch]$TestarApenasAcesso,
    [switch]$CriarEstrutura,
    [switch]$CopiarArquivos,
    [switch]$ImplantarCompleto
)

$ErrorActionPreference = "Stop"

# Configuracoes
$CAMINHO_PRODUCAO = "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ"
$CAMINHO_DEV = $PSScriptRoot
$PYTHON_PATH = "C:\Users\charles.oliveira.AGENCIAPCJ\AppData\Local\Programs\Python\Python313\python.exe"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " IMPLANTACAO DO SISTEMA EM PRODUCAO" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# =====================================================================
# FUNCAO: Testar Acesso
# =====================================================================
function Test-ServerAccess {
    Write-Host "Testando acesso ao servidor..." -ForegroundColor Yellow
    
    if (Test-Path $CAMINHO_PRODUCAO) {
        Write-Host "OK: Acesso ao servidor verificado`n" -ForegroundColor Green
        return $true
    } else {
        Write-Host "ERRO: Nao foi possivel acessar $CAMINHO_PRODUCAO`n" -ForegroundColor Red
        return $false
    }
}

# =====================================================================
# FUNCAO: Criar Estrutura de Pastas
# =====================================================================
function New-FolderStructure {
    Write-Host "`nCriando estrutura de pastas...`n" -ForegroundColor Yellow
    
    $pastas = @(
        "$CAMINHO_PRODUCAO\AutomacaoRetorno",
        "$CAMINHO_PRODUCAO\Retorno\Processados",
        "$CAMINHO_PRODUCAO\Retorno\Erro",
        "$CAMINHO_PRODUCAO\Retorno\ied",
        "$CAMINHO_PRODUCAO\Retorno\ied\2025"
    )
    
    foreach ($pasta in $pastas) {
        if (!(Test-Path $pasta)) {
            New-Item -ItemType Directory -Path $pasta -Force | Out-Null
            Write-Host "  OK: Criada: $pasta" -ForegroundColor Green
        } else {
            Write-Host "  INFO: Ja existe: $pasta" -ForegroundColor Gray
        }
    }
    
    Write-Host "`nEstrutura de pastas criada com sucesso!`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Ajustar Caminhos nos Arquivos Python
# =====================================================================
function Update-PythonFiles {
    Write-Host "`nAjustando caminhos nos arquivos Python...`n" -ForegroundColor Yellow
    
    $destino = "$CAMINHO_PRODUCAO\AutomacaoRetorno"
    
    # monitor_retornos.py
    $conteudo = Get-Content "$CAMINHO_DEV\monitor_retornos.py" -Raw
    $conteudo = $conteudo -replace 'pasta_entrada = Path\(r"D:\\Teste_Cobrança_Acess\\Retorno"\)', 'pasta_entrada = Path(r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno")'
    $conteudo = $conteudo -replace "r'D:\\Teste_Cobrança_Acess\\dbBaixa2025\.accdb'", "r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb'"
    $conteudo = $conteudo -replace "r'D:\\Teste_Cobrança_Acess\\Cobranca2019\.accdb'", "r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb'"
    $conteudo = $conteudo -replace "r'D:\\Teste_Cobrança_Acess\\Backup'", "r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup'"
    [System.IO.File]::WriteAllText("$destino\monitor_retornos.py", $conteudo)
    Write-Host "  OK: monitor_retornos.py ajustado" -ForegroundColor Green
    
    # integrador_access.py
    $conteudo = Get-Content "$CAMINHO_DEV\integrador_access.py" -Raw
    $conteudo = $conteudo -replace 'DB_BAIXA = r"D:\\Teste_Cobrança_Acess\\dbBaixa2025\.accdb"', 'DB_BAIXA = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb"'
    $conteudo = $conteudo -replace 'DB_COBRANCA = r"D:\\Teste_Cobrança_Acess\\Cobranca2019\.accdb"', 'DB_COBRANCA = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb"'
    $conteudo = $conteudo -replace 'PASTA_BACKUP = r"D:\\Teste_Cobrança_Acess\\Backup"', 'PASTA_BACKUP = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup"'
    [System.IO.File]::WriteAllText("$destino\integrador_access.py", $conteudo)
    Write-Host "  OK: integrador_access.py ajustado" -ForegroundColor Green
    
    # processador_cbr724.py (sem alteracoes, mas copiar)
    Copy-Item "$CAMINHO_DEV\processador_cbr724.py" -Destination "$destino\processador_cbr724.py" -Force
    Write-Host "  OK: processador_cbr724.py copiado" -ForegroundColor Green
    
    Write-Host "`nArquivos Python ajustados e copiados!`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Ajustar Scripts BAT
# =====================================================================
function Update-BatFiles {
    Write-Host "`nAjustando scripts BAT...`n" -ForegroundColor Yellow
    
    $destino = "$CAMINHO_PRODUCAO\AutomacaoRetorno"
    
    $batFiles = @(
        "INICIAR_MONITOR.bat",
        "INICIAR_MONITOR_OCULTO.bat",
        "INICIAR_MONITOR_MINIMIZADO.bat",
        "STATUS_MONITOR.bat",
        "PARAR_MONITOR.bat"
    )
    
    foreach ($bat in $batFiles) {
        $conteudo = Get-Content "$CAMINHO_DEV\$bat" -Raw
        $conteudo = $conteudo -replace 'D:\\Teste_Cobrança_Acess\\AutomacaoRetorno', '\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno'
        $conteudo = $conteudo -replace 'D:\\Teste_Cobrança_Acess\\Retorno', '\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno'
        [System.IO.File]::WriteAllText("$destino\$bat", $conteudo, [System.Text.Encoding]::Default)
        Write-Host "  OK: $bat ajustado" -ForegroundColor Green
    }
    
    Write-Host "`nScripts BAT ajustados e copiados!`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Ajustar Arquivo _start_monitor.bat
# =====================================================================
function Update-StartMonitorBat {
    Write-Host "`nAjustando _start_monitor.bat...`n" -ForegroundColor Yellow
    
    $destino = "$CAMINHO_PRODUCAO\AutomacaoRetorno"
    
    # Criar conteudo linha por linha
    $linha1 = "@echo off"
    $linha2 = "cd /d `"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno`""
    $linha3 = "`"C:\Users\charles.oliveira.AGENCIAPCJ\AppData\Local\Programs\Python\Python313\python.exe`" monitor_retornos.py"
    
    $conteudo = "$linha1`r`n$linha2`r`n$linha3"
    
    [System.IO.File]::WriteAllText("$destino\_start_monitor.bat", $conteudo, [System.Text.Encoding]::Default)
    
    # Copiar para C:\Temp tambem
    if (!(Test-Path "C:\Temp")) {
        New-Item -ItemType Directory -Path "C:\Temp" | Out-Null
    }
    [System.IO.File]::WriteAllText("C:\Temp\_start_cbr_monitor.bat", $conteudo, [System.Text.Encoding]::Default)
    
    Write-Host "  OK: _start_monitor.bat ajustado" -ForegroundColor Green
    Write-Host "  OK: Copiado para C:\Temp\_start_cbr_monitor.bat`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Copiar Arquivos Auxiliares
# =====================================================================
function Copy-AuxFiles {
    Write-Host "`nCopiando arquivos auxiliares...`n" -ForegroundColor Yellow
    
    $destino = "$CAMINHO_PRODUCAO\AutomacaoRetorno"
    
    $arquivos = @(
        "_run_hidden.vbs",
        "_check_monitor.ps1",
        "COMO_USAR.md",
        "APROVADO.md"
    )
    
    foreach ($arquivo in $arquivos) {
        Copy-Item "$CAMINHO_DEV\$arquivo" -Destination "$destino\$arquivo" -Force
        Write-Host "  OK: $arquivo copiado" -ForegroundColor Green
    }
    
    Write-Host "`nArquivos auxiliares copiados!`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Criar README de Producao
# =====================================================================
function New-ProductionReadme {
    Write-Host "`nCriando README de producao...`n" -ForegroundColor Yellow
    
    $dataHora = Get-Date -Format "dd/MM/yyyy HH:mm"
    
    $readme = @"
# SISTEMA EM PRODUCAO

**Servidor:** \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ
**Data de Implantacao:** $dataHora
**Status:** ATIVO

## Como Usar

### Iniciar Monitor (Modo Oculto - Recomendado)
``````
INICIAR_MONITOR_OCULTO.bat
``````

### Verificar Status
``````
STATUS_MONITOR.bat
``````

### Parar Monitor
``````
PARAR_MONITOR.bat
``````

## Pastas

- **Retorno\\** - Coloque arquivos .ret aqui
- **Retorno\\Processados\\** - Arquivos processados com sucesso
- **Retorno\\Erro\\** - Arquivos com erro
- **backup\\** - Backups automaticos dos bancos

## Logs

Veja detalhes em: ``monitor_retornos.log``

## Importante

- Sistema roda 24/7 em segundo plano
- Cria backup automatico antes de processar
- Move arquivos processados automaticamente
- Registra tudo em log

## Suporte

Veja documentacao completa em: ``COMO_USAR.md``

---

*Implantado em: $dataHora*
"@
    
    $destino = "$CAMINHO_PRODUCAO\AutomacaoRetorno"
    [System.IO.File]::WriteAllText("$destino\README_PRODUCAO.md", $readme)
    
    Write-Host "  OK: README_PRODUCAO.md criado`n" -ForegroundColor Green
}

# =====================================================================
# FUNCAO: Implantacao Completa
# =====================================================================
function Start-FullDeployment {
    Write-Host "`nIniciando implantacao completa...`n" -ForegroundColor Cyan
    
    # Passo 1: Testar Acesso
    if (!(Test-ServerAccess)) {
        Write-Host "Implantacao abortada - sem acesso ao servidor`n" -ForegroundColor Red
        return
    }
    
    # Passo 2: Criar Estrutura
    New-FolderStructure
    
    # Passo 3: Ajustar e Copiar Python
    Update-PythonFiles
    
    # Passo 4: Ajustar e Copiar BAT
    Update-BatFiles
    
    # Passo 5: Ajustar _start_monitor.bat
    Update-StartMonitorBat
    
    # Passo 6: Copiar Auxiliares
    Copy-AuxFiles
    
    # Passo 7: Criar README
    New-ProductionReadme
    
    Write-Host "`n=========================================" -ForegroundColor Green
    Write-Host " IMPLANTACAO CONCLUIDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "=========================================`n" -ForegroundColor Green
    
    Write-Host "PROXIMOS PASSOS:`n" -ForegroundColor Cyan
    Write-Host "  1. Acesse: \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno" -ForegroundColor White
    Write-Host "  2. Execute: INICIAR_MONITOR.bat (modo visivel para testar)" -ForegroundColor White
    Write-Host "  3. Copie um arquivo .ret para Retorno\" -ForegroundColor White
    Write-Host "  4. Verifique o processamento" -ForegroundColor White
    Write-Host "  5. Se OK, use: INICIAR_MONITOR_OCULTO.bat`n" -ForegroundColor White
    
    Write-Host "Localizacao: $CAMINHO_PRODUCAO\AutomacaoRetorno`n" -ForegroundColor Yellow
}

# =====================================================================
# EXECUCAO PRINCIPAL
# =====================================================================

if ($TestarApenasAcesso) {
    Test-ServerAccess
}
elseif ($CriarEstrutura) {
    if (Test-ServerAccess) {
        New-FolderStructure
    }
}
elseif ($CopiarArquivos) {
    if (Test-ServerAccess) {
        Update-PythonFiles
        Update-BatFiles
        Update-StartMonitorBat
        Copy-AuxFiles
        New-ProductionReadme
    }
}
elseif ($ImplantarCompleto) {
    Start-FullDeployment
}
else {
    Write-Host "`nUSO DO SCRIPT:`n" -ForegroundColor Yellow
    Write-Host "  Testar acesso:          .\IMPLANTAR.ps1 -TestarApenasAcesso" -ForegroundColor White
    Write-Host "  Criar estrutura:        .\IMPLANTAR.ps1 -CriarEstrutura" -ForegroundColor White
    Write-Host "  Copiar arquivos:        .\IMPLANTAR.ps1 -CopiarArquivos" -ForegroundColor White
    Write-Host "  Implantacao completa:   .\IMPLANTAR.ps1 -ImplantarCompleto`n" -ForegroundColor White
    Write-Host "Recomendado: Use -ImplantarCompleto para fazer tudo de uma vez`n" -ForegroundColor Cyan
}
