@echo off
chcp 65001 > nul
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════
echo  🧪 TESTE DE RECUPERAÇÃO APÓS QUEDA DO SERVIDOR
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Este script testa se o sistema se recupera automaticamente
echo  após uma queda de servidor.
echo.
echo  ⚠️  ATENÇÃO: Este é um teste destrutivo!
echo      Não execute em produção sem supervisão.
echo.
echo ───────────────────────────────────────────────────────────────
echo  ETAPAS DO TESTE:
echo ───────────────────────────────────────────────────────────────
echo.
echo  1. ✅ Verificar se monitor está rodando
echo  2. 📋 Verificar configuração de monitoramento
echo  3. ⏸️  Simular queda (desconectar rede ou desligar servidor)
echo  4. ⏰ Aguardar 6 minutos (1 minuto + intervalo de verificação)
echo  5. 🔌 Reconectar servidor
echo  6. 📊 Verificar se sistema recuperou automaticamente
echo  7. 📁 Verificar se arquivos pendentes foram processados
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 1: Verificar Status do Monitor
echo ═══════════════════════════════════════════════════════════════
echo.

call "%~dp0STATUS.bat"

echo.
echo ───────────────────────────────────────────────────────────────
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 2: Verificar Configuração de Monitoramento
echo ═══════════════════════════════════════════════════════════════
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$config = Get-Content '%~dp0config\config.ini' -Raw; ^
if ($config -match '\[MONITORAMENTO_SERVIDOR\]') { ^
    Write-Host '✅ Seção [MONITORAMENTO_SERVIDOR] encontrada' -ForegroundColor Green; ^
    if ($config -match 'habilitado\s*=\s*true') { ^
        Write-Host '✅ Monitoramento habilitado' -ForegroundColor Green; ^
    } else { ^
        Write-Host '❌ Monitoramento DESABILITADO - teste não funcionará!' -ForegroundColor Red; ^
        exit 1; ^
    } ^
    if ($config -match 'intervalo_verificacao\s*=\s*(\d+)') { ^
        $intervalo = $matches[1]; ^
        Write-Host \"✅ Intervalo: $intervalo segundos ($([math]::Round($intervalo/60,1)) minutos)\" -ForegroundColor Green; ^
    } ^
    if ($config -match 'alertar_por_email\s*=\s*true') { ^
        Write-Host '✅ Alertas por email habilitados' -ForegroundColor Green; ^
    } ^
} else { ^
    Write-Host '⚠️  Seção [MONITORAMENTO_SERVIDOR] não encontrada' -ForegroundColor Yellow; ^
    Write-Host '   Sistema usará configurações padrão (5 minutos)' -ForegroundColor Yellow; ^
}"

echo.
echo ───────────────────────────────────────────────────────────────
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 3: Instruções para Simular Queda
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Para simular queda do servidor, você pode:
echo.
echo  OPÇÃO A - Desconectar unidade de rede:
echo     1. Abrir "Este Computador"
echo     2. Clicar com botão direito na unidade mapeada
echo     3. Selecionar "Desconectar"
echo.
echo  OPÇÃO B - Renomear pasta temporariamente:
echo     1. No servidor, renomear pasta "Retorno"
echo     2. Adicionar sufixo "_TESTE" no nome
echo.
echo  OPÇÃO C - Desligar servidor (⚠️ CUIDADO!)
echo.
echo  ⏰ Após simular a queda, aguarde 6+ minutos antes de prosseguir
echo     (tempo suficiente para o monitor detectar o problema)
echo.
echo ───────────────────────────────────────────────────────────────
echo.
echo  Pressione qualquer tecla DEPOIS de simular a queda...
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 4: Aguardando Detecção (6 minutos)...
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ⏰ Aguardando 6 minutos para monitor detectar problema...
echo     Acompanhe o log em tempo real: logs\monitor_retornos.log
echo.

timeout /t 360 /nobreak

echo.
echo ───────────────────────────────────────────────────────────────
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 5: Verificar Logs (Deve mostrar alerta de servidor)
echo ═══════════════════════════════════════════════════════════════
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Get-Content '%~dp0logs\monitor_retornos.log' -Tail 20 | Where-Object {$_ -match 'ALERTA|inacessível|Servidor'}"

echo.
echo ───────────────────────────────────────────────────────────────
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 6: Instruções para Reconectar Servidor
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Agora RECONECTE o servidor (desfaça a ação do Passo 3):
echo.
echo  • Se desconectou unidade: reconecte
echo  • Se renomeou pasta: volte ao nome original
echo  • Se desligou servidor: ligue novamente
echo.
echo ───────────────────────────────────────────────────────────────
echo.
echo  Pressione qualquer tecla DEPOIS de reconectar...
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 7: Aguardando Recuperação (6 minutos)...
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ⏰ Aguardando 6 minutos para monitor detectar recuperação...
echo.

timeout /t 360 /nobreak

echo.
echo ───────────────────────────────────────────────────────────────
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  PASSO 8: Verificar Recuperação
echo ═══════════════════════════════════════════════════════════════
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Write-Host '🔍 Últimas 30 linhas do log:' -ForegroundColor Cyan; ^
Get-Content '%~dp0logs\monitor_retornos.log' -Tail 30"

echo.
echo ───────────────────────────────────────────────────────────────
echo.
echo  O que você deve ver no log:
echo    ⚠️  "ALERTA: Servidor ficou inacessível"
echo    ✅ "SERVIDOR RECUPERADO"
echo    📁 "Processando arquivos pendentes"
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo  RESULTADO DO TESTE
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ SUCESSO se:
echo     • Log mostra detecção da queda
echo     • Log mostra recuperação automática
echo     • Arquivos adicionados durante queda foram processados
echo     • Recebeu emails de alerta e recuperação
echo.
echo  ❌ FALHA se:
echo     • Log não mostra detecção da queda
echo     • Sistema travou e não recuperou
echo     • Arquivos não foram processados
echo     • Não recebeu emails
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
