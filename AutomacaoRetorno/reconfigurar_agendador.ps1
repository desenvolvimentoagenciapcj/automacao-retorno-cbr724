# Script PowerShell para reconfigurar tarefa do Agendador
# Executa uma vez por dia (início do expediente)

$ErrorActionPreference = "Continue"

Write-Host "Reconfigurando tarefa do Agendador..." -ForegroundColor Cyan

# Remover tarefa antiga
schtasks /Delete /TN "AutomacaoRetorno\Agendador" /F 2>&1 | Out-Null

# Criar XML da tarefa com gatilho diário
$baseDir = Split-Path -Parent $PSCommandPath

$xmlAgendador = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Agendador de Verificação - Verifica se monitor está ativo às 8h30</Description>
    <Author>Sistema de Automação</Author>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-10-17T08:30:00</StartBoundary>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
      <Enabled>true</Enabled>
    </CalendarTrigger>
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
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$baseDir\scripts\bat\INICIAR_AGENDADOR_OCULTO.bat</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile = "$env:TEMP\agendador_task.xml"
$xmlAgendador | Out-File -FilePath $xmlFile -Encoding unicode

schtasks /Create /XML $xmlFile /TN "AutomacaoRetorno\Agendador" /F 2>&1 | Out-Null
Remove-Item $xmlFile -Force

Write-Host "✅ Tarefa reconfigu​rada!" -ForegroundColor Green
Write-Host ""
Write-Host "A tarefa agora vai rodar:" -ForegroundColor Cyan
Write-Host "  • Todos os dias às 8h30" -ForegroundColor White
Write-Host "  • Irá iniciar o agendador se não estiver rodando" -ForegroundColor White
Write-Host ""

$task = Get-ScheduledTask -TaskName "Agendador" -TaskPath "\AutomacaoRetorno\"
Write-Host "Status: $($task.State)" -ForegroundColor Green
