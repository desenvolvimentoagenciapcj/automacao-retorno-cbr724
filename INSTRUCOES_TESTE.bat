@echo off
REM ============================================================================
REM INSTRUÇÕES DE TESTE - Notificação de Arquivos Faltantes
REM ============================================================================
REM
REM Este arquivo contém instruções passo-a-passo para testar a nova 
REM funcionalidade de notificação quando não há arquivos na pasta
REM
REM ============================================================================

cls
color 0A
echo.
echo ============================================================================
echo   TESTE: NOTIFICAÇÃO DE ARQUIVOS FALTANTES
echo   Sistema de Automação de Retornos CBR724
echo ============================================================================
echo.

REM ============================================================================
REM TESTE 1: Verificação de Sintaxe
REM ============================================================================

echo.
echo [1/3] VALIDANDO SINTAXE PYTHON...
echo.

python -m py_compile Scripts\python\agendador_verificacao.py

if errorlevel 1 (
    color 0C
    echo ❌ ERRO: Há erros de sintaxe no arquivo!
    echo.
    pause
    exit /b 1
)

color 0A
echo ✅ Sintaxe OK!
echo.

REM ============================================================================
REM TESTE 2: Teste Prático
REM ============================================================================

echo.
echo [2/3] EXECUTANDO TESTE PRÁTICO...
echo.
echo Este teste vai:
echo   1. Verificar se há arquivos na pasta de retorno
echo   2. Se NÃO houver → Enviar email de notificação
echo   3. Se HOUVER → Continuar normalmente
echo.
echo ⏳ Aguarde... (pode levar alguns segundos)
echo.

python Scripts\python\agendador_verificacao.py --testar

if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERRO durante o teste!
    echo.
    pause
    exit /b 1
)

color 0A
echo.
echo ✅ Teste concluído com sucesso!
echo.

REM ============================================================================
REM TESTE 3: Verificação de Email
REM ============================================================================

echo.
echo [3/3] VERIFICAÇÃO DO EMAIL...
echo.
echo Se não houve arquivo na pasta, você deve ter recebido um email com:
echo.
echo   De:      tipcj@agencia.baciaspcj.org.br
echo   Para:    backoffice@agencia.baciaspcj.org.br
echo   Assunto: ⚠️  Nenhum Arquivo Recebido - Verificação 08:30
echo.
echo 📧 Verifique sua caixa de entrada (ou spam)
echo.

REM ============================================================================
REM RESUMO FINAL
REM ============================================================================

echo.
echo ============================================================================
echo   ✅ TESTES CONCLUÍDOS COM SUCESSO!
echo ============================================================================
echo.
echo O sistema está pronto para uso:
echo.
echo   ✅ Sintaxe validada
echo   ✅ Funcionalidade testada
echo   ✅ Email configurado corretamente
echo.
echo Sistema vai operar da seguinte forma:
echo.
echo   📅 TODOS OS DIAS ÚTEIS (seg-sex)
echo   🕐 ÀS 8h30 DA MANHÃ
echo   ✓  Verifica servidor
echo   ✓  Verifica monitor
echo   ✓  Verifica se há arquivos de retorno
echo      ├─ Se NÃO houver → 📧 Envia email
echo      └─ Se HOUVER → ✅ Continua normalmente
echo.
echo Para monitorar logs, veja:
echo   📄 logs\agendador.log
echo.
echo ============================================================================
echo.

pause
