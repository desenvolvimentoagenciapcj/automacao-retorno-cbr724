# Script PowerShell para criar tarefas agendadas
# Executado com privilégios elevados

$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Configurando Início Automático" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Caminho base
$baseDir = Split-Path -Parent $PSCommandPath

# Remover tarefas antigas
Write-Host "[1/4] Removendo tarefas antigas..." -ForegroundColor Yellow
try {
    schtasks /Delete /TN "AutomacaoRetorno\Monitor" /F 2>&1 | Out-Null
} catch {}
try {
    schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F 2>&1 | Out-Null
} catch {}
try {
    schtasks /Delete /TN "AutomacaoRetorno\VerificacaoAposReinicio" /F 2>&1 | Out-Null
} catch {}
Write-Host "   OK" -ForegroundColor Green

# Criar XML para tarefa de início
Write-Host "[2/4] Criando tarefa de início automático..." -ForegroundColor Yellow

$xmlInicio = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Inicia automaticamente o Monitor de Retornos CBR724 ao iniciar o Windows</Description>
    <Author>Sistema de Automação</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Delay>PT2M</Delay>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$env:USERNAME</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$baseDir\scripts\bat\INICIAR_MONITOR_OCULTO.bat</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile1 = "$env:TEMP\monitor_task.xml"
$xmlInicio | Out-File -FilePath $xmlFile1 -Encoding unicode

schtasks /Create /XML $xmlFile1 /TN "AutomacaoRetorno\MonitorAutoInicio" /F | Out-Null
Remove-Item $xmlFile1 -Force
Write-Host "   OK - Tarefa criada" -ForegroundColor Green

# Criar XML para tarefa de verificação
Write-Host "[3/4] Criando tarefa de verificação pós-boot..." -ForegroundColor Yellow

$xmlVerificacao = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Verifica se o monitor iniciou corretamente após reinicialização</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Delay>PT10M</Delay>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$env:USERNAME</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <ExecutionTimeLimit>PT5M</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$baseDir\scripts\bat\VERIFICAR_APOS_BOOT.bat</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile2 = "$env:TEMP\verificacao_task.xml"
$xmlVerificacao | Out-File -FilePath $xmlFile2 -Encoding unicode

schtasks /Create /XML $xmlFile2 /TN "AutomacaoRetorno\VerificacaoAposReinicio" /F | Out-Null
Remove-Item $xmlFile2 -Force
Write-Host "   OK - Tarefa criada" -ForegroundColor Green

# Verificar
Write-Host "[4/4] Verificando tarefas criadas..." -ForegroundColor Yellow

$task1 = Get-ScheduledTask -TaskName "MonitorAutoInicio" -TaskPath "\AutomacaoRetorno\" -ErrorAction SilentlyContinue
$task2 = Get-ScheduledTask -TaskName "VerificacaoAposReinicio" -TaskPath "\AutomacaoRetorno\" -ErrorAction SilentlyContinue

if ($task1 -and $task2) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host " CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tarefas criadas:" -ForegroundColor Cyan
    Write-Host "  1. MonitorAutoInicio" -ForegroundColor White
    Write-Host "     - Inicia 2 minutos após boot" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. VerificacaoAposReinicio" -ForegroundColor White
    Write-Host "     - Verifica após 10 minutos" -ForegroundColor Gray
    Write-Host ""
    Write-Host "O sistema agora iniciará automaticamente!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERRO: Nem todas as tarefas foram criadas!" -ForegroundColor Red
    if (-not $task1) { Write-Host "  - MonitorAutoInicio: FALTANDO" -ForegroundColor Red }
    if (-not $task2) { Write-Host "  - VerificacaoAposReinicio: FALTANDO" -ForegroundColor Red }
}

Write-Host ""
Write-Host "Pressione qualquer tecla para fechar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
