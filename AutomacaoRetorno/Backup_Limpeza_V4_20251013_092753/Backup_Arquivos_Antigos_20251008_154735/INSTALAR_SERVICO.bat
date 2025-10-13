@echo off
REM ============================================================================
REM Instalar Serviço do Windows - Monitor de Retornos
REM Execute como ADMINISTRADOR
REM ============================================================================

title Instalação do Serviço de Monitoramento
color 0E

echo.
echo ================================================================================
echo         INSTALAÇÃO DO SERVIÇO - MONITOR DE RETORNOS BANCÁRIOS
echo ================================================================================
echo.
echo   ATENÇÃO: Este script deve ser executado como ADMINISTRADOR
echo.
echo   O serviço será instalado e configurado para:
echo   - Iniciar automaticamente com o Windows
echo   - Monitorar continuamente a pasta de retornos
echo   - Processar arquivos CBR724 automaticamente
echo.
echo ================================================================================
echo.

cd /d "D:\Teste_Cobrança_Acess\AutomacaoRetorno"

echo Instalando dependências...
pip install pywin32
echo.

echo Instalando serviço...
python servico_monitor.py install
echo.

echo Configurando inicialização automática...
sc config MonitorRetornosBancarios start= auto
echo.

echo.
echo ================================================================================
echo   INSTALAÇÃO CONCLUÍDA!
echo ================================================================================
echo.
echo   Para INICIAR o serviço agora:
echo   python servico_monitor.py start
echo.
echo   Para PARAR o serviço:
echo   python servico_monitor.py stop
echo.
echo   Para REMOVER o serviço:
echo   python servico_monitor.py remove
echo.
echo   O serviço iniciará automaticamente no próximo boot do Windows.
echo ================================================================================
echo.

pause
