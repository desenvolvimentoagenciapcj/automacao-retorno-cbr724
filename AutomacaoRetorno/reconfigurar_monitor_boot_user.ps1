# Reconfigura MonitorAutoInicio para rodar como o usuário atual, StartWhenAvailable true e sem exigir rede
$ErrorActionPreference = 'Continue'

Write-Host "Reconfigurando MonitorAutoInicio para rodar como usuário atual..." -ForegroundColor Cyan

# Remover tarefa existente
schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F 2>$null | Out-Null

$baseDir = Split-Path -Parent $PSCommandPath
$batPath = Join-Path $baseDir 'scripts\bat\INICIAR_MONITOR_OCULTO.bat'

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Inicia o Monitor de Retornos no Boot como usuário</Description>
    <Author>Sistema de Automação</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Delay>PT1M</Delay>
      <Enabled>true</Enabled>
    </BootTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
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
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$batPath</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile = "$env:TEMP\monitor_boot_user.xml"
$xml | Out-File -FilePath $xmlFile -Encoding unicode

schtasks /Create /XML $xmlFile /TN "AutomacaoRetorno\MonitorAutoInicio" /F | Out-Null
Remove-Item $xmlFile -Force

Write-Host "Pronto - tarefa MonitorAutoInicio configurada com usuário $env:USERNAME" -ForegroundColor Green
