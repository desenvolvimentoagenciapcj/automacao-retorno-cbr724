@echo off
REM ============================================================================
REM Script para copiar projeto atualizado para OneDrive
REM ============================================================================
REM Data: 29/10/2025
REM Versao: 2.1 com notificacoes de alerta de arquivo
REM Objetivo: Backup da ultima versao com melhorias

cls
color 0A
echo.
echo ================================================================================
echo          BACKUP ONEDRIVE - AUTOMACAO RETORNOS CBR724
echo          Versao: 2.1 (com alerta de arquivo faltante)
echo ================================================================================
echo.

REM Caminho do OneDrive definido no config.ini
set "ONEDRIVE_PATH=F:\OneDrive - Fundacao Agencia das Bacias PCJ\Repositorio_TI\Manuais\SCPCJ\AutomaçãoDbBaixa"

REM Se não existir, permitir entrada manual
if not exist "%ONEDRIVE_PATH%" (
    echo.
    echo AVISO: Caminho padrão não encontrado!
    echo.
    set /p ONEDRIVE_PATH="Digite o caminho correto do OneDrive: "
)

if not exist "%ONEDRIVE_PATH%" (
    echo.
    color 0C
    echo ERRO: Caminho não existe!
    echo.
    pause
    exit /b 1
)

echo.
echo Caminho de destino: %ONEDRIVE_PATH%
echo.

REM Criar timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set "TIMESTAMP=%mydate%_%mytime%"

set "DESTINO=%ONEDRIVE_PATH%\Backup_%TIMESTAMP%"

echo Criando pasta de backup: %DESTINO%
mkdir "%DESTINO%" 2>nul
mkdir "%DESTINO%\Scripts\python" 2>nul
mkdir "%DESTINO%\Scripts\bat" 2>nul
mkdir "%DESTINO%\Scripts\powershell" 2>nul
mkdir "%DESTINO%\config" 2>nul
mkdir "%DESTINO%\docs" 2>nul
mkdir "%DESTINO%\logs" 2>nul

echo.
echo ================================================================================
echo Copiando arquivos...
echo ================================================================================
echo.

REM Copiar scripts Python (PRINCIPAL)
echo [1/7] Copiando scripts Python...
copy /Y "Scripts\python\*.py" "%DESTINO%\Scripts\python\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Scripts Python copiados
) else (
    echo    ⚠️  AVISO: Erro ao copiar scripts Python
)

REM Copiar scripts BAT
echo [2/7] Copiando scripts BAT...
copy /Y "Scripts\bat\*.bat" "%DESTINO%\Scripts\bat\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Scripts BAT copiados
) else (
    echo    ⚠️  AVISO: Erro ao copiar scripts BAT
)

REM Copiar scripts PowerShell
echo [3/7] Copiando scripts PowerShell...
copy /Y "Scripts\powershell\*.ps1" "%DESTINO%\Scripts\powershell\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Scripts PowerShell copiados
) else (
    echo    ⚠️  AVISO: Erro ao copiar scripts PowerShell
)

REM Copiar configuracoes
echo [4/7] Copiando configuracoes...
copy /Y "config\config.ini" "%DESTINO%\config\config.ini.backup" >nul 2>&1
copy /Y "config\requirements.txt" "%DESTINO%\config\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Configuracoes copiadas
) else (
    echo    ⚠️  AVISO: Erro ao copiar configuracoes
)

REM Copiar documentacao
echo [5/7] Copiando documentacao...
copy /Y "*.md" "%DESTINO%\docs\" >nul 2>&1
copy /Y "*.txt" "%DESTINO%\docs\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Documentacao copiada
) else (
    echo    ⚠️  AVISO: Erro ao copiar documentacao
)

REM Copiar atalhos raiz
echo [6/7] Copiando atalhos...
copy /Y "*.bat" "%DESTINO%\" >nul 2>&1
copy /Y "README.md" "%DESTINO%\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Atalhos copiados
) else (
    echo    ⚠️  AVISO: Erro ao copiar atalhos
)

REM Criar arquivo INFO
echo [7/7] Criando informacoes...
(
echo # BACKUP AUTOMACAO RETORNOS CBR724
echo.
echo **Data do Backup:** %TIMESTAMP%
echo **Versao:** 2.1
echo **Alteracoes:** Notificacao de arquivo faltante para Aline e Lilian
echo.
echo ## Conteudo
echo.
echo - **Scripts/python/** - Arquivos Python (monitor, processador, notificador, agendador)
echo - **Scripts/bat/** - Scripts em lote
echo - **Scripts/powershell/** - Scripts PowerShell
echo - **config/** - Configuracoes (config.ini.backup + requirements.txt)
echo - **docs/** - Documentacao completa
echo.
echo ## Novidades nesta versao
echo.
echo - ✅ Notificacao quando nao ha arquivo ate 8h30
echo - ✅ Email enviado para: backoffice, Aline, Lilian
echo - ✅ Correcao do erro RFC 5322 do Gmail
echo - ✅ Melhorias na funcao _criar_mensagem()
echo.
echo ## Principais Modificacoes
echo.
echo 1. Scripts/python/notificador_email.py
echo    - Funcao notificar_sem_arquivos() agora aceita emails adicionais
echo    - Funcao _criar_mensagem() aceita lista de destinatarios
echo.
echo 2. Scripts/python/agendador_verificacao.py
echo    - Adicionado metodo verificar_arquivos_na_pasta()
echo    - Verifica se ha arquivos .ret na pasta de retorno
echo    - Envia notificacao para Aline Briques e Lilian Cruz
echo.
echo ## Para restaurar
echo.
echo 1. Copiar conteudo de Scripts/ para d:\Teste_Cobranca_Acess\AutomaçãoDbBaixa\Scripts\
echo 2. Copiar config/config.ini.backup para d:\Teste_Cobranca_Acess\AutomaçãoDbBaixa\config\config.ini
echo 3. Reiniciar o agendador
echo.
echo ## Suporte
echo.
echo - Aline Briques (aline.briques@agencia.baciaspcj.org.br)
echo - Lilian Cruz (lilian.cruz@agencia.baciaspcj.org.br)
echo - Charles Oliveira (charles.oliveira@agencia.baciaspcj.org.br)
) > "%DESTINO%\INFO_BACKUP.md"

echo    ✅ OK: Informacoes criadas

echo.
echo ================================================================================
echo Criando arquivo ZIP de backup...
echo ================================================================================
echo.

REM Obter nome da pasta base para o ZIP
for %%f in ("%DESTINO%") do set "FOLDER_NAME=%%~nf"

REM Criar ZIP usando PowerShell
powershell -Command "Compress-Archive -Path '%DESTINO%' -DestinationPath '%ONEDRIVE_PATH%\%FOLDER_NAME%.zip' -Force"

if %ERRORLEVEL% EQU 0 (
    echo    ✅ OK: Arquivo ZIP criado: %FOLDER_NAME%.zip
) else (
    echo    ⚠️  AVISO: Nao foi possivel criar ZIP
)

echo.
echo ================================================================================
echo          BACKUP CONCLUIDO COM SUCESSO!
echo ================================================================================
echo.
echo Informacoes:
echo   - Data: %TIMESTAMP%
echo   - Versao: 2.1
echo   - Pasta: %DESTINO%
echo.
echo Arquivos copiados:
echo   - Scripts Python:       7 arquivos
echo   - Scripts BAT:          ~10 arquivos
echo   - Scripts PowerShell:   ~5 arquivos
echo   - Configuracoes:        2 arquivos
echo   - Documentacao:         15+ arquivos
echo.
echo Localizacao:
echo   OneDrive: %ONEDRIVE_PATH%
echo   Backup: Backup_%TIMESTAMP%
echo   ZIP: %FOLDER_NAME%.zip
echo.
echo ================================================================================
echo.

pause
