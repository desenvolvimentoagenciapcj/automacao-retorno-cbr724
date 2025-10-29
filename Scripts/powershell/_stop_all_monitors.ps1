# ============================================================================
# Para TODOS os monitores rodando (limpeza completa)
# ============================================================================

Write-Host "`n=== PARANDO TODOS OS MONITORES ===" -ForegroundColor Yellow
Write-Host ""

# Procurar TODOS processos Python que estão rodando monitor_retornos.py
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
            # Ignorar erros de acesso
        }
    }
    
    if ($monitors.Count -gt 0) {
        Write-Host "Encontrados $($monitors.Count) monitor(es) rodando:" -ForegroundColor Cyan
        Write-Host ""
        
        foreach ($proc in $monitors) {
            Write-Host "  - PID: $($proc.Id)" -ForegroundColor White
            Write-Host "    Iniciado: $($proc.StartTime)" -ForegroundColor Gray
            Write-Host "    Memoria: $([math]::Round($proc.WorkingSet64/1MB, 1)) MB" -ForegroundColor Gray
            Write-Host ""
        }
        
        Write-Host "Encerrando processos..." -ForegroundColor Yellow
        $monitors | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        # Verificar se foram encerrados
        $remaining = @()
        foreach ($proc in $monitors) {
            $check = Get-Process -Id $proc.Id -ErrorAction SilentlyContinue
            if ($check) {
                $remaining += $check
            }
        }
        
        if ($remaining.Count -gt 0) {
            Write-Host "Alguns processos nao responderam. Forcando encerramento..." -ForegroundColor Red
            $remaining | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
        }
        
        Write-Host "Todos os monitores foram encerrados" -ForegroundColor Green
        
    } else {
        Write-Host "Nenhum monitor rodando" -ForegroundColor Gray
    }
} else {
    Write-Host "Nenhum processo Python rodando" -ForegroundColor Gray
}

Write-Host ""
