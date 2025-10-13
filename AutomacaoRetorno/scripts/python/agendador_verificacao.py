"""
Agendador de Verificação do Monitor
====================================

Verifica se o monitor está rodando em horários programados.
Por padrão: Segunda a Sexta às 8h da manhã.

Se o monitor não estiver rodando, inicia automaticamente.

Funcionalidades:
- Verificação agendada (configurável)
- Detecção de processo Python monitor_retornos.py
- Reinício automático se caído
- Notificações Windows e E-mail
- Logs detalhados

Configuração:
- Configure horários no config.ini seção [VERIFICACAO_AGENDADA]

Autor: Sistema de Automação CBR724
Data: 13/10/2025
"""

import os
import sys
import time
import logging
import psutil
import schedule
import subprocess
from datetime import datetime
from pathlib import Path

# Adiciona o diretório do projeto ao path
script_dir = Path(__file__).parent
projeto_dir = script_dir.parent.parent
sys.path.insert(0, str(projeto_dir / 'scripts' / 'python'))

from config_manager import Config
from notificador_windows import NotificadorWindows
from notificador_email import NotificadorEmail

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(projeto_dir / 'logs' / 'agendador.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AgendadorVerificacao:
    """Agendador que verifica se o monitor está ativo"""
    
    def __init__(self):
        """Inicializa o agendador"""
        self.config = Config()
        self.notificador_windows = NotificadorWindows()
        self.notificador_email = NotificadorEmail()
        self.projeto_dir = projeto_dir
        
        # Configurações do agendamento
        self.habilitado = self._get_config_bool('VERIFICACAO_AGENDADA', 'habilitado', True)
        self.horario = self.config.config.get('VERIFICACAO_AGENDADA', 'horario', fallback='08:00')
        self.dias_semana = self._get_dias_semana()
        
        logger.info("="*80)
        logger.info("📅 AGENDADOR DE VERIFICAÇÃO INICIADO")
        logger.info("="*80)
        logger.info(f"⏰ Horário: {self.horario}")
        logger.info(f"📆 Dias: {', '.join(self.dias_semana)}")
        logger.info(f"🔧 Status: {'Habilitado' if self.habilitado else 'Desabilitado'}")
        logger.info("="*80)
    
    def _get_config_bool(self, secao, chave, padrao=False):
        """Obtém valor booleano do config"""
        valor = self.config.config.get(secao, chave, fallback=str(padrao))
        return valor.lower() in ('true', 'yes', '1', 'sim')
    
    def _get_dias_semana(self):
        """Obtém dias da semana configurados"""
        dias_str = self.config.config.get('VERIFICACAO_AGENDADA', 'dias_semana', 
                                          fallback='segunda,terca,quarta,quinta,sexta')
        
        dias_map = {
            'segunda': 'monday',
            'terca': 'tuesday',
            'quarta': 'wednesday',
            'quinta': 'thursday',
            'sexta': 'friday',
            'sabado': 'saturday',
            'domingo': 'sunday'
        }
        
        dias_config = [d.strip().lower() for d in dias_str.split(',')]
        return [dias_map.get(d, d) for d in dias_config if d in dias_map]
    
    def monitor_esta_rodando(self):
        """
        Verifica se o monitor está rodando
        
        Returns:
            tuple: (bool, int ou None) - (está rodando?, PID ou None)
        """
        try:
            for processo in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = processo.info.get('cmdline', [])
                    if cmdline and 'python' in processo.info['name'].lower():
                        cmdline_str = ' '.join(cmdline).lower()
                        if 'monitor_retornos.py' in cmdline_str:
                            return True, processo.info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False, None
        
        except Exception as e:
            logger.error(f"❌ Erro ao verificar processos: {e}")
            return False, None
    
    def iniciar_monitor(self):
        """
        Inicia o monitor em modo oculto
        
        Returns:
            bool: True se iniciou com sucesso
        """
        try:
            logger.info("🚀 Iniciando monitor automaticamente...")
            
            # Caminho do script BAT para iniciar monitor
            bat_iniciar = self.projeto_dir / 'scripts' / 'bat' / 'INICIAR_MONITOR_OCULTO.bat'
            
            if not bat_iniciar.exists():
                logger.error(f"❌ Arquivo não encontrado: {bat_iniciar}")
                return False
            
            # Executa o BAT
            resultado = subprocess.run(
                ['cmd', '/c', str(bat_iniciar)],
                cwd=str(self.projeto_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Aguarda 3 segundos para o monitor iniciar
            time.sleep(3)
            
            # Verifica se realmente iniciou
            rodando, pid = self.monitor_esta_rodando()
            
            if rodando:
                logger.info(f"✅ Monitor iniciado com sucesso! PID: {pid}")
                return True
            else:
                logger.error("❌ Monitor não iniciou corretamente")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("❌ Timeout ao iniciar monitor")
            return False
        
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar monitor: {e}")
            return False
    
    def verificar_e_agir(self):
        """
        Verifica se o monitor está rodando e age conforme necessário
        """
        logger.info("")
        logger.info("="*80)
        logger.info(f"🔍 VERIFICAÇÃO AGENDADA - {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
        logger.info("="*80)
        
        # Verifica se está rodando
        rodando, pid = self.monitor_esta_rodando()
        
        if rodando:
            logger.info(f"✅ Monitor está ativo - PID: {pid}")
            logger.info("="*80)
            return
        
        # Monitor NÃO está rodando - alerta e reinicia
        logger.warning("⚠️  MONITOR NÃO ESTÁ RODANDO!")
        logger.info("🔄 Tentando reiniciar automaticamente...")
        
        # Notifica ANTES de tentar reiniciar
        self.notificador_windows.notificar_monitor_caiu_reiniciando()
        
        # Tenta iniciar
        sucesso = self.iniciar_monitor()
        
        if sucesso:
            logger.info("✅ Monitor reiniciado com sucesso!")
            
            # Notifica sucesso
            self.notificador_windows.notificar_monitor_reiniciado()
            self.notificador_email.notificar_monitor_iniciado()
            
        else:
            logger.error("❌ FALHA ao reiniciar monitor!")
            logger.error("⚠️  AÇÃO MANUAL NECESSÁRIA!")
            
            # Notifica falha crítica
            self.notificador_windows.notificar_erro_critico(
                "Falha ao Reiniciar Monitor",
                "O monitor não está rodando e não foi possível reiniciá-lo automaticamente. Verifique imediatamente!"
            )
            
            if self.notificador_email.habilitado:
                self.notificador_email.notificar_erro(
                    "MONITOR CAIU",
                    "O monitor não está rodando e a tentativa de reinício automático falhou. Ação manual necessária!"
                )
        
        logger.info("="*80)
    
    def agendar_verificacoes(self):
        """Agenda as verificações nos horários configurados"""
        if not self.habilitado:
            logger.warning("⚠️  Agendador desabilitado no config.ini")
            return
        
        # Agenda para cada dia da semana configurado
        for dia in self.dias_semana:
            getattr(schedule.every(), dia).at(self.horario).do(self.verificar_e_agir)
            logger.info(f"📅 Agendado: {dia.capitalize()} às {self.horario}")
        
        logger.info("")
        logger.info("👀 Agendador ativo. Aguardando horários programados...")
        logger.info("   (Pressione Ctrl+C para parar)")
        logger.info("")
    
    def executar(self):
        """Loop principal do agendador"""
        try:
            self.agendar_verificacoes()
            
            # Loop infinito verificando agendamentos
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        
        except KeyboardInterrupt:
            logger.info("")
            logger.info("="*80)
            logger.info("⏹️  Agendador encerrado pelo usuário")
            logger.info("="*80)


def verificar_agora():
    """Executa verificação imediata (modo teste)"""
    logger.info("\n🧪 MODO TESTE - Verificação Imediata\n")
    agendador = AgendadorVerificacao()
    agendador.verificar_e_agir()


def main():
    """Função principal"""
    # Verifica se é modo teste (argumento --testar)
    if len(sys.argv) > 1 and sys.argv[1] == '--testar':
        verificar_agora()
        return
    
    # Modo normal - agendador contínuo
    agendador = AgendadorVerificacao()
    agendador.executar()


if __name__ == "__main__":
    main()
