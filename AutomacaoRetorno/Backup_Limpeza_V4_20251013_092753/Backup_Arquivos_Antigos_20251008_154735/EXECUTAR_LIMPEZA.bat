@echo off
chcp 65001 > nul
color 0E
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🧹 LIMPEZA SEGURA - MODO BACKUP                         ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📦 Criando pasta de backup...
echo.

REM Criar pasta de backup com timestamp
set TIMESTAMP=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_DIR=Backup_Arquivos_Antigos_%TIMESTAMP%

mkdir "%BACKUP_DIR%" 2>nul

echo ✅ Pasta criada: %BACKUP_DIR%
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📋 Movendo arquivos de teste e desenvolvimento...
echo.

REM Arquivos de teste
if exist "analise_manual_cbr724.py" (
    move "analise_manual_cbr724.py" "%BACKUP_DIR%\" >nul
    echo    ✓ analise_manual_cbr724.py
)
if exist "checar_datas.py" (
    move "checar_datas.py" "%BACKUP_DIR%\" >nul
    echo    ✓ checar_datas.py
)
if exist "teste_data_arquivo.py" (
    move "teste_data_arquivo.py" "%BACKUP_DIR%\" >nul
    echo    ✓ teste_data_arquivo.py
)
if exist "verificar_datas_banco.py" (
    move "verificar_datas_banco.py" "%BACKUP_DIR%\" >nul
    echo    ✓ verificar_datas_banco.py
)
if exist "verificar_sistema.py" (
    move "verificar_sistema.py" "%BACKUP_DIR%\" >nul
    echo    ✓ verificar_sistema.py
)
if exist "monitor_arquivos.py" (
    move "monitor_arquivos.py" "%BACKUP_DIR%\" >nul
    echo    ✓ monitor_arquivos.py
)
if exist "monitor_arquivos_simples.py" (
    move "monitor_arquivos_simples.py" "%BACKUP_DIR%\" >nul
    echo    ✓ monitor_arquivos_simples.py
)

echo.
echo 📋 Movendo arquivos duplicados/backup...
echo.

if exist "integrador_access.py.backup" (
    move "integrador_access.py.backup" "%BACKUP_DIR%\" >nul
    echo    ✓ integrador_access.py.backup
)
if exist "integrador_vba_logic.py" (
    move "integrador_vba_logic.py" "%BACKUP_DIR%\" >nul
    echo    ✓ integrador_vba_logic.py
)

echo.
echo 📋 Movendo processadores não utilizados...
echo.

if exist "processador_cnab.py" (
    move "processador_cnab.py" "%BACKUP_DIR%\" >nul
    echo    ✓ processador_cnab.py
)
if exist "processar_todos_arquivos.py" (
    move "processar_todos_arquivos.py" "%BACKUP_DIR%\" >nul
    echo    ✓ processar_todos_arquivos.py
)

echo.
echo 📋 Movendo documentação redundante...
echo.

if exist "COMO_USAR.md" (
    move "COMO_USAR.md" "%BACKUP_DIR%\" >nul
    echo    ✓ COMO_USAR.md
)
if exist "README.md" (
    move "README.md" "%BACKUP_DIR%\" >nul
    echo    ✓ README.md
)
if exist "README_SISTEMA.md" (
    move "README_SISTEMA.md" "%BACKUP_DIR%\" >nul
    echo    ✓ README_SISTEMA.md
)
if exist "LIMPEZA_PRODUCAO.md" (
    move "LIMPEZA_PRODUCAO.md" "%BACKUP_DIR%\" >nul
    echo    ✓ LIMPEZA_PRODUCAO.md
)

echo.
echo 📋 Movendo configuração não usada...
echo.

if exist "config.yaml" (
    move "config.yaml" "%BACKUP_DIR%\" >nul
    echo    ✓ config.yaml
)

echo.
echo 📋 Movendo arquivos de serviço Windows (opcional)...
echo.

if exist "servico_monitor.py" (
    move "servico_monitor.py" "%BACKUP_DIR%\" >nul
    echo    ✓ servico_monitor.py
)
if exist "INSTALAR_SERVICO.bat" (
    move "INSTALAR_SERVICO.bat" "%BACKUP_DIR%\" >nul
    echo    ✓ INSTALAR_SERVICO.bat
)
if exist "CRIAR_ATALHO.bat" (
    move "CRIAR_ATALHO.bat" "%BACKUP_DIR%\" >nul
    echo    ✓ CRIAR_ATALHO.bat
)

echo.
echo 📋 Movendo documentação de limpeza...
echo.

if exist "PLANO_LIMPEZA.md" (
    move "PLANO_LIMPEZA.md" "%BACKUP_DIR%\" >nul
    echo    ✓ PLANO_LIMPEZA.md
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✅ LIMPEZA CONCLUÍDA COM SUCESSO!
echo.
echo 📂 Arquivos antigos salvos em: %BACKUP_DIR%
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📁 ARQUIVOS ESSENCIAIS MANTIDOS:
echo.
echo    ✓ processador_cbr724.py        (Processa CBR724)
echo    ✓ integrador_access.py         (Integra com Access)
echo    ✓ monitor_retornos.py          (Monitor automático)
echo    ✓ INICIAR_MONITOR.bat          (Inicia o sistema)
echo    ✓ GUIA_RAPIDO.txt              (Como usar)
echo    ✓ requirements.txt             (Dependências)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🎉 Projeto agora está ENXUTO e ORGANIZADO!
echo.
echo 💡 DICA: Se precisar recuperar algum arquivo, basta copiar
echo          de volta da pasta de backup.
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
