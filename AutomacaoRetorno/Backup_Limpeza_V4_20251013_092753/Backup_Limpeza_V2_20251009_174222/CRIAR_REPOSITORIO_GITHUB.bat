@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  CRIAR REPOSITÓRIO NO GITHUB                                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se GitHub CLI está instalado
where gh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ GitHub CLI não encontrado!
    echo.
    echo 📥 Instalando GitHub CLI...
    winget install --id GitHub.cli --accept-source-agreements --accept-package-agreements
    echo.
    echo ✅ GitHub CLI instalado! Feche e reabra este terminal.
    pause
    exit /b
)

echo ✅ GitHub CLI encontrado
echo.

REM Verificar se já está logado
gh auth status >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🔐 Você precisa fazer login no GitHub primeiro...
    echo.
    echo Siga as instruções abaixo:
    echo   1. Escolha: GitHub.com
    echo   2. Escolha: HTTPS
    echo   3. Escolha: Login with a web browser
    echo   4. Copie o código que aparecer
    echo   5. Pressione Enter e cole o código no navegador
    echo.
    pause
    gh auth login
    echo.
)

echo.
echo ✅ Autenticado no GitHub!
echo.

REM Obter informações do usuário
for /f "tokens=*" %%i in ('gh api user -q .login') do set GITHUB_USER=%%i
echo 👤 Usuário: %GITHUB_USER%
echo.

REM Perguntar nome do repositório
set /p REPO_NAME="📝 Nome do repositório (automacao-retorno-cbr724): "
if "%REPO_NAME%"=="" set REPO_NAME=automacao-retorno-cbr724

REM Perguntar descrição
set /p REPO_DESC="📄 Descrição (Sistema automático de processamento de retornos bancários CBR724): "
if "%REPO_DESC%"=="" set REPO_DESC=Sistema automático de processamento de retornos bancários CBR724

REM Perguntar se é privado
echo.
echo 🔒 Visibilidade:
echo   [1] Private (Recomendado - dados financeiros sensíveis)
echo   [2] Public (Código aberto para qualquer pessoa)
echo.
set /p VISIBILITY="Escolha (1 ou 2): "

if "%VISIBILITY%"=="2" (
    set VIS_FLAG=--public
    echo.
    echo ⚠️  ATENÇÃO: Repositório será PÚBLICO!
    echo    Certifique-se de que não há dados sensíveis no código!
    echo.
    pause
) else (
    set VIS_FLAG=--private
    echo.
    echo ✅ Repositório será PRIVADO
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 🚀 Criando repositório no GitHub...
echo    Nome: %REPO_NAME%
echo    Descrição: %REPO_DESC%
echo    Visibilidade: %VIS_FLAG%
echo.

REM Criar repositório
gh repo create %REPO_NAME% %VIS_FLAG% --description "%REPO_DESC%" --source=. --remote=origin

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Repositório criado com sucesso!
    echo.
    echo 📤 Enviando código para o GitHub...
    
    REM Renomear branch para main
    git branch -M main
    
    REM Push para o GitHub
    git push -u origin main
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ╔════════════════════════════════════════════════════════════════╗
        echo ║  🎉 SUCESSO! PROJETO NO GITHUB!                                ║
        echo ╚════════════════════════════════════════════════════════════════╝
        echo.
        echo 🌐 Ver no navegador:
        echo    https://github.com/%GITHUB_USER%/%REPO_NAME%
        echo.
        
        REM Abrir no navegador
        set /p OPEN_BROWSER="Abrir repositório no navegador? (S/N): "
        if /i "%OPEN_BROWSER%"=="S" (
            start https://github.com/%GITHUB_USER%/%REPO_NAME%
        )
    ) else (
        echo.
        echo ❌ Erro ao enviar código para o GitHub
        echo    Tente novamente: git push -u origin main
    )
) else (
    echo.
    echo ❌ Erro ao criar repositório
    echo    Verifique se o nome já existe ou se há problemas de autenticação
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
