#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Notificações
Classe responsável por enviar notificações por email sobre o processamento
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Any

class Notificador:
    """Sistema de notificações por email"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configurações de email
        self.smtp_server = config['email']['servidor_smtp']
        self.smtp_port = config['email']['porta']
        self.usuario = config['email']['usuario']
        self.senha = config['email']['senha']
        self.destinatarios = config['email']['destinatarios']
    
    def enviar_sucesso(self, nome_arquivo: str, resultado: Dict[str, int]):
        """Envia notificação de processamento bem-sucedido"""
        if not self.config['email']['enviar_sucesso']:
            return
        
        try:
            assunto = f"✅ Arquivo de Retorno Processado com Sucesso - {nome_arquivo}"
            
            corpo = f"""
            <html>
            <body>
                <h2 style="color: #28a745;">Processamento Concluído com Sucesso</h2>
                
                <h3>Informações do Arquivo:</h3>
                <ul>
                    <li><strong>Nome do Arquivo:</strong> {nome_arquivo}</li>
                    <li><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</li>
                </ul>
                
                <h3>Resultados do Processamento:</h3>
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px;"><strong>Registros Processados</strong></td>
                        <td style="padding: 8px;">{resultado.get('total_processados', 0)}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;"><strong>Baixas Realizadas</strong></td>
                        <td style="padding: 8px; color: #28a745;"><strong>{resultado.get('baixas', 0)}</strong></td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px;"><strong>Atualizações</strong></td>
                        <td style="padding: 8px;">{resultado.get('atualizacoes', 0)}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;"><strong>Duplicatas Ignoradas</strong></td>
                        <td style="padding: 8px;">{resultado.get('duplicatas', 0)}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px;"><strong>Erros</strong></td>
                        <td style="padding: 8px; color: #dc3545;">{resultado.get('erros', 0)}</td>
                    </tr>
                </table>
                
                <p style="margin-top: 20px; font-size: 12px; color: #6c757d;">
                    Esta é uma mensagem automática do Sistema de Automação de Retorno Bancário.
                </p>
            </body>
            </html>
            """
            
            self._enviar_email(assunto, corpo, html=True)
            self.logger.info(f"Notificação de sucesso enviada para: {', '.join(self.destinatarios)}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de sucesso: {e}")
    
    def enviar_erro(self, nome_arquivo: str, erro: str):
        """Envia notificação de erro no processamento"""
        if not self.config['email']['enviar_erro']:
            return
        
        try:
            assunto = f"❌ ERRO no Processamento de Retorno - {nome_arquivo}"
            
            corpo = f"""
            <html>
            <body>
                <h2 style="color: #dc3545;">Erro no Processamento</h2>
                
                <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px;">
                    <h3>⚠️ ATENÇÃO: Arquivo não foi processado!</h3>
                </div>
                
                <h3>Informações do Erro:</h3>
                <ul>
                    <li><strong>Nome do Arquivo:</strong> {nome_arquivo}</li>
                    <li><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</li>
                    <li><strong>Erro:</strong> {erro}</li>
                </ul>
                
                <h3>Ações Necessárias:</h3>
                <ol>
                    <li>Verificar o arquivo na pasta de erro</li>
                    <li>Analisar o log detalhado do sistema</li>
                    <li>Corrigir o problema e reprocessar o arquivo</li>
                    <li>Contatar o suporte se necessário</li>
                </ol>
                
                <p style="margin-top: 20px; font-size: 12px; color: #6c757d;">
                    Esta é uma mensagem automática do Sistema de Automação de Retorno Bancário.
                </p>
            </body>
            </html>
            """
            
            self._enviar_email(assunto, corpo, html=True)
            self.logger.info(f"Notificação de erro enviada para: {', '.join(self.destinatarios)}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de erro: {e}")
    
    def enviar_relatorio_diario(self, estatisticas: Dict[str, Any]):
        """Envia relatório diário de atividades"""
        if not self.config['email']['enviar_relatorio_diario']:
            return
        
        try:
            data_hoje = datetime.now().strftime('%d/%m/%Y')
            assunto = f"📊 Relatório Diário - Retorno Bancário - {data_hoje}"
            
            total_arquivos = estatisticas.get('total_arquivos', 0)
            total_registros = estatisticas.get('total_registros', 0)
            total_baixas = estatisticas.get('total_baixas', 0)
            total_erros = estatisticas.get('total_erros', 0)
            
            # Cor do status baseada nos resultados
            if total_erros == 0:
                cor_status = "#28a745"  # Verde
                status = "✅ Todos os arquivos processados com sucesso"
            elif total_erros < total_arquivos:
                cor_status = "#ffc107"  # Amarelo
                status = "⚠️ Alguns arquivos com erro"
            else:
                cor_status = "#dc3545"  # Vermelho
                status = "❌ Todos os arquivos com erro"
            
            corpo = f"""
            <html>
            <body>
                <h2>Relatório Diário - Sistema de Retorno Bancário</h2>
                <h3>Data: {data_hoje}</h3>
                
                <div style="background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <h3 style="color: {cor_status}; margin: 0;">{status}</h3>
                </div>
                
                <h3>Resumo do Dia:</h3>
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <tr style="background-color: #007bff; color: white;">
                        <td style="padding: 10px;"><strong>Métrica</strong></td>
                        <td style="padding: 10px;"><strong>Quantidade</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;">Arquivos Processados</td>
                        <td style="padding: 8px; text-align: center;"><strong>{total_arquivos}</strong></td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px;">Registros Processados</td>
                        <td style="padding: 8px; text-align: center;"><strong>{total_registros}</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;">Baixas Realizadas</td>
                        <td style="padding: 8px; text-align: center; color: #28a745;"><strong>{total_baixas}</strong></td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px;">Arquivos com Erro</td>
                        <td style="padding: 8px; text-align: center; color: #dc3545;"><strong>{total_erros}</strong></td>
                    </tr>
                </table>
                
                <h3>Detalhes por Arquivo:</h3>
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <tr style="background-color: #007bff; color: white;">
                        <td style="padding: 8px;"><strong>Arquivo</strong></td>
                        <td style="padding: 8px;"><strong>Horário</strong></td>
                        <td style="padding: 8px;"><strong>Status</strong></td>
                        <td style="padding: 8px;"><strong>Baixas</strong></td>
                    </tr>
            """
            
            # Adicionar detalhes dos arquivos
            for arquivo in estatisticas.get('arquivos', []):
                status_cor = "#28a745" if arquivo['status'] == 'Sucesso' else "#dc3545"
                corpo += f"""
                    <tr>
                        <td style="padding: 8px;">{arquivo['nome']}</td>
                        <td style="padding: 8px;">{arquivo['horario']}</td>
                        <td style="padding: 8px; color: {status_cor};"><strong>{arquivo['status']}</strong></td>
                        <td style="padding: 8px; text-align: center;">{arquivo.get('baixas', 0)}</td>
                    </tr>
                """
            
            corpo += """
                </table>
                
                <p style="margin-top: 20px; font-size: 12px; color: #6c757d;">
                    Esta é uma mensagem automática do Sistema de Automação de Retorno Bancário.<br>
                    Relatório gerado automaticamente às 18:00.
                </p>
            </body>
            </html>
            """
            
            self._enviar_email(assunto, corpo, html=True)
            self.logger.info(f"Relatório diário enviado para: {', '.join(self.destinatarios)}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar relatório diário: {e}")
    
    def _enviar_email(self, assunto: str, corpo: str, html: bool = False):
        """Envia email usando SMTP"""
        try:
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = self.usuario
            msg['To'] = ', '.join(self.destinatarios)
            msg['Subject'] = assunto
            
            # Adicionar corpo
            if html:
                msg.attach(MIMEText(corpo, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            
            # Conectar ao servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.usuario, self.senha)
                
                # Enviar email
                text = msg.as_string()
                server.sendmail(self.usuario, self.destinatarios, text)
            
            self.logger.debug(f"Email enviado com sucesso: {assunto}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar email: {e}")
            raise
    
    def testar_configuracao(self) -> bool:
        """Testa configuração de email"""
        try:
            assunto = "🔧 Teste de Configuração - Sistema de Retorno"
            corpo = f"""
            <html>
            <body>
                <h2>Teste de Configuração</h2>
                <p>Se você recebeu este email, a configuração está funcionando corretamente!</p>
                <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                
                <h3>Configurações Testadas:</h3>
                <ul>
                    <li>Servidor SMTP: {self.smtp_server}:{self.smtp_port}</li>
                    <li>Usuário: {self.usuario}</li>
                    <li>Destinatários: {len(self.destinatarios)} configurados</li>
                </ul>
                
                <p style="color: #28a745;"><strong>✅ Sistema de notificações funcionando corretamente!</strong></p>
            </body>
            </html>
            """
            
            self._enviar_email(assunto, corpo, html=True)
            return True
            
        except Exception as e:
            self.logger.error(f"Erro no teste de configuração: {e}")
            return False