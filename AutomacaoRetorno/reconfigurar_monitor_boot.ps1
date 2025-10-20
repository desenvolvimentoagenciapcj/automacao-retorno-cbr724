# Reconfigura MonitorAutoInicio para rodar como SYSTEM e iniciar no boot
$ErrorActionPreference = 'Continue'

Write-Host "Reconfigurando MonitorAutoInicio para rodar como SYSTEM no boot..." -ForegroundColor Cyan

# Remover tarefa existente
schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F 2>&1 | Out-Null

$baseDir = Split-Path -Parent $PSCommandPath

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Inicia o Monitor de Retornos no Boot como SYSTEM</Description>
    <Author>Sistema de Automação</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Delay>PT1M</Delay>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>SYSTEM</UserId>
      <LogonType>ServiceAccount</LogonType>
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
      <Command>$baseDir\scripts\bat\INICIAR_MONITOR_OCULTO.bat</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile = "$env:TEMP\monitor_boot_sys.xml"
$xml | Out-File -FilePath $xmlFile -Encoding unicode

schtasks /Create /XML $xmlFile /TN "AutomacaoRetorno\MonitorAutoInicio" /F | Out-Null
Remove-Item $xmlFile -Force

Write-Host "Pronto - tarefa MonitorAutoInicio configurada para SYSTEM" -ForegroundColor Green
