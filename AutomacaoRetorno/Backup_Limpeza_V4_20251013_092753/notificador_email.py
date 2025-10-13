# ============================================================================
# Sistema de Notificações por E-mail
# ============================================================================
# Envia e-mails sobre eventos importantes do sistema

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import configparser
from pathlib import Path

class NotificadorEmail:
    """Envia notificações por e-mail sobre eventos do sistema"""
    
    def __init__(self):
        """Carrega configurações de e-mail do config.ini"""
        config_path = Path(__file__).parent / 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        # Configurações de e-mail (se existirem)
        if config.has_section('EMAIL'):
            self.habilitado = config.getboolean('EMAIL', 'habilitado', fallback=False)
            self.smtp_servidor = config.get('EMAIL', 'smtp_servidor', fallback='smtp.gmail.com')
            self.smtp_porta = config.getint('EMAIL', 'smtp_porta', fallback=587)
            self.remetente = config.get('EMAIL', 'remetente', fallback='')
            self.senha = config.get('EMAIL', 'senha', fallback='')
            self.destinatarios = config.get('EMAIL', 'destinatarios', fallback='').split(',')
            self.destinatarios = [email.strip() for email in self.destinatarios if email.strip()]
        else:
            self.habilitado = False
            
    def enviar(self, assunto, mensagem, tipo='info'):
        """
        Envia e-mail de notificação
        
        Args:
            assunto: Assunto do e-mail
            mensagem: Corpo da mensagem
            tipo: 'sucesso', 'erro', 'alerta', 'info'
        """
        if not self.habilitado:
            return False
            
        if not self.remetente or not self.senha or not self.destinatarios:
            return False
            
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.remetente
            msg['To'] = ', '.join(self.destinatarios)
            msg['Subject'] = f"[{tipo.upper()}] {assunto}"
            
            # Corpo do e-mail em HTML
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: {'#d4edda' if tipo == 'sucesso' else '#f8d7da' if tipo == 'erro' else '#fff3cd' if tipo == 'alerta' else '#d1ecf1'}; 
                            padding: 20px; border-radius: 5px; border-left: 5px solid {'#28a745' if tipo == 'sucesso' else '#dc3545' if tipo == 'erro' else '#ffc107' if tipo == 'alerta' else '#17a2b8'};">
                    <h2 style="color: {'#155724' if tipo == 'sucesso' else '#721c24' if tipo == 'erro' else '#856404' if tipo == 'alerta' else '#0c5460'};">
                        {assunto}
                    </h2>
                    <hr>
                    <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; background-color: #f8f9fa; padding: 15px; border-radius: 3px;">
{mensagem}
                    </pre>
                    <hr>
                    <p style="color: #6c757d; font-size: 12px;">
                        <strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br>
                        <strong>Sistema:</strong> Monitor Automático de Retornos CBR724
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            # Conectar e enviar
            server = smtplib.SMTP(self.smtp_servidor, self.smtp_porta)
            server.starttls()
            server.login(self.remetente, self.senha)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False
    
    def notificar_processamento_sucesso(self, arquivo, titulos_criados, titulos_pagos, titulos_cancelados):
        """Notifica processamento bem-sucedido"""
        mensagem = f"""
Arquivo: {arquivo}
Status: PROCESSADO COM SUCESSO

Resumo:
- Títulos criados: {titulos_criados}
- Títulos pagos: {titulos_pagos}
- Títulos cancelados: {titulos_cancelados}
- Total processado: {titulos_criados + titulos_pagos + titulos_cancelados}

O arquivo foi movido para a pasta de processados.
        """
        self.enviar(
            f"✅ Arquivo processado: {arquivo}",
            mensagem.strip(),
            tipo='sucesso'
        )
    
    def notificar_processamento_erro(self, arquivo, erro):
        """Notifica erro no processamento"""
        mensagem = f"""
Arquivo: {arquivo}
Status: ERRO NO PROCESSAMENTO

Erro:
{erro}

O arquivo foi movido para a pasta de erros.
AÇÃO NECESSÁRIA: Verificar o arquivo manualmente.
        """
        self.enviar(
            f"❌ Erro ao processar: {arquivo}",
            mensagem.strip(),
            tipo='erro'
        )
    
    def notificar_monitor_iniciado(self):
        """Notifica que o monitor foi iniciado"""
        mensagem = """
O monitor de retornos foi iniciado com sucesso.

Status: AGUARDANDO ARQUIVOS
Pasta monitorada: \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno

O sistema está rodando em segundo plano e processará
automaticamente qualquer arquivo .ret que for detectado.
        """
        self.enviar(
            "🚀 Monitor de retornos iniciado",
            mensagem.strip(),
            tipo='info'
        )
    
    def notificar_monitor_parado(self, motivo='Manual'):
        """Notifica que o monitor foi parado"""
        mensagem = f"""
O monitor de retornos foi PARADO.

Motivo: {motivo}

ATENÇÃO: Arquivos .ret não serão mais processados automaticamente
até que o monitor seja reiniciado.

Para reiniciar: Execute INICIAR_MONITOR_OCULTO.bat
        """
        self.enviar(
            "⚠️ Monitor de retornos parado",
            mensagem.strip(),
            tipo='alerta'
        )
    
    def notificar_monitor_caiu(self):
        """Notifica que o monitor caiu inesperadamente"""
        mensagem = """
O monitor de retornos CAIU inesperadamente!

Status: MONITOR NÃO ESTÁ RODANDO

AÇÃO URGENTE NECESSÁRIA:
1. Verificar logs em: monitor_retornos.log
2. Reiniciar monitor: INICIAR_MONITOR_OCULTO.bat

Enquanto o monitor estiver parado, arquivos .ret não serão processados.
        """
        self.enviar(
            "🔴 ALERTA: Monitor caiu!",
            mensagem.strip(),
            tipo='erro'
        )


# Função auxiliar para testar
if __name__ == "__main__":
    print("Testando sistema de notificações...")
    notificador = NotificadorEmail()
    
    if notificador.habilitado:
        print(f"E-mail habilitado: {notificador.remetente} → {notificador.destinatarios}")
        # notificador.notificar_monitor_iniciado()
        print("Teste concluído (descomente a linha acima para enviar e-mail de teste)")
    else:
        print("E-mail não configurado. Adicione seção [EMAIL] no config.ini")
