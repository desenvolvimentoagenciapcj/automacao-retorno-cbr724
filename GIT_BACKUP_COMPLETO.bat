@echo off
REM ============================================================================
REM Script para inicializar Git e fazer backup/commit
REM ============================================================================
REM Data: 29/10/2025
REM Objetivo: Versionar projeto com Git + fazer backup OneDrive

cls
color 0A
echo.
echo ================================================================================
echo          GIT INIT E BACKUP - AUTOMACAO RETORNOS CBR724
echo          Versao: 2.1
echo ================================================================================
echo.

REM Verificar se já existe repositório Git
cd /d "%~dp0"

if exist ".git" (
    echo ✅ Repositorio Git ja existe
    echo.
    git status
    echo.
    echo Deseja fazer commit das alteracoes? (S/N)
    set /p RESP="Resposta: "
    
    if /i "%RESP%"=="S" (
        goto FAZER_COMMIT
    ) else (
        echo Cancelado.
        pause
        exit /b 0
    )
) else (
    echo ⚠️  Repositorio Git NAO encontrado
    echo.
    echo Deseja inicializar Git agora? (S/N)
    set /p RESP="Resposta: "
    
    if /i "%RESP%"=="N" (
        echo Cancelado.
        pause
        exit /b 0
    )
    
    goto INICIALIZAR_GIT
)

REM ============================================================================
:INICIALIZAR_GIT
REM ============================================================================

echo.
echo ================================================================================
echo Inicializando repositorio Git...
echo ================================================================================
echo.

git init
git config user.name "Charles Oliveira"
git config user.email "charles.oliveira@agencia.baciaspcj.org.br"

echo.
echo Digite a URL do repositorio remoto (ex: https://github.com/usuario/repo.git)
echo Deixe em branco se nao tiver:
set /p GIT_URL="URL: "

if not "%GIT_URL%"=="" (
    echo.
    echo Adicionando repositorio remoto...
    git remote add origin "%GIT_URL%"
    echo ✅ Remoto adicionado: %GIT_URL%
)

echo.
echo Criando .gitignore...

REM Criar arquivo .gitignore
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Ambiente
echo .env
echo .venv
echo env/
echo venv/
echo ENV/
echo env.bak/
echo venv.bak/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Projeto
echo logs/
echo *.log
echo Backup_*/
echo config/config.ini
) > .gitignore

echo ✅ .gitignore criado

:FAZER_COMMIT

echo.
echo ================================================================================
echo Adicionando arquivos...
echo ================================================================================
echo.

git add .

echo.
echo ================================================================================
echo Status do Git
echo ================================================================================
echo.

git status

echo.
echo Digite a mensagem do commit (ex: "v2.1: Notificacao arquivo faltante")
set /p COMMIT_MSG="Mensagem: "

if "%COMMIT_MSG%"=="" (
    set "COMMIT_MSG=v2.1: Notificacao arquivo faltante para Aline e Lilian"
)

echo.
echo Fazendo commit: %COMMIT_MSG%
echo.

git commit -m "%COMMIT_MSG%"

if %ERRORLEVEL% EQU 0 (
    echo.
    color 0B
    echo ================================================================================
    echo          ✅ COMMIT REALIZADO COM SUCESSO!
    echo ================================================================================
    echo.
    
    git log --oneline -5
    
    echo.
    echo Deseja fazer push para o repositorio remoto? (S/N)
    set /p PUSH_RESP="Resposta: "
    
    if /i "%PUSH_RESP%"=="S" (
        echo.
        echo Fazendo push...
        git push -u origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo ✅ Push realizado com sucesso!
        ) else (
            echo ⚠️  Erro ao fazer push. Verifique a URL do repositorio.
        )
    )
    
) else (
    color 0C
    echo.
    echo ❌ Erro ao fazer commit
    echo.
)

echo.
echo ================================================================================
echo Agora fazendo backup no OneDrive...
echo ================================================================================
echo.

REM Executar script de backup OneDrive
if exist "BACKUP_ONEDRIVE.bat" (
    call BACKUP_ONEDRIVE.bat
) else (
    echo ⚠️  Script BACKUP_ONEDRIVE.bat nao encontrado
)

echo.
echo ================================================================================
echo          PROCESSO CONCLUIDO!
echo ================================================================================
echo.
echo Resumo:
echo   - Repositorio Git: INICIALIZADO/ATUALIZADO
echo   - Commits: ENVIADOS
echo   - Backup OneDrive: REALIZADO
echo.
echo Status final:
echo.

git status

echo.
pause
