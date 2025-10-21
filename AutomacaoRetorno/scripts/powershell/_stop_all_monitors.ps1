# ============================================================================
# Para TODOS os monitores rodando (VERSAO SILENCIOSA)
# ============================================================================

$allPython = Get-Process python -ErrorAction SilentlyContinue

if ($allPython) {
    $monitors = @()
    
    foreach ($proc in $allPython) {
        try {
            $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.Id)" -ErrorAction SilentlyContinue).CommandLine
            if ($cmdLine -like "*monitor_retornos.py*") {
                $monitors += $proc
            }
        } catch {
            # Ignorar erros
        }
    }
    
    if ($monitors.Count -gt 0) {
        $monitors | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }
}
