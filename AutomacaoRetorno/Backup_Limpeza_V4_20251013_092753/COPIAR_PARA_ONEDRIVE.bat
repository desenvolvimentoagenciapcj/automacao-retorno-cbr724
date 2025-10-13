@echo off
REM ============================================================================
REM Script para copiar projeto para OneDrive/Manuais
REM ============================================================================

cls
echo.
echo ================================================================================
echo          COPIAR PROJETO PARA ONEDRIVE - MANUAIS
echo ================================================================================
echo.

REM Solicitar caminho do OneDrive
set /p ONEDRIVE_PATH="Digite o caminho da pasta Manuais no OneDrive: "

REM Se não informado, usar padrão
if "%ONEDRIVE_PATH%"=="" (
    set "ONEDRIVE_PATH=%USERPROFILE%\OneDrive\Manuais"
)

echo.
echo Caminho de destino: %ONEDRIVE_PATH%
echo.

REM Criar pasta de destino
set "DESTINO=%ONEDRIVE_PATH%\AutomacaoRetorno-CBR724"
echo Criando pasta: %DESTINO%
mkdir "%DESTINO%" 2>nul
mkdir "%DESTINO%\Codigo" 2>nul
mkdir "%DESTINO%\Scripts" 2>nul
mkdir "%DESTINO%\Documentacao" 2>nul
mkdir "%DESTINO%\Config" 2>nul

echo.
echo ================================================================================
echo Copiando arquivos...
echo ================================================================================
echo.

REM Copiar documentação
echo [1/5] Copiando documentacao...
copy /Y "MANUAL_IMPLANTACAO_COMPLETO.md" "%DESTINO%\Documentacao\" >nul
copy /Y "GUIA_CONFIG.md" "%DESTINO%\Documentacao\" >nul
copy /Y "NOTIFICACOES_WINDOWS.md" "%DESTINO%\Documentacao\" >nul
copy /Y "SISTEMA_WATCHDOG.md" "%DESTINO%\Documentacao\" >nul
copy /Y "CHANGELOG.md" "%DESTINO%\Documentacao\" >nul
copy /Y "README.md" "%DESTINO%\Documentacao\" 2>nul
echo    OK: Documentacao copiada

REM Copiar código Python
echo [2/5] Copiando codigo Python...
copy /Y "*.py" "%DESTINO%\Codigo\" >nul
echo    OK: Codigo Python copiado

REM Copiar scripts BAT e PS1
echo [3/5] Copiando scripts...
copy /Y "*.bat" "%DESTINO%\Scripts\" >nul
copy /Y "*.ps1" "%DESTINO%\Scripts\" >nul
copy /Y "*.vbs" "%DESTINO%\Scripts\" 2>nul
echo    OK: Scripts copiados

REM Copiar configurações
echo [4/5] Copiando configuracoes...
copy /Y "config.ini" "%DESTINO%\Config\config.ini.exemplo" >nul
copy /Y "requirements.txt" "%DESTINO%\Config\" >nul
echo    OK: Configuracoes copiadas

REM Criar README no OneDrive
echo [5/5] Criando README...
(
echo # Sistema de Automacao de Retornos CBR724
echo.
echo **Organizacao:** Agencia PCJ
echo **Data:** %DATE%
echo **Versao:** 1.0
echo.
echo ## Conteudo desta Pasta
echo.
echo - **Documentacao/** - Manuais e guias completos
echo - **Codigo/** - Arquivos Python do sistema
echo - **Scripts/** - Scripts BAT e PowerShell
echo - **Config/** - Arquivos de configuracao
echo.
echo ## Inicio Rapido
echo.
echo 1. Leia `Documentacao/MANUAL_IMPLANTACAO_COMPLETO.md`
echo 2. Siga o passo a passo de instalacao
echo 3. Configure o `config.ini`
echo.
echo ## Arquivos Importantes
echo.
echo - **MANUAL_IMPLANTACAO_COMPLETO.md** - Guia completo de implantacao
echo - **GUIA_CONFIG.md** - Explicacao das configuracoes
echo - **NOTIFICACOES_WINDOWS.md** - Sistema de notificacoes
echo - **SISTEMA_WATCHDOG.md** - Auto-restart do monitor
echo.
echo ## Suporte
echo.
echo - Charles Oliveira
echo - charles.oliveira@agencia.baciaspcj.org.br
) > "%DESTINO%\README.txt"
echo    OK: README criado

echo.
echo ================================================================================
echo Criando arquivo ZIP de backup...
echo ================================================================================
echo.

REM Criar ZIP usando PowerShell
powershell -Command "Compress-Archive -Path '%DESTINO%\*' -DestinationPath '%DESTINO%\..\AutomacaoRetorno-CBR724-Backup.zip' -Force"

if %ERRORLEVEL% EQU 0 (
    echo    OK: Backup ZIP criado
) else (
    echo    AVISO: Nao foi possivel criar ZIP
)

echo.
echo ================================================================================
echo          COPIA CONCLUIDA COM SUCESSO!
echo ================================================================================
echo.
echo Destino: %DESTINO%
echo.
echo Estrutura criada:
echo   - Documentacao/  (5 arquivos MD)
echo   - Codigo/        (7 arquivos PY)
echo   - Scripts/       (arquivos BAT e PS1)
echo   - Config/        (config.ini.exemplo + requirements.txt)
echo   - README.txt
echo.
echo Backup ZIP: %ONEDRIVE_PATH%\AutomacaoRetorno-CBR724-Backup.zip
echo.
echo ================================================================================
echo.

pause
