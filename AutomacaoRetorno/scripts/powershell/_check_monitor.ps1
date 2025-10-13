# Procura processo Python rodando monitor_retornos.py
$processo = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine
    $cmdLine -like '*monitor_retornos.py*'
}

if ($processo) {
    Write-Output $processo.Id
}
