#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Configuração
Lê configurações do arquivo config.ini
"""

import os
import configparser
from pathlib import Path

class Config:
    """Gerenciador de configurações do sistema"""
    
    def __init__(self, arquivo_config='config.ini'):
        """Inicializa e carrega configurações"""
        # Caminho: scripts/python -> AutomacaoRetorno -> config/config.ini
        self.script_dir = Path(__file__).parent.absolute()
        self.projeto_dir = self.script_dir.parent.parent
        self.arquivo_config = self.projeto_dir / 'config' / arquivo_config
        
        # Verificar se config.ini existe
        if not self.arquivo_config.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.arquivo_config}\n"
                f"Por favor, certifique-se de que config.ini está na pasta: {self.projeto_dir / 'config'}"
            )
        
        # Carregar configurações
        self.config = configparser.ConfigParser()
        self.config.read(self.arquivo_config, encoding='utf-8')
        
        # Validar seções obrigatórias
        self._validar_config()
    
    def _validar_config(self):
        """Valida se todas as seções necessárias existem"""
        secoes_obrigatorias = ['CAMINHOS', 'BANCOS_ACCESS', 'PYTHON', 'LOGS', 'PROCESSAMENTO', 'DIRETORIOS']
        faltando = [s for s in secoes_obrigatorias if s not in self.config]
        
        if faltando:
            raise ValueError(
                f"Seções faltando no config.ini: {', '.join(faltando)}\n"
                f"Verifique o arquivo: {self.arquivo_config}"
            )
    
    def _get_bool(self, secao, chave, padrao=False):
        """Obtém valor booleano"""
        valor = self.config.get(secao, chave, fallback=str(padrao))
        return valor.lower() in ('true', 'yes', '1', 'sim')
    
    # =========================================================================
    # CAMINHOS
    # =========================================================================
    
    @property
    def pasta_retorno(self):
        """Pasta monitorada (onde ficam os .ret)"""
        return Path(self.config.get('CAMINHOS', 'pasta_retorno'))
    
    @property
    def pasta_processados(self):
        """Pasta para arquivos processados"""
        caminho = self.config.get('CAMINHOS', 'pasta_processados', fallback=None)
        if caminho:
            return Path(caminho)
        return self.pasta_retorno / 'Processados'
    
    @property
    def pasta_erro(self):
        """Pasta para arquivos com erro"""
        caminho = self.config.get('CAMINHOS', 'pasta_erro', fallback=None)
        if caminho:
            return Path(caminho)
        return self.pasta_retorno / 'Erro'
    
    @property
    def pasta_backup(self):
        """Pasta para backups dos bancos"""
        return Path(self.config.get('CAMINHOS', 'pasta_backup'))
    
    # =========================================================================
    # BANCOS ACCESS
    # =========================================================================
    
    @property
    def db_baixa(self):
        """Caminho do banco dbBaixa2025.accdb"""
        return self.config.get('BANCOS_ACCESS', 'db_baixa')
    
    @property
    def db_cobranca(self):
        """Caminho do banco Cobranca2019.accdb"""
        return self.config.get('BANCOS_ACCESS', 'db_cobranca')
    
    @property
    def usar_cobranca(self):
        """Usar banco de cobrança?"""
        return self._get_bool('BANCOS_ACCESS', 'usar_cobranca', False)
    
    # =========================================================================
    # PYTHON
    # =========================================================================
    
    @property
    def python_executavel(self):
        """Caminho do executável Python"""
        return self.config.get('PYTHON', 'executavel')
    
    # =========================================================================
    # LOGS
    # =========================================================================
    
    @property
    def arquivo_log(self):
        """Nome do arquivo de log"""
        return self.config.get('LOGS', 'arquivo_log', fallback='monitor_retornos.log')
    
    @property
    def nivel_log(self):
        """Nível de log (DEBUG, INFO, WARNING, ERROR)"""
        return self.config.get('LOGS', 'nivel_log', fallback='INFO').upper()
    
    @property
    def caminho_log_completo(self):
        """Caminho completo do arquivo de log"""
        return self.script_dir / self.arquivo_log
    
    # =========================================================================
    # PROCESSAMENTO
    # =========================================================================
    
    @property
    def tempo_espera_arquivo(self):
        """Tempo de espera (segundos) para arquivo ser copiado"""
        return self.config.getint('PROCESSAMENTO', 'tempo_espera_arquivo', fallback=1)
    
    @property
    def fazer_backup(self):
        """Fazer backup antes de processar?"""
        return self._get_bool('PROCESSAMENTO', 'fazer_backup', True)
    
    @property
    def excluir_ied(self):
        """Excluir automaticamente arquivos IEDCBR?"""
        return self._get_bool('PROCESSAMENTO', 'excluir_ied', True)
    
    @property
    def processar_existentes_ao_iniciar(self):
        """Processar arquivos que já existem ao iniciar monitor?"""
        return self._get_bool('PROCESSAMENTO', 'processar_existentes_ao_iniciar', True)
    
    # =========================================================================
    # DIRETÓRIOS
    # =========================================================================
    
    @property
    def dir_trabalho(self):
        """Diretório de trabalho local"""
        caminho = self.config.get('DIRETORIOS', 'dir_trabalho', fallback=None)
        if caminho:
            return Path(caminho)
        return self.script_dir
    
    @property
    def dir_producao(self):
        """Diretório de produção no servidor"""
        return self.config.get('DIRETORIOS', 'dir_producao')
    
    # =========================================================================
    # ONEDRIVE
    # =========================================================================
    
    @property
    def onedrive_backup(self):
        """Caminho do backup no OneDrive"""
        return self.config.get('ONEDRIVE', 'caminho_backup', fallback='')
    
    # =========================================================================
    # NOTIFICAÇÕES
    # =========================================================================
    
    @property
    def notificacoes_habilitadas(self):
        """Notificações Windows habilitadas?"""
        return self._get_bool('NOTIFICACOES', 'habilitado', True)
    
    # =========================================================================
    # EMAIL
    # =========================================================================
    
    @property
    def email_habilitado(self):
        """Email habilitado?"""
        return self._get_bool('EMAIL', 'habilitado', False)
    
    @property
    def email_smtp_servidor(self):
        """Servidor SMTP"""
        return self.config.get('EMAIL', 'smtp_servidor', fallback='smtp.gmail.com')
    
    @property
    def email_smtp_porta(self):
        """Porta SMTP"""
        return self.config.getint('EMAIL', 'smtp_porta', fallback=587)
    
    @property
    def email_remetente(self):
        """Email remetente"""
        return self.config.get('EMAIL', 'remetente', fallback='')
    
    @property
    def email_senha(self):
        """Senha do email"""
        return self.config.get('EMAIL', 'senha', fallback='')
    
    @property
    def email_destinatarios(self):
        """Lista de destinatários"""
        dest = self.config.get('EMAIL', 'destinatarios', fallback='')
        return [email.strip() for email in dest.split(',') if email.strip()]
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    def get_config_integrador(self):
        """Retorna configuração no formato esperado pelo IntegradorAccess"""
        return {
            'bancos': {
                'baixa': {
                    'caminho': self.db_baixa
                },
                'cobranca': {
                    'ativo': self.usar_cobranca,
                    'caminho': self.db_cobranca
                }
            },
            'diretorios': {
                'backup': str(self.pasta_backup)
            }
        }
    
    def exibir_configuracao(self):
        """Exibe configuração atual (para debug)"""
        print("\n" + "="*70)
        print("CONFIGURAÇÃO CARREGADA")
        print("="*70)
        print(f"\n📂 CAMINHOS:")
        print(f"   Pasta Retorno:    {self.pasta_retorno}")
        print(f"   Processados:      {self.pasta_processados}")
        print(f"   Erros:            {self.pasta_erro}")
        print(f"   Backup:           {self.pasta_backup}")
        print(f"\n💾 BANCOS ACCESS:")
        print(f"   DB Baixa:         {self.db_baixa}")
        print(f"   DB Cobrança:      {self.db_cobranca}")
        print(f"   Usar Cobrança:    {self.usar_cobranca}")
        print(f"\n🐍 PYTHON:")
        print(f"   Executável:       {self.python_executavel}")
        print(f"\n📝 LOGS:")
        print(f"   Arquivo:          {self.caminho_log_completo}")
        print(f"   Nível:            {self.nivel_log}")
        print(f"\n⚙️  PROCESSAMENTO:")
        print(f"   Tempo Espera:     {self.tempo_espera_arquivo}s")
        print(f"   Fazer Backup:     {self.fazer_backup}")
        print(f"   Excluir IED:      {self.excluir_ied}")
        print(f"\n📁 DIRETÓRIOS:")
        print(f"   Trabalho Local:   {self.dir_trabalho}")
        print(f"   Produção:         {self.dir_producao}")
        print(f"\n☁️  ONEDRIVE:")
        print(f"   Backup:           {self.onedrive_backup}")
        print(f"\n🔔 NOTIFICAÇÕES:")
        print(f"   Windows:          {self.notificacoes_habilitadas}")
        print(f"   Email:            {self.email_habilitado}")
        if self.email_habilitado:
            print(f"   Servidor SMTP:    {self.email_smtp_servidor}:{self.email_smtp_porta}")
            print(f"   Remetente:        {self.email_remetente}")
            print(f"   Destinatários:    {', '.join(self.email_destinatarios)}")
        print("="*70 + "\n")


# Instância global (singleton)
_config = None

def get_config():
    """Obtém instância da configuração (singleton)"""
    global _config
    if _config is None:
        _config = Config()
    return _config


# Para testes
if __name__ == '__main__':
    try:
        cfg = get_config()
        cfg.exibir_configuracao()
        print("✅ Configuração carregada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
