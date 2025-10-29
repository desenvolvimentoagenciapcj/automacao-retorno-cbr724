"""
Módulo de Notificação por E-mail
=================================

Envia notificações por e-mail sobre o processamento de arquivos de retorno.

Funcionalidades:
- Envia e-mails quando arquivos são processados com sucesso
- Envia alertas quando ocorrem erros
- Envia relatórios diários com resumo de processamento
- Suporta múltiplos destinatários

Configuração:
- Configure os parâmetros SMTP no config.ini seção [EMAIL]
- Use "Senha de App" do Google Workspace, não a senha normal
- Adicione os destinatários separados por vírgula

Autor: Sistema de Automação CBR724
Data: 13/10/2025
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import sys

# Adiciona o diretório do projeto ao path para importar config_manager
script_dir = Path(__file__).parent
projeto_dir = script_dir.parent.parent
sys.path.insert(0, str(projeto_dir / 'scripts' / 'python'))

from config_manager import Config

logger = logging.getLogger(__name__)


class NotificadorEmail:
    """Classe para enviar notificações por e-mail"""
    
    def __init__(self):
        """Inicializa o notificador com as configurações do config.ini"""
        self.config = Config()
        self.habilitado = self.config.config.get('EMAIL', 'habilitado', fallback='false').lower() == 'true'
        
        if self.habilitado:
            self.smtp_servidor = self.config.config.get('EMAIL', 'smtp_servidor')
            self.smtp_porta = int(self.config.config.get('EMAIL', 'smtp_porta', fallback='587'))
            self.remetente = self.config.config.get('EMAIL', 'remetente')
            self.senha = self.config.config.get('EMAIL', 'senha')
            
            # Converte destinatários de string para lista
            dest_str = self.config.config.get('EMAIL', 'destinatarios', fallback='')
            self.destinatarios = [email.strip() for email in dest_str.split(',') if email.strip()]
            
            logger.info(f"📧 Notificador de e-mail inicializado")
            logger.info(f"   Remetente: {self.remetente}")
            logger.info(f"   Destinatários: {', '.join(self.destinatarios)}")
        else:
            logger.info("📧 Notificações por e-mail desabilitadas no config.ini")
    
    def _criar_mensagem(self, assunto: str, corpo_html: str, destinatarios: list = None) -> MIMEMultipart:
        """
        Cria uma mensagem de e-mail formatada
        
        Args:
            assunto: Assunto do e-mail
            corpo_html: Corpo do e-mail em HTML
            destinatarios: Lista de destinatários (se None, usa self.destinatarios)
            
        Returns:
            Mensagem MIME pronta para envio
        """
        if destinatarios is None:
            destinatarios = self.destinatarios
        
        mensagem = MIMEMultipart('alternative')
        mensagem['Subject'] = assunto
        mensagem['From'] = self.remetente
        mensagem['To'] = ', '.join(destinatarios)
        
        # Versão texto simples (fallback)
        texto = corpo_html.replace('<br>', '\n').replace('</p>', '\n').replace('<p>', '')
        texto = texto.replace('<strong>', '').replace('</strong>', '')
        texto = texto.replace('<ul>', '').replace('</ul>', '').replace('<li>', '• ').replace('</li>', '\n')
        
        parte_texto = MIMEText(texto, 'plain', 'utf-8')
        parte_html = MIMEText(corpo_html, 'html', 'utf-8')
        
        mensagem.attach(parte_texto)
        mensagem.attach(parte_html)
        
        return mensagem
    
    def _enviar(self, mensagem: MIMEMultipart) -> bool:
        """
        Envia a mensagem via SMTP
        
        Args:
            mensagem: Mensagem MIME a ser enviada
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            with smtplib.SMTP(self.smtp_servidor, self.smtp_porta) as servidor:
                servidor.starttls()  # Ativa criptografia TLS
                servidor.login(self.remetente, self.senha)
                servidor.send_message(mensagem)
            
            logger.info(f"✅ E-mail enviado: {mensagem['Subject']}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ Erro de autenticação SMTP - Verifique remetente/senha no config.ini")
            logger.error("   💡 Dica: Use 'Senha de App' do Google Workspace, não a senha normal")
            return False
            
        except smtplib.SMTPException as e:
            logger.error(f"❌ Erro SMTP ao enviar e-mail: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao enviar e-mail: {e}")
            return False
    
    def notificar_sucesso(self, arquivo: str, registros_processados: int = 0) -> bool:
        """
        Envia notificação de sucesso no processamento
        
        Args:
            arquivo: Nome do arquivo processado
            registros_processados: Número de registros processados (opcional)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        assunto = f"✅ Arquivo Processado com Sucesso - {arquivo}"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #28a745; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .info {{ background-color: white; padding: 15px; border-left: 4px solid #28a745; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>✅ Processamento Concluído com Sucesso</h2>
                </div>
                <div class="content">
                    <p><strong>Arquivo processado:</strong></p>
                    <div class="info">
                        <p>📄 <strong>{arquivo}</strong></p>
                        <p>🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                        {f'<p>📊 Registros processados: {registros_processados}</p>' if registros_processados > 0 else ''}
                    </div>
                    <p>O arquivo foi importado para o banco de dados e movido para a pasta de processados.</p>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        return self._enviar(mensagem)
    
    def notificar_erro(self, arquivo: str, erro: str) -> bool:
        """
        Envia notificação de erro no processamento
        
        Args:
            arquivo: Nome do arquivo que causou erro
            erro: Descrição do erro
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        assunto = f"❌ ERRO ao Processar Arquivo - {arquivo}"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc3545; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .error {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #dc3545; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>❌ Erro no Processamento</h2>
                </div>
                <div class="content">
                    <p><strong>Arquivo com erro:</strong></p>
                    <div class="error">
                        <p>📄 <strong>{arquivo}</strong></p>
                        <p>🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                        <p>⚠️ <strong>Erro:</strong> {erro}</p>
                    </div>
                    <p><strong>Ação necessária:</strong></p>
                    <ul>
                        <li>Verificar o arquivo na pasta de erros</li>
                        <li>Analisar o log do sistema para mais detalhes</li>
                        <li>Corrigir o problema e reprocessar manualmente</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        return self._enviar(mensagem)
    
    def notificar_monitor_iniciado(self) -> bool:
        """
        Envia notificação quando o monitor é iniciado
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        assunto = "🚀 Monitor de Retornos Iniciado"
        
        pasta_monitorada = self.config.pasta_retorno
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .info {{ background-color: white; padding: 15px; border-left: 4px solid #007bff; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🚀 Monitor Iniciado</h2>
                </div>
                <div class="content">
                    <p>O sistema de monitoramento de retornos foi iniciado com sucesso.</p>
                    <div class="info">
                        <p>📂 <strong>Pasta monitorada:</strong><br>{pasta_monitorada}</p>
                        <p>🕐 <strong>Iniciado em:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    </div>
                    <p>O sistema está aguardando novos arquivos .ret para processar automaticamente.</p>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        return self._enviar(mensagem)
    
    def enviar_relatorio_diario(self, arquivos_processados: int, arquivos_erro: int, 
                                detalhes_sucesso: list = None, detalhes_erro: list = None) -> bool:
        """
        Envia relatório diário de processamento
        
        Args:
            arquivos_processados: Número de arquivos processados com sucesso
            arquivos_erro: Número de arquivos com erro
            detalhes_sucesso: Lista de nomes dos arquivos processados (opcional)
            detalhes_erro: Lista de tuplas (arquivo, erro) com erros (opcional)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        assunto = f"📊 Relatório Diário - {data_hoje}"
        
        # Monta lista de sucessos
        lista_sucessos = ""
        if detalhes_sucesso:
            lista_sucessos = "<ul>"
            for arquivo in detalhes_sucesso:
                lista_sucessos += f"<li>✅ {arquivo}</li>"
            lista_sucessos += "</ul>"
        
        # Monta lista de erros
        lista_erros = ""
        if detalhes_erro:
            lista_erros = "<ul>"
            for arquivo, erro in detalhes_erro:
                lista_erros += f"<li>❌ {arquivo}<br><small>{erro}</small></li>"
            lista_erros += "</ul>"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #6c757d; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background-color: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; margin: 0 5px; }}
                .stat-number {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .detalhes {{ background-color: white; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📊 Relatório Diário de Processamento</h2>
                    <p>{data_hoje}</p>
                </div>
                <div class="content">
                    <div class="stats">
                        <div class="stat-box">
                            <p>Processados</p>
                            <div class="stat-number success">{arquivos_processados}</div>
                        </div>
                        <div class="stat-box">
                            <p>Com Erro</p>
                            <div class="stat-number error">{arquivos_erro}</div>
                        </div>
                    </div>
                    
                    {f'<div class="detalhes"><h3>✅ Arquivos Processados</h3>{lista_sucessos}</div>' if lista_sucessos else ''}
                    {f'<div class="detalhes"><h3>❌ Arquivos com Erro</h3>{lista_erros}</div>' if lista_erros else ''}
                    
                    <p style="margin-top: 20px;">
                        <strong>Total de arquivos:</strong> {arquivos_processados + arquivos_erro}<br>
                        <strong>Taxa de sucesso:</strong> {(arquivos_processados / (arquivos_processados + arquivos_erro) * 100) if (arquivos_processados + arquivos_erro) > 0 else 0:.1f}%
                    </p>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        return self._enviar(mensagem)
    
    def notificar_id_nao_encontrado(self, arquivo: str, nosso_numero: str, 
                                    numero_linha: int) -> bool:
        """
        Notifica quando um nosso_número NÃO é encontrado em ids.json
        
        Args:
            arquivo: Nome do arquivo sendo processado
            nosso_numero: Nosso número que não foi encontrado
            numero_linha: Número da linha onde ocorreu
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        assunto = f"⚠️  ID Não Mapeado - {arquivo}"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff9800; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .warning {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #ff9800; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>⚠️  ID Não Encontrado em ids.json</h2>
                </div>
                <div class="content">
                    <p><strong>Aviso:</strong> Um nosso_número não foi encontrado no arquivo de mapeamento de IDs.</p>
                    <div class="warning">
                        <p><strong>Arquivo:</strong> {arquivo}</p>
                        <p><strong>Linha:</strong> {numero_linha}</p>
                        <p><strong>Nosso Número:</strong> {nosso_numero}</p>
                        <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    </div>
                    <p><strong>O que aconteceu?</strong></p>
                    <ul>
                        <li>O sistema processou o arquivo normalmente</li>
                        <li>Mas não encontrou o ID correspondente para este nosso_número</li>
                        <li>O campo de empresa foi deixado SEM o ID</li>
                    </ul>
                    <p><strong>Ação recomendada:</strong></p>
                    <ul>
                        <li>Verifique se o nosso_número está correto</li>
                        <li>Atualize o arquivo ids.json se necessário</li>
                        <li>Reprocesse o arquivo se precisar adicionar o ID</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        return self._enviar(mensagem)
    
    def notificar_sem_arquivos(self, destinatarios_adicionais: list = None) -> bool:
        """
        Notifica quando nenhum arquivo foi recebido até 08:30
        
        Args:
            destinatarios_adicionais: Lista de emails adicionais para receber notificação
                                      Exemplo: ['aline.briques@agencia.baciaspcj.org.br', 'lilian.cruz@agencia.baciaspcj.org.br']
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        # Se não fornecer destinatários adicionais, usa os padrão
        destinatarios = self.destinatarios.copy()
        if destinatarios_adicionais:
            destinatarios.extend(destinatarios_adicionais)
        
        assunto = "⚠️  Nenhum Arquivo Recebido - Verificação 08:30"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ffc107; color: #333; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .alert {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0; }}
                .info {{ background-color: #e7f3ff; padding: 15px; border-left: 4px solid #2196F3; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>⚠️  Nenhum Arquivo Recebido</h2>
                </div>
                <div class="content">
                    <p>A verificação agendada de 08:30 detectou que <strong>nenhum arquivo de retorno foi recebido</strong> na pasta de entrada.</p>
                    <div class="alert">
                        <p><strong>Horário da Verificação:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                        <p><strong>Pasta Monitorada:</strong> \\Retorno</p>
                        <p><strong>Status:</strong> ❌ Nenhum arquivo CBR724*.ret encontrado</p>
                    </div>
                    <p><strong>O que fazer?</strong></p>
                    <ul>
                        <li>✅ Verifique se os arquivos de retorno foram enviados para a pasta correta</li>
                        <li>✅ Confirme se não há problemas na origem dos arquivos</li>
                        <li>✅ Se houver arquivos, copie-os para a pasta \\Retorno</li>
                        <li>✅ O monitor processará automaticamente assim que os arquivos chegarem</li>
                    </ul>
                    <div class="info">
                        <p><strong>💡 Dica:</strong> Se isso foi intencional (nenhum retorno no dia), pode ignorar este aviso.</p>
                    </div>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html, destinatarios)
        return self._enviar(mensagem)

    def testar_configuracao(self) -> bool:
        """
        Testa a configuração de e-mail enviando um e-mail de teste
        
        Returns:
            True se o teste foi bem-sucedido, False caso contrário
        """
        if not self.habilitado:
            print("⚠️  Notificações por e-mail estão desabilitadas no config.ini")
            return False
        
        print(f"\n📧 Testando configuração de e-mail...")
        print(f"   Servidor: {self.smtp_servidor}:{self.smtp_porta}")
        print(f"   Remetente: {self.remetente}")
        print(f"   Destinatários: {', '.join(self.destinatarios)}")
        
        assunto = "✅ Teste de Configuração - Sistema de Retornos"
        
        corpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #17a2b8; color: white; padding: 15px; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .info {{ background-color: white; padding: 15px; border-left: 4px solid #17a2b8; margin: 10px 0; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>✅ E-mail de Teste</h2>
                </div>
                <div class="content">
                    <p>Parabéns! A configuração de e-mail está funcionando corretamente.</p>
                    <div class="info">
                        <p><strong>Configurações:</strong></p>
                        <p>📧 Servidor SMTP: {self.smtp_servidor}:{self.smtp_porta}</p>
                        <p>👤 Remetente: {self.remetente}</p>
                        <p>🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    </div>
                    <p>Você receberá notificações sobre:</p>
                    <ul>
                        <li>✅ Arquivos processados com sucesso</li>
                        <li>❌ Erros no processamento</li>
                        <li>🚀 Início do monitoramento</li>
                        <li>📊 Relatórios diários (opcional)</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>Sistema de Automação de Retornos CBR724<br>
                    Agência das Bacias PCJ</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mensagem = self._criar_mensagem(assunto, corpo_html)
        resultado = self._enviar(mensagem)
        
        if resultado:
            print("\n✅ E-mail de teste enviado com sucesso!")
            print("   Verifique sua caixa de entrada.")
        else:
            print("\n❌ Falha ao enviar e-mail de teste.")
            print("   Verifique as configurações no config.ini")
        
        return resultado


# Função de teste quando executar o script diretamente
if __name__ == "__main__":
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*60)
    print("  TESTE DE NOTIFICAÇÃO POR E-MAIL")
    print("="*60 + "\n")
    
    notificador = NotificadorEmail()
    
    if notificador.habilitado:
        print("\nEscolha o tipo de teste:")
        print("1 - Enviar e-mail de teste de configuração")
        print("2 - Simular notificação de sucesso")
        print("3 - Simular notificação de erro")
        print("4 - Simular relatório diário")
        print("0 - Sair")
        
        escolha = input("\nOpção: ").strip()
        
        if escolha == "1":
            notificador.testar_configuracao()
        
        elif escolha == "2":
            print("\n📤 Enviando notificação de sucesso...")
            resultado = notificador.notificar_sucesso(
                arquivo="CBR7241234510202512345.ret",
                registros_processados=150
            )
            if resultado:
                print("✅ Notificação enviada!")
        
        elif escolha == "3":
            print("\n📤 Enviando notificação de erro...")
            resultado = notificador.notificar_erro(
                arquivo="CBR7241234510202512345.ret",
                erro="Arquivo corrompido ou formato inválido"
            )
            if resultado:
                print("✅ Notificação enviada!")
        
        elif escolha == "4":
            print("\n📤 Enviando relatório diário...")
            resultado = notificador.enviar_relatorio_diario(
                arquivos_processados=25,
                arquivos_erro=2,
                detalhes_sucesso=["arquivo1.ret", "arquivo2.ret", "arquivo3.ret"],
                detalhes_erro=[("arquivo_erro1.ret", "Formato inválido"), ("arquivo_erro2.ret", "Banco não encontrado")]
            )
            if resultado:
                print("✅ Relatório enviado!")
        
        elif escolha == "0":
            print("\n👋 Até logo!")
        
        else:
            print("\n⚠️  Opção inválida!")
    else:
        print("\n⚠️  Configure o e-mail no config.ini primeiro!")
        print("\nPassos:")
        print("1. Edite config/config.ini")
        print("2. Na seção [EMAIL], altere 'habilitado = true'")
        print("3. Configure smtp_servidor, smtp_porta, remetente")
        print("4. Gere uma 'Senha de App' no Google Workspace")
        print("5. Configure a senha e os destinatários")
