"""
Instala o Monitor de Retornos como um Serviço do Windows
Executa automaticamente ao iniciar o sistema
"""
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
from pathlib import Path

# Configurar path
sys.path.append(str(Path(__file__).parent))

from monitor_retornos import ProcessadorRetornoHandler
from watchdog.observers import Observer

class MonitorRetornosService(win32serviceutil.ServiceFramework):
    """Serviço Windows para monitoramento automático de retornos"""
    
    _svc_name_ = "MonitorRetornosBancarios"
    _svc_display_name_ = "Monitor de Retornos Bancários - CBR724"
    _svc_description_ = "Processa automaticamente arquivos de retorno bancário CBR724"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.observer = None
        
        # Configurar logging para o serviço
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    r'D:\Teste_Cobrança_Acess\AutomacaoRetorno\servico_monitor.log',
                    encoding='utf-8'
                )
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def SvcStop(self):
        """Para o serviço"""
        self.logger.info("Parando serviço de monitoramento...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.observer:
            self.observer.stop()
    
    def SvcDoRun(self):
        """Executa o serviço"""
        self.logger.info("Iniciando serviço de monitoramento...")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()
    
    def main(self):
        """Loop principal do serviço"""
        try:
            # Configurar pastas
            pasta_entrada = Path(r"D:\Teste_Cobrança_Acess\Retorno")
            pasta_processados = pasta_entrada / "Processados"
            pasta_erro = pasta_entrada / "Erro"
            
            # Criar o manipulador de eventos
            event_handler = ProcessadorRetornoHandler(
                pasta_entrada=pasta_entrada,
                pasta_processados=pasta_processados,
                pasta_erro=pasta_erro
            )
            
            # Criar o observador
            self.observer = Observer()
            self.observer.schedule(event_handler, str(pasta_entrada), recursive=False)
            self.observer.start()
            
            self.logger.info("Serviço iniciado com sucesso. Monitorando arquivos...")
            
            # Loop principal
            while True:
                # Esperar pelo evento de parada (timeout de 1 segundo)
                rc = win32event.WaitForSingleObject(self.stop_event, 1000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
            
            self.observer.stop()
            self.observer.join()
            self.logger.info("Serviço parado com sucesso")
        
        except Exception as e:
            self.logger.error(f"Erro no serviço: {e}", exc_info=True)
            servicemanager.LogErrorMsg(f"Erro no serviço: {e}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonitorRetornosService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonitorRetornosService)
