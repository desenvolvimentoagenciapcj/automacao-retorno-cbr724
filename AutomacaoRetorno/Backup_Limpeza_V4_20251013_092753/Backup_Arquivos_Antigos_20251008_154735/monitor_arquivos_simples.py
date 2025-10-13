#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Arquivos de Retorno Bancário - VERSÃO SIMPLIFICADA
Sistema básico de automação para processamento de arquivos CNAB
"""

import os
import time
import yaml
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processador_cbr724 import ProcessadorCBR724
from integrador_access import IntegradorAccess

class MonitorArquivos(FileSystemEventHandler):
    """Classe responsável por monitorar a pasta de entrada de arquivos"""
    
    def __init__(self, config):
        self.config = config
        # APENAS processador CBR724 (conforme especificação do manual)
        self.processador_cbr724 = ProcessadorCBR724()
        self.integrador = IntegradorAccess(config)
        
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
        """Verifica se o arquivo é um retorno bancário válido - APENAS CBR724 conforme manual"""
        nome = os.path.basename(arquivo).upper()
        extensoes_validas = ['.RET', '.TXT', '.REM', '.CRT']
        
        # Verificar extensão
        if not any(nome.endswith(ext) for ext in extensoes_validas):
            return False
        
        # APAGAR arquivos IEDCBR automaticamente (conforme manual - processar APENAS CBR724)
        if nome.startswith('IEDCBR'):
            try:
                os.remove(arquivo)
                self.logger.warning(f"🗑️  Arquivo IEDCBR APAGADO automaticamente (conforme manual): {nome}")
            except Exception as e:
                self.logger.error(f"Erro ao apagar arquivo IEDCBR {nome}: {e}")
            return False
        
        # APENAS arquivos CBR724 são processados (conforme especificação do manual)
        if nome.startswith('CBR724'):
            # Verificar tamanho mínimo
            try:
                if os.path.getsize(arquivo) < 100:  # Arquivo muito pequeno
                    return False
            except OSError:
                return False
            return True
        
        # Ignorar todos os outros formatos
        return False
    
    def processar_arquivo(self, arquivo):
        """Processa um arquivo de retorno"""
        nome_arquivo = os.path.basename(arquivo)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            self.logger.info(f"Iniciando processamento: {nome_arquivo}")
            print(f"\n{'='*60}")
            print(f"🔄 PROCESSANDO: {nome_arquivo}")
            print(f"{'='*60}")
            
            # Fazer backup do banco antes do processamento
            if self.config['bancos']['backup_antes_processo']:
                print("📦 Criando backup dos bancos...")
                self.integrador.fazer_backup()
            
            # Processar apenas CBR724 (conforme especificação do manual)
            print("📄 Processando arquivo CBR724 (160 caracteres)...")
            registros = self.processador_cbr724.processar_arquivo(arquivo)
            
            if not registros:
                raise Exception("Nenhum registro válido encontrado no arquivo")
            
            print(f"✅ {len(registros)} registros encontrados")
            
            # Integrar com o banco Access
            print("💾 Integrando com banco Access...")
            resultado = self.integrador.processar_registros(registros)
            
            # Mover arquivo para pasta de processados
            arquivo_processado = os.path.join(
                self.config['diretorios']['processados'],
                f"{timestamp}_{nome_arquivo}"
            )
            os.rename(arquivo, arquivo_processado)
            
            # Exibir resultado
            print(f"\n{'='*60}")
            print(f"✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print(f"{'='*60}")
            print(f"📊 Registros processados: {len(registros)}")
            print(f"💰 Baixas realizadas: {resultado.get('baixas', 0)}")
            print(f"🔄 Atualizações: {resultado.get('atualizacoes', 0)}")
            print(f"❌ Erros: {resultado.get('erros', 0)}")
            print(f"🔍 Não encontrados: {resultado.get('nao_encontrados', 0)}")
            print(f"{'='*60}\n")
            
            self.logger.info(f"Arquivo processado com sucesso: {nome_arquivo}")
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {nome_arquivo}: {str(e)}")
            
            print(f"\n{'='*60}")
            print(f"❌ ERRO NO PROCESSAMENTO!")
            print(f"{'='*60}")
            print(f"Arquivo: {nome_arquivo}")
            print(f"Erro: {str(e)}")
            print(f"{'='*60}\n")
            
            # Mover arquivo para pasta de erro
            arquivo_erro = os.path.join(
                self.config['diretorios']['erro'],
                f"{timestamp}_ERRO_{nome_arquivo}"
            )
            try:
                os.rename(arquivo, arquivo_erro)
            except OSError:
                pass
    
    def processar_arquivos_pendentes(self):
        """Processa arquivos que já estão na pasta de entrada"""
        pasta_entrada = self.config['diretorios']['entrada']
        
        try:
            arquivos = [f for f in os.listdir(pasta_entrada) 
                       if os.path.isfile(os.path.join(pasta_entrada, f))]
            
            if arquivos:
                self.logger.info(f"Encontrados {len(arquivos)} arquivos pendentes")
                print(f"\n📂 Encontrados {len(arquivos)} arquivos pendentes para processar\n")
                
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
        
        print("\n" + "=" * 60)
        print("🏦 SISTEMA DE AUTOMAÇÃO - RETORNO BANCÁRIO CBR724")
        print("=" * 60)
        print(f"📁 Monitorando: {config['diretorios']['entrada']}")
        print(f"📄 Formato: CBR724 (160 caracteres)")
        print(f"💾 Banco Baixa: {config['bancos']['baixa']['caminho']}")
        print(f"💾 Banco Cobrança: {config['bancos']['cobranca']['caminho']}")
        print(f"📝 Logs: {config['diretorios']['logs']}")
        print("=" * 60 + "\n")
        
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
        print("✅ Monitor iniciado e aguardando novos arquivos...")
        print("⏹️  Pressione Ctrl+C para parar.\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Parando monitor...")
            observer.stop()
        
        observer.join()
        print("✅ Monitor finalizado.\n")
        
    except FileNotFoundError:
        print("❌ Arquivo config.yaml não encontrado!")
        print("Certifique-se de que o arquivo de configuração existe.")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()