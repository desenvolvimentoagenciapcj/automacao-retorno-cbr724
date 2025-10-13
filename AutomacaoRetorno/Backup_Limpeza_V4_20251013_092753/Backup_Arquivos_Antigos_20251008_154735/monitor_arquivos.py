#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Arquivos de Retorno Bancário
Sistema de automação para processamento de arquivos CNAB
"""

import os
import time
import yaml
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processador_cnab import ProcessadorCNAB
from integrador_access import IntegradorAccess
from notificador import Notificador

class MonitorArquivos(FileSystemEventHandler):
    """Classe responsável por monitorar a pasta de entrada de arquivos"""
    
    def __init__(self, config):
        self.config = config
        self.processador = ProcessadorCNAB(config)
        self.integrador = IntegradorAccess(config)
        self.notificador = Notificador(config)
        
        # Configurar logging
        self.setup_logging()
        
        # Criar diretórios necessários
        self.criar_diretorios()
        
        self.logger.info("Monitor de arquivos iniciado")
    
    def setup_logging(self):
        """Configura o sistema de logs"""
        log_dir = Path(self.config['diretorios']['logs'])
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"monitor_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, self.config['log']['nivel']),
            format=self.config['log']['formato'],
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def criar_diretorios(self):
        """Cria os diretórios necessários se não existirem"""
        diretorios = [
            self.config['diretorios']['entrada'],
            self.config['diretorios']['processados'],
            self.config['diretorios']['erro'],
            self.config['diretorios']['backup'],
            self.config['diretorios']['logs']
        ]
        
        for diretorio in diretorios:
            Path(diretorio).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Diretório verificado/criado: {diretorio}")
    
    def on_created(self, event):
        """Evento disparado quando um novo arquivo é criado na pasta monitorada"""
        if event.is_directory:
            return
        
        arquivo = event.src_path
        nome_arquivo = os.path.basename(arquivo)
        
        self.logger.info(f"Novo arquivo detectado: {nome_arquivo}")
        
        # Aguardar um pouco para garantir que o arquivo foi completamente copiado
        time.sleep(2)
        
        # Verificar se é um arquivo de retorno válido
        if self.is_arquivo_retorno(arquivo):
            self.processar_arquivo(arquivo)
        else:
            self.logger.warning(f"Arquivo ignorado (não é retorno bancário): {nome_arquivo}")
    
    def is_arquivo_retorno(self, arquivo):
        """Verifica se o arquivo é um retorno bancário válido"""
        nome = os.path.basename(arquivo).upper()
        extensoes_validas = ['.RET', '.TXT', '.REM', '.CRT']
        
        # Verificar extensão
        if not any(nome.endswith(ext) for ext in extensoes_validas):
            return False
        
        # Verificar tamanho mínimo
        try:
            if os.path.getsize(arquivo) < 100:  # Arquivo muito pequeno
                return False
        except OSError:
            return False
        
        # Verificar se contém indicadores de CNAB
        try:
            with open(arquivo, 'r', encoding='latin1') as f:
                primeira_linha = f.readline()
                # Header CNAB240 começa com '01' ou CNAB400 com '0'
                if primeira_linha.startswith(('01', '0')):
                    return True
        except Exception as e:
            self.logger.error(f"Erro ao verificar arquivo {arquivo}: {e}")
            return False
        
        return False
    
    def processar_arquivo(self, arquivo):
        """Processa um arquivo de retorno"""
        nome_arquivo = os.path.basename(arquivo)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            self.logger.info(f"Iniciando processamento: {nome_arquivo}")
            
            # Fazer backup do banco antes do processamento
            if self.config['banco']['backup_antes_processo']:
                self.integrador.fazer_backup()
            
            # Processar arquivo CNAB
            registros = self.processador.processar_arquivo(arquivo)
            
            if not registros:
                raise Exception("Nenhum registro válido encontrado no arquivo")
            
            # Integrar com o banco Access
            resultado = self.integrador.processar_registros(registros)
            
            # Mover arquivo para pasta de processados
            arquivo_processado = os.path.join(
                self.config['diretorios']['processados'],
                f"{timestamp}_{nome_arquivo}"
            )
            os.rename(arquivo, arquivo_processado)
            
            # Enviar notificação de sucesso
            self.notificador.enviar_sucesso(nome_arquivo, resultado)
            
            self.logger.info(f"Arquivo processado com sucesso: {nome_arquivo}")
            self.logger.info(f"Registros processados: {len(registros)}")
            self.logger.info(f"Baixas realizadas: {resultado.get('baixas', 0)}")
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {nome_arquivo}: {str(e)}")
            
            # Mover arquivo para pasta de erro
            arquivo_erro = os.path.join(
                self.config['diretorios']['erro'],
                f"{timestamp}_ERRO_{nome_arquivo}"
            )
            try:
                os.rename(arquivo, arquivo_erro)
            except OSError:
                pass
            
            # Enviar notificação de erro
            self.notificador.enviar_erro(nome_arquivo, str(e))
    
    def processar_arquivos_pendentes(self):
        """Processa arquivos que já estão na pasta de entrada"""
        pasta_entrada = self.config['diretorios']['entrada']
        
        try:
            arquivos = [f for f in os.listdir(pasta_entrada) 
                       if os.path.isfile(os.path.join(pasta_entrada, f))]
            
            if arquivos:
                self.logger.info(f"Encontrados {len(arquivos)} arquivos pendentes")
                
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_entrada, arquivo)
                    if self.is_arquivo_retorno(caminho_completo):
                        self.processar_arquivo(caminho_completo)
                        time.sleep(1)  # Pequena pausa entre processamentos
        except Exception as e:
            self.logger.error(f"Erro ao processar arquivos pendentes: {e}")

def main():
    """Função principal"""
    try:
        # Carregar configurações
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("=" * 60)
        print("🏦 SISTEMA DE AUTOMAÇÃO - RETORNO BANCÁRIO")
        print("=" * 60)
        print(f"📁 Monitorando: {config['diretorios']['entrada']}")
        print(f"💾 Banco Access: {config['banco']['caminho']}")
        print(f"📧 Notificações: {'Ativadas' if config['email']['enviar_sucesso'] else 'Desativadas'}")
        print("=" * 60)
        
        # Criar monitor
        monitor = MonitorArquivos(config)
        
        # Processar arquivos já existentes
        monitor.processar_arquivos_pendentes()
        
        # Configurar observer
        observer = Observer()
        observer.schedule(
            monitor, 
            config['diretorios']['entrada'], 
            recursive=False
        )
        
        # Iniciar monitoramento
        observer.start()
        print("✅ Monitor iniciado! Pressione Ctrl+C para parar.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando monitor...")
            observer.stop()
        
        observer.join()
        print("✅ Monitor finalizado.")
        
    except FileNotFoundError:
        print("❌ Arquivo config.yaml não encontrado!")
        print("Certifique-se de que o arquivo de configuração existe.")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()