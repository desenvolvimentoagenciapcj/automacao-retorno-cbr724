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
        self.horario = self.config.config.get('VERIFICACAO_AGENDADA', 'horario', fallback='08:30')
        self.dias_semana = self._get_dias_semana()
        
        # Controle de recuperação persistente
        self.em_recuperacao = False
        self.hora_inicio_recuperacao = None
        self.tentativas_recuperacao = 0
        self.max_tentativas = 6  # 30 minutos (6 tentativas x 5 min)
        
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
    
    def servidor_esta_acessivel(self):
        """
        Verifica se o servidor está acessível
        
        Returns:
            bool: True se servidor está acessível
        """
        try:
            pasta_retorno = self.config.pasta_retorno
            return os.path.exists(pasta_retorno) and os.path.isdir(pasta_retorno)
        except:
            return False
    
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
        Verificação inteligente: tenta recuperar até 9h antes de desistir
        """
        logger.info("")
        logger.info("="*80)
        logger.info(f"🔍 VERIFICAÇÃO AGENDADA - {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
        logger.info("="*80)
        
        hora_atual = datetime.now()
        hora_limite = hora_atual.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # PASSO 1: Verificar servidor
        servidor_ok = self.servidor_esta_acessivel()
        if not servidor_ok:
            logger.warning("⚠️  SERVIDOR INACESSÍVEL!")
            
            if not self.em_recuperacao:
                # Primeira detecção - iniciar processo de recuperação
                self.em_recuperacao = True
                self.hora_inicio_recuperacao = hora_atual
                self.tentativas_recuperacao = 0
                
                logger.warning("🔄 Iniciando processo de recuperação...")
                logger.info(f"   Tentativas a cada 5 minutos até {hora_limite.strftime('%H:%M')}")
                
                # Notificar
                self.notificador_windows.notificar_erro_critico(
                    "Servidor Inacessível às 8h30",
                    "Sistema tentará recuperar a cada 5 minutos até 9h"
                )
            
            # Verifica se ainda está dentro do prazo
            if hora_atual < hora_limite and self.tentativas_recuperacao < self.max_tentativas:
                self.tentativas_recuperacao += 1
                logger.info(f"   Tentativa {self.tentativas_recuperacao}/{self.max_tentativas}")
                logger.info(f"   Próxima verificação em 5 minutos...")
                
                # Agenda próxima tentativa daqui a 5 minutos
                schedule.every(5).minutes.do(self.verificar_e_agir).tag('recuperacao')
                logger.info("="*80)
                return
            else:
                # Passou das 9h ou esgotou tentativas - DESISTIR
                logger.error("="*80)
                logger.error("❌ FALHA CRÍTICA - Servidor continua inacessível")
                logger.error(f"   Tentativas: {self.tentativas_recuperacao}")
                logger.error(f"   Horário atual: {hora_atual.strftime('%H:%M')}")
                logger.error("   AÇÃO MANUAL URGENTE NECESSÁRIA!")
                logger.error("="*80)
                
                # Notificar FALHA CRÍTICA
                self.notificador_windows.notificar_erro_critico(
                    "FALHA CRÍTICA - Servidor Inacessível",
                    f"Servidor continua inacessível após {self.tentativas_recuperacao} tentativas.\nAção manual URGENTE!"
                )
                
                if self.notificador_email.habilitado:
                    self.notificador_email.notificar_erro(
                        "🚨 FALHA CRÍTICA - Servidor Inacessível às 9h",
                        f"""ATENÇÃO: Servidor continua inacessível!
                        
⏰ Horário Limite: 9h00
🔄 Tentativas Realizadas: {self.tentativas_recuperacao}
📁 Servidor: {self.config.pasta_retorno}

❌ STATUS: Servidor NÃO está acessível

⚠️  AÇÃO URGENTE NECESSÁRIA:
1. Verificar se servidor \\SERVIDOR1 está ligado
2. Verificar conexão de rede
3. Testar acesso manual à pasta
4. Após correção, executar: .\\PROCESSAR.bat

Arquivos de retorno NÃO estão sendo processados!"""
                    )
                
                # Reset para próximo dia
                self.em_recuperacao = False
                schedule.clear('recuperacao')
                logger.info("="*80)
                return
        
        # PASSO 2: Servidor OK - verificar monitor
        rodando, pid = self.monitor_esta_rodando()
        
        if rodando and servidor_ok:
            logger.info(f"✅ Sistema OK - Monitor ativo (PID: {pid}) e Servidor acessível")
            
            # Se estava em recuperação, notificar sucesso
            if self.em_recuperacao:
                logger.info("✅ RECUPERAÇÃO BEM-SUCEDIDA!")
                logger.info(f"   Recuperado após {self.tentativas_recuperacao} tentativa(s)")
                
                self.notificador_windows.notificar_sucesso(
                    "Sistema Recuperado",
                    "Monitor ativo e servidor acessível!"
                )
                
                if self.notificador_email.habilitado:
                    self.notificador_email.notificar_sucesso(
                        "✅ Sistema Recuperado com Sucesso",
                        f"""Sistema voltou ao normal!
                        
⏰ Horário: {hora_atual.strftime('%H:%M:%S')}
🔄 Tentativas até recuperar: {self.tentativas_recuperacao}

✅ Monitor: Ativo (PID {pid})
✅ Servidor: Acessível

Sistema processando retornos normalmente."""
                    )
                
                # Reset
                self.em_recuperacao = False
                self.tentativas_recuperacao = 0
                schedule.clear('recuperacao')
            
            logger.info("="*80)
            return
        
        # PASSO 3: Servidor OK mas monitor NÃO está rodando
        logger.warning("⚠️  MONITOR NÃO ESTÁ RODANDO!")
        logger.info("🔄 Tentando reiniciar automaticamente...")
        
        if not self.em_recuperacao:
            self.em_recuperacao = True
            self.hora_inicio_recuperacao = hora_atual
            self.tentativas_recuperacao = 0
            self.notificador_windows.notificar_monitor_caiu_reiniciando()
        
        # Tenta iniciar
        sucesso = self.iniciar_monitor()
        
        if sucesso:
            logger.info("✅ Monitor reiniciado com sucesso!")
            self.notificador_windows.notificar_monitor_reiniciado()
            self.notificador_email.notificar_monitor_iniciado()
            
            # Reset
            self.em_recuperacao = False
            self.tentativas_recuperacao = 0
            schedule.clear('recuperacao')
        else:
            # Falhou - verificar se ainda está dentro do prazo
            if hora_atual < hora_limite and self.tentativas_recuperacao < self.max_tentativas:
                self.tentativas_recuperacao += 1
                logger.warning(f"⚠️  Falha ao iniciar - Tentativa {self.tentativas_recuperacao}/{self.max_tentativas}")
                logger.info("   Próxima tentativa em 5 minutos...")
                
                # Agenda próxima tentativa
                schedule.every(5).minutes.do(self.verificar_e_agir).tag('recuperacao')
            else:
                # DESISTIR
                logger.error("="*80)
                logger.error("❌ FALHA CRÍTICA - Monitor não iniciou")
                logger.error(f"   Tentativas: {self.tentativas_recuperacao}")
                logger.error("   AÇÃO MANUAL URGENTE NECESSÁRIA!")
                logger.error("="*80)
                
                self.notificador_windows.notificar_erro_critico(
                    "FALHA CRÍTICA - Monitor Não Iniciou",
                    f"Monitor não iniciou após {self.tentativas_recuperacao} tentativas. Ação manual URGENTE!"
                )
                
                if self.notificador_email.habilitado:
                    self.notificador_email.notificar_erro(
                        "🚨 FALHA CRÍTICA - Monitor Não Iniciou às 9h",
                        f"""ATENÇÃO: Monitor não conseguiu iniciar!
                        
⏰ Horário Limite: 9h00
🔄 Tentativas: {self.tentativas_recuperacao}

❌ STATUS: Monitor NÃO está rodando

⚠️  AÇÃO URGENTE:
1. Executar: .\\STATUS.bat
2. Verificar logs em: logs\\monitor_retornos.log
3. Tentar manualmente: .\\INICIAR.bat
4. Processar pendentes: .\\PROCESSAR.bat

Arquivos de retorno NÃO estão sendo processados!"""
                    )
                
                # Reset
                self.em_recuperacao = False
                schedule.clear('recuperacao')
        
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
                time.sleep(30)  # Verifica a cada 30 segundos (para captar agendamentos de 5 min)
        
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
