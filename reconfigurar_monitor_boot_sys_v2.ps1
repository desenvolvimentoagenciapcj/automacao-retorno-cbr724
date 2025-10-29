# Reconfigura MonitorAutoInicio para rodar como SYSTEM usando XML (v2)
$ErrorActionPreference = 'Continue'

Write-Host "Reconfigurando MonitorAutoInicio (v2) para SYSTEM..." -ForegroundColor Cyan

# Remove se existir
schtasks /Delete /TN "AutomacaoRetorno\MonitorAutoInicio" /F 2>$null | Out-Null

$baseDir = Split-Path -Parent $PSCommandPath
$batPath = Join-Path $baseDir 'scripts\bat\INICIAR_MONITOR_OCULTO.bat'

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Inicia o Monitor de Retornos no Boot como SYSTEM (v2)</Description>
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
      <Command>$batPath</Command>
      <WorkingDirectory>$baseDir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$xmlFile = "$env:TEMP\monitor_boot_sys_v2.xml"
$xml | Out-File -FilePath $xmlFile -Encoding unicode

schtasks /Create /XML $xmlFile /TN "AutomacaoRetorno\MonitorAutoInicio" /F 2>&1 | Out-Null
$return = $LASTEXITCODE
Remove-Item $xmlFile -Force

if ($return -eq 0) { Write-Host "Tarefa criada com sucesso" -ForegroundColor Green } else { Write-Host "Erro ao criar a tarefa (código $return)" -ForegroundColor Red }
