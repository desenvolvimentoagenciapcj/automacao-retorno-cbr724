# ============================================================================
# Configurar Inicialização via Registro Windows (Fallback mais robusto)
# ============================================================================
# Este script configura a inicialização do monitor via Registry Run
# que executa ANTES de qualquer tarefa agendada e independente de logon

$ErrorActionPreference = "Stop"

Write-Host "`n════════════════════════════════════════════════════════════════════"
Write-Host "⚙️  CONFIGURANDO INICIALIZAÇÃO VIA REGISTRO WINDOWS (FALLBACK)"
Write-Host "════════════════════════════════════════════════════════════════════`n"

# Diretório do projeto
$projectRoot = "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
$batFile = "$projectRoot\scripts\bat\INICIAR_MONITOR_OCULTO.bat"

# Verificar se arquivo exists
if (-not (Test-Path $batFile)) {
    Write-Host "❌ Erro: Arquivo não encontrado: $batFile`n" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Configurações:`n" -ForegroundColor Cyan
Write-Host "   Arquivo BAT: $batFile"
Write-Host "   Chave Registro: HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
Write-Host "   Nome: MonitorAutoInicio`n"

# Criar entrada no Registro (CurrentUser - Autoruns)
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$regName = "MonitorAutoInicio"

# Comando para executar o BAT
$command = "`"$batFile`""

try {
    # Criar/atualizar chave no registro
    if (-not (Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    
    New-ItemProperty -Path $regPath -Name $regName -Value $command -PropertyType String -Force | Out-Null
    
    Write-Host "✅ Registro Windows atualizado com sucesso!`n" -ForegroundColor Green
    Write-Host "📍 Localização: $regPath\$regName" -ForegroundColor Yellow
    Write-Host "💾 Valor: $command`n"
    
} catch {
    Write-Host "❌ Erro ao configurar registro: $_`n" -ForegroundColor Red
    exit 1
}

# Verificar se foi criado
$verify = Get-ItemProperty -Path $regPath -Name $regName -ErrorAction SilentlyContinue
if ($verify) {
    Write-Host "✓ Verificação OK - Entrada existe no registro`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Verificação falhou - Entrada não encontrada`n" -ForegroundColor Yellow
}

Write-Host "════════════════════════════════════════════════════════════════════"
Write-Host "🎯 Próximo passo:"
Write-Host "════════════════════════════════════════════════════════════════════"
Write-Host ""
Write-Host "   1️⃣  Reinicie o computador para testar"
Write-Host "   2️⃣  O monitor deve iniciar automaticamente após o login"
Write-Host "   3️⃣  Verifique com: STATUS_MONITOR.bat"
Write-Host ""
Write-Host "💡 Dica: Se você remover via Registry cleaner, execute este script novamente"
Write-Host "`n════════════════════════════════════════════════════════════════════`n"

