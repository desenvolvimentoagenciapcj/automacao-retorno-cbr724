@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  TESTE AUTOMÁTICO DO MONITOR                                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Este script irá testar as 3 correções:
echo   ✓ Backup antes do processamento
echo   ✓ Exclusão de arquivos IEDCBR
echo   ✓ Sufixo "-processado" nos arquivos
echo.

REM Aguardar 5 segundos para dar tempo de iniciar o monitor
echo ⏳ Aguardando 5 segundos para você iniciar o monitor...
timeout /t 5 /nobreak > nul
echo.

echo 📝 CRIANDO ARQUIVO IEDCBR DE TESTE...
echo IEDCBR arquivo de instrução > "..\Retorno\IEDCBR_TESTE_AUTO.ret"
echo    ✓ IEDCBR_TESTE_AUTO.ret criado
echo.
timeout /t 2 > nul

echo 📝 CRIANDO ARQUIVO CBR DE TESTE...
(
    echo 000000CBR7246260810202521206
    echo 28TESTE                                                                                                08102025
) > "..\Retorno\CBR_TESTE_AUTO.ret"
echo    ✓ CBR_TESTE_AUTO.ret criado
echo.

echo ⏳ Aguardando 10 segundos para o monitor processar...
timeout /t 10 /nobreak > nul
echo.

echo ═══════════════════════════════════════════════════════════════════
echo   VERIFICANDO RESULTADOS:
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Verificar se IEDCBR foi excluído
if exist "..\Retorno\IEDCBR_TESTE_AUTO.ret" (
    echo ❌ ERRO: IEDCBR_TESTE_AUTO.ret NÃO foi excluído
) else (
    echo ✅ SUCESSO: IEDCBR_TESTE_AUTO.ret foi excluído corretamente
)
echo.

REM Verificar se CBR foi processado
if exist "..\Retorno\Processados\CBR_TESTE_AUTO-processado.ret" (
    echo ✅ SUCESSO: CBR_TESTE_AUTO-processado.ret existe em Processados/
) else (
    echo ❌ ERRO: Arquivo processado não foi encontrado
)
echo.

REM Verificar backup mais recente
echo 🔍 Verificando backups criados nos últimos 2 minutos...
powershell -Command "$backups = Get-ChildItem '..\Backup\backup_*dbBaixa2025.accdb' | Where-Object {$_.LastWriteTime -gt (Get-Date).AddMinutes(-2)} | Sort-Object LastWriteTime -Descending; if ($backups) { Write-Host '✅ SUCESSO: Backup criado -' $backups[0].Name -ForegroundColor Green } else { Write-Host '❌ ERRO: Nenhum backup recente encontrado' -ForegroundColor Red }"
echo.

echo ═══════════════════════════════════════════════════════════════════
echo   TESTE CONCLUÍDO!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Pressione qualquer tecla para sair...
pause > nul
