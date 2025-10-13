"""
Monitor Automático de Arquivos de Retorno Bancário
Processa automaticamente arquivos CBR724 que chegam na pasta de entrada
"""
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processador_cbr724 import ProcessadorCBR724
from integrador_access import IntegradorAccess
from config_manager import get_config
from notificador_windows import NotificadorWindows
from notificador_email import NotificadorEmail

# Garantir que estamos executando no diretório correto
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

# Carregar configurações do config.ini
try:
    cfg = get_config()
except Exception as e:
    print(f"❌ ERRO ao carregar config.ini: {e}")
    print(f"Certifique-se de que config.ini existe em: {SCRIPT_DIR}")
    sys.exit(1)

# Handler customizado que grava logs no TOPO do arquivo
class TopFileHandler(logging.FileHandler):
    """Handler que escreve logs no topo do arquivo (mais recentes primeiro)"""
    
    def emit(self, record):
        try:
            msg = self.format(record) + '\n'
            
            # Ler conteúdo existente
            if os.path.exists(self.baseFilename):
                with open(self.baseFilename, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            else:
                old_content = ''
            
            # Escrever nova mensagem no topo + conteúdo antigo
            with open(self.baseFilename, 'w', encoding='utf-8') as f:
                f.write(msg + old_content)
                
        except Exception:
            self.handleError(record)

# Configuração de logging usando config.ini
logging.basicConfig(
    level=getattr(logging, cfg.nivel_log),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        TopFileHandler(cfg.caminho_log_completo, encoding='utf-8'),  # Logs no topo
        logging.StreamHandler()  # Console normal
    ]
)
logger = logging.getLogger(__name__)

class ProcessadorRetornoHandler(FileSystemEventHandler):
    """Manipulador de eventos de arquivo para processar retornos automaticamente"""
    
    def __init__(self, pasta_entrada, pasta_processados, pasta_erro):
        self.pasta_entrada = Path(pasta_entrada)
        self.pasta_processados = Path(pasta_processados)
        self.pasta_erro = Path(pasta_erro)
        self.arquivos_processando = set()
        
        # Inicializar notificadores (Windows e E-mail)
        self.notificador = NotificadorWindows()
        self.notificador_email = NotificadorEmail()
        
        # Criar pastas se não existirem
        self.pasta_processados.mkdir(parents=True, exist_ok=True)
        self.pasta_erro.mkdir(parents=True, exist_ok=True)
        
        logger.info("="*80)
        logger.info("🤖 MONITOR AUTOMÁTICO DE RETORNOS INICIADO")
        logger.info("="*80)
        logger.info(f"📂 Monitorando: {self.pasta_entrada}")
        logger.info(f"✅ Processados: {self.pasta_processados}")
        logger.info(f"❌ Erros: {self.pasta_erro}")
        logger.info("="*80)
        
        # Enviar notificações de início
        self.notificador.notificar_monitor_iniciado(str(self.pasta_entrada))
        self.notificador_email.notificar_monitor_iniciado()
    
    def on_created(self, event):
        """Chamado quando um novo arquivo é criado na pasta"""
        if event.is_directory:
            return
        
        arquivo = Path(event.src_path)
        
        # Ignorar arquivos temporários e que não são .ret
        if arquivo.suffix.lower() != '.ret':
            return
        
        # EXCLUIR arquivos IEDCBR (instrução de entrada, não retorno)
        if 'IEDCBR' in arquivo.name.upper():
            try:
                arquivo.unlink()  # Excluir o arquivo
                logger.info(f"🗑️  Arquivo IEDCBR excluído: {arquivo.name}")
                self.notificador.notificar_arquivo_iedcbr_excluido(arquivo.name)
            except Exception as e:
                logger.error(f"❌ Erro ao excluir arquivo IEDCBR {arquivo.name}: {e}")
            return
        
        # Processar o arquivo
        self.processar_arquivo(arquivo)
    
    def on_modified(self, event):
        """Chamado quando um arquivo é modificado (pode ser quando termina de copiar)"""
        if event.is_directory:
            return
        
        arquivo = Path(event.src_path)
        
        # Verificar se é .ret e não está sendo processado
        if arquivo.suffix.lower() == '.ret' and arquivo not in self.arquivos_processando:
            # Aguardar para garantir que o arquivo foi completamente copiado (via config.ini)
            time.sleep(cfg.tempo_espera_arquivo)
            
            # EXCLUIR IEDCBR (se configurado no config.ini)
            if cfg.excluir_ied and 'IEDCBR' in arquivo.name.upper():
                try:
                    arquivo.unlink()  # Excluir o arquivo
                    logger.info(f"🗑️  Arquivo IEDCBR excluído: {arquivo.name}")
                    self.notificador.notificar_arquivo_iedcbr_excluido(arquivo.name)
                except Exception as e:
                    logger.error(f"❌ Erro ao excluir arquivo IEDCBR {arquivo.name}: {e}")
                return
            
            # Verificar se o arquivo ainda existe e não é vazio
            if arquivo.exists() and arquivo.stat().st_size > 0:
                self.processar_arquivo(arquivo)
    
    def processar_arquivo(self, arquivo):
        """Processa um arquivo de retorno"""
        # Evitar processamento duplicado
        if arquivo in self.arquivos_processando:
            return
        
        self.arquivos_processando.add(arquivo)
        
        try:
            logger.info("")
            logger.info("="*80)
            logger.info(f"🆕 NOVO ARQUIVO DETECTADO: {arquivo.name}")
            logger.info("="*80)
            
            # Notificar arquivo detectado
            self.notificador.notificar_arquivo_detectado(arquivo.name)
            
            # Aguardar arquivo estar completamente escrito
            tamanho_anterior = 0
            while True:
                try:
                    tamanho_atual = arquivo.stat().st_size
                    if tamanho_atual == tamanho_anterior and tamanho_atual > 0:
                        break
                    tamanho_anterior = tamanho_atual
                    time.sleep(0.5)
                except Exception:
                    time.sleep(0.5)
            
            # Detectar tipo de arquivo
            with open(arquivo, 'r', encoding='latin-1') as f:
                primeira_linha = f.readline()
            
            # Verificar se é CBR724
            if primeira_linha.startswith('000000CBR7'):
                logger.info("📋 Tipo detectado: CBR724")
                self._processar_cbr724(arquivo)
            else:
                logger.warning(f"⚠️  Tipo de arquivo não reconhecido: {arquivo.name}")
                self._mover_para_erro(arquivo, "Tipo de arquivo não reconhecido")
        
        except Exception as e:
            logger.error(f"❌ Erro ao processar {arquivo.name}: {e}")
            self._mover_para_erro(arquivo, str(e))
        
        finally:
            self.arquivos_processando.discard(arquivo)
    
    def _processar_cbr724(self, arquivo):
        """Processa arquivo CBR724"""
        try:
            # Processar arquivo
            logger.info("🔄 Processando arquivo CBR724...")
            processador = ProcessadorCBR724()
            registros = processador.processar_arquivo(str(arquivo))
            
            if not registros:
                logger.warning("⚠️  Nenhum registro encontrado no arquivo")
                self._mover_para_erro(arquivo, "Nenhum registro encontrado")
                return
            
            logger.info(f"✓ {len(registros)} registros encontrados")
            
            # Configuração para integração com Access (via config.ini)
            config_integrador = cfg.get_config_integrador()
            
            # Integrar com Access
            logger.info("🔄 Integrando com banco Access...")
            integrador = IntegradorAccess(config_integrador)
            resultado = integrador.processar_registros(registros)
            
            # Verificar resultado
            if resultado['erros'] > 0:
                logger.warning(f"⚠️  Processamento com {resultado['erros']} erro(s)")
                self.notificador.notificar_processamento_erro(
                    arquivo.name,
                    f"{resultado['erros']} erro(s) no processamento"
                )
                self.notificador_email.notificar_erro(
                    arquivo.name,
                    f"{resultado['erros']} erro(s) no processamento"
                )
                self._mover_para_erro(arquivo, f"{resultado['erros']} erros no processamento")
            else:
                logger.info("✅ Processamento concluído com sucesso!")
                logger.info(f"   • Processados: {resultado['total_processados']}")
                logger.info(f"   • Criados: {resultado['criados']}")
                logger.info(f"   • Baixas: {resultado['baixas']}")
                logger.info(f"   • Cancelados: {resultado['cancelados']}")
                
                # Notificar sucesso (Windows e E-mail)
                self.notificador.notificar_processamento_sucesso(
                    arquivo.name,
                    titulos_criados=resultado.get('criados', 0),
                    titulos_pagos=resultado.get('baixas', 0),
                    titulos_cancelados=resultado.get('cancelados', 0)
                )
                self.notificador_email.notificar_sucesso(
                    arquivo.name,
                    registros_processados=resultado.get('total_processados', 0)
                )
                
                self._mover_para_processados(arquivo)
        
        except Exception as e:
            logger.error(f"❌ Erro no processamento CBR724: {e}", exc_info=True)
            self.notificador.notificar_processamento_erro(arquivo.name, str(e))
            self.notificador_email.notificar_erro(arquivo.name, str(e))
            self._mover_para_erro(arquivo, str(e))
    
    def _mover_para_processados(self, arquivo):
        """Move arquivo para pasta de processados"""
        try:
            # Adicionar sufixo -processado (sem timestamp)
            nome_novo = f"{arquivo.stem}-processado{arquivo.suffix}"
            destino = self.pasta_processados / nome_novo
            
            arquivo.rename(destino)
            logger.info(f"📦 Movido para: {destino.name}")
            logger.info("="*80)
        
        except Exception as e:
            logger.error(f"❌ Erro ao mover arquivo: {e}")
    
    def _mover_para_erro(self, arquivo, motivo):
        """Move arquivo para pasta de erro"""
        try:
            # Adicionar sufixo -erro e timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_novo = f"{arquivo.stem}-erro_{timestamp}{arquivo.suffix}"
            destino = self.pasta_erro / nome_novo
            
            arquivo.rename(destino)
            logger.error(f"💥 Movido para ERRO: {destino.name}")
            logger.error(f"   Motivo: {motivo}")
            logger.info("="*80)
        
        except Exception as e:
            logger.error(f"❌ Erro ao mover arquivo para pasta de erro: {e}")


def processar_arquivos_existentes(event_handler, pasta_entrada):
    """
    Processa arquivos .ret que já existem na pasta antes do monitor iniciar
    
    Args:
        event_handler: Handler de eventos do monitor
        pasta_entrada: Pasta a ser verificada
    """
    pasta = Path(pasta_entrada)
    arquivos_ret = list(pasta.glob("*.ret"))
    
    if arquivos_ret:
        logger.info("")
        logger.info("="*80)
        logger.info(f"🔍 VERIFICAÇÃO INICIAL: {len(arquivos_ret)} arquivo(s) .ret encontrado(s)")
        logger.info("="*80)
        
        for arquivo in arquivos_ret:
            # Ignorar arquivos IEDCBR
            if 'IEDCBR' in arquivo.name.upper():
                if cfg.excluir_ied:
                    try:
                        arquivo.unlink()
                        logger.info(f"🗑️  Arquivo IEDCBR excluído: {arquivo.name}")
                    except Exception as e:
                        logger.error(f"❌ Erro ao excluir IEDCBR {arquivo.name}: {e}")
                continue
            
            # Processar arquivo existente
            logger.info(f"📄 Processando arquivo existente: {arquivo.name}")
            event_handler.processar_arquivo(arquivo)
        
        logger.info("")
        logger.info("="*80)
        logger.info("✅ Verificação inicial concluída")
        logger.info("="*80)
        logger.info("")
    else:
        logger.info("📭 Nenhum arquivo .ret encontrado na verificação inicial")
        logger.info("")


def main():
    """Inicia o monitor automático"""
    # Log do diretório de trabalho para debug
    logger.info(f"📂 Diretório de trabalho: {os.getcwd()}")
    logger.info(f"📜 Arquivo de log: {cfg.caminho_log_completo}")
    
    # Configurar pastas usando config.ini
    pasta_entrada = cfg.pasta_retorno
    pasta_processados = cfg.pasta_processados
    pasta_erro = cfg.pasta_erro
    
    # Criar o manipulador de eventos
    event_handler = ProcessadorRetornoHandler(
        pasta_entrada=pasta_entrada,
        pasta_processados=pasta_processados,
        pasta_erro=pasta_erro
    )
    
    # 🆕 PROCESSAR ARQUIVOS QUE JÁ EXISTEM NA PASTA (se configurado)
    if cfg.processar_existentes_ao_iniciar:
        processar_arquivos_existentes(event_handler, pasta_entrada)
    else:
        logger.info("⏭️  Verificação inicial desabilitada (processar_existentes_ao_iniciar = false)")
        logger.info("")
    
    # Criar o observador
    observer = Observer()
    observer.schedule(event_handler, str(pasta_entrada), recursive=False)
    observer.start()
    
    logger.info("👀 Aguardando novos arquivos...")
    logger.info("   (Pressione Ctrl+C para parar)")
    logger.info("")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("")
        logger.info("="*80)
        logger.info("⏹️  Monitor encerrado pelo usuário")
        logger.info("="*80)
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    main()
