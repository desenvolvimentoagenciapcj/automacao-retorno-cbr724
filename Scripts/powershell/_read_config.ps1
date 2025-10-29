# ============================================================================
# Script auxiliar para ler configurações do config.ini
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Secao,
    
    [Parameter(Mandatory=$true)]
    [string]$Chave
)

# Caminho relativo: scripts/powershell -> AutomacaoRetorno -> config/config.ini
$raizProjeto = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$configPath = Join-Path $raizProjeto "config\config.ini"

if (-not (Test-Path $configPath)) {
    Write-Error "config.ini não encontrado em: $configPath"
    exit 1
}

$conteudo = Get-Content $configPath -Encoding UTF8

$dentroSecao = $false
foreach ($linha in $conteudo) {
    # Remove espaços em branco
    $linha = $linha.Trim()
    
    # Pula comentários e linhas vazias
    if ($linha -match "^#" -or $linha -eq "") {
        continue
    }
    
    # Verifica se é uma seção
    if ($linha -match "^\[(.+)\]$") {
        $secaoAtual = $matches[1]
        if ($secaoAtual -eq $Secao) {
            $dentroSecao = $true
        } else {
            $dentroSecao = $false
        }
        continue
    }
    
    # Se estamos na seção correta, procura a chave
    if ($dentroSecao -and $linha -match "^([^=]+)=(.*)$") {
        $chaveAtual = $matches[1].Trim()
        $valor = $matches[2].Trim()
        
        if ($chaveAtual -eq $Chave) {
            Write-Output $valor
            exit 0
        }
    }
}

Write-Error "Chave '$Chave' não encontrada na seção [$Secao]"
exit 1
