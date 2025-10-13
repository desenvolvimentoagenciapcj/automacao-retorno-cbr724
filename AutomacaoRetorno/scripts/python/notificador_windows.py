"""
Sistema de Notificações do Windows
Envia notificações visuais usando o sistema nativo do Windows 10/11
Autor: Sistema de Automação CBR724
Data: 2025-10-10
"""

import os
import sys
from pathlib import Path

try:
    from plyer import notification
    PLYER_DISPONIVEL = True
except ImportError:
    PLYER_DISPONIVEL = False
    print("⚠️ Biblioteca 'plyer' não instalada. Execute: pip install plyer")

import configparser


class NotificadorWindows:
    """Classe para enviar notificações do Windows"""
    
    def __init__(self):
        """Inicializa o notificador"""
        self.habilitado = True
        self.app_name = "Monitor CBR724"
        self.icon_path = None
        
        # Tenta carregar configurações do config.ini
        try:
            config = configparser.ConfigParser()
            config_path = Path(__file__).parent / 'config.ini'
            
            if config_path.exists():
                config.read(config_path, encoding='utf-8')
                
                # Verifica se notificações estão habilitadas
                if config.has_section('NOTIFICACOES'):
                    self.habilitado = config.getboolean('NOTIFICACOES', 'habilitado', fallback=True)
        except Exception as e:
            print(f"⚠️ Aviso ao carregar config: {e}")
            # Continua com valores padrão
    
    def enviar(self, titulo, mensagem, timeout=10, icone='info'):
        """
        Envia uma notificação do Windows
        
        Args:
            titulo (str): Título da notificação
            mensagem (str): Corpo da mensagem
            timeout (int): Tempo em segundos que a notificação fica visível (padrão: 10)
            icone (str): Tipo de ícone - 'info', 'sucesso', 'alerta', 'erro'
        
        Returns:
            bool: True se enviou com sucesso, False caso contrário
        """
        if not self.habilitado:
            return False
        
        if not PLYER_DISPONIVEL:
            print(f"⚠️ Notificação (plyer não disponível): {titulo} - {mensagem}")
            return False
        
        try:
            # Adiciona emoji baseado no tipo
            emojis = {
                'info': 'ℹ️',
                'sucesso': '✅',
                'alerta': '⚠️',
                'erro': '❌'
            }
            
            emoji = emojis.get(icone, 'ℹ️')
            titulo_completo = f"{emoji} {titulo}"
            
            # Envia a notificação
            notification.notify(
                title=titulo_completo,
                message=mensagem,
                app_name=self.app_name,
                timeout=timeout,
                app_icon=self.icon_path  # Pode ser None
            )
            
            return True
            
        except Exception as e:
            print(f"⚠️ Erro ao enviar notificação: {e}")
            return False
    
    def notificar_monitor_iniciado(self, pasta_monitorada):
        """Notifica que o monitor foi iniciado"""
        mensagem = f"Monitorando:\n{pasta_monitorada}"
        return self.enviar(
            titulo="Monitor Iniciado",
            mensagem=mensagem,
            timeout=5,
            icone='info'
        )
    
    def notificar_processamento_sucesso(self, arquivo, titulos_criados=0, titulos_pagos=0, titulos_cancelados=0):
        """Notifica processamento bem-sucedido"""
        mensagem = f"Arquivo: {arquivo}\n"
        mensagem += f"✅ Criados: {titulos_criados}\n"
        mensagem += f"💰 Pagos: {titulos_pagos}\n"
        
        if titulos_cancelados > 0:
            mensagem += f"❌ Cancelados: {titulos_cancelados}"
        
        return self.enviar(
            titulo="Arquivo Processado",
            mensagem=mensagem,
            timeout=8,
            icone='sucesso'
        )
    
    def notificar_processamento_erro(self, arquivo, erro):
        """Notifica erro no processamento"""
        mensagem = f"Arquivo: {arquivo}\n"
        mensagem += f"Erro: {str(erro)[:100]}"  # Limita tamanho
        
        return self.enviar(
            titulo="Erro no Processamento",
            mensagem=mensagem,
            timeout=15,
            icone='erro'
        )
    
    def notificar_arquivo_detectado(self, arquivo):
        """Notifica que um novo arquivo foi detectado"""
        mensagem = f"Processando:\n{arquivo}"
        
        return self.enviar(
            titulo="Novo Arquivo Detectado",
            mensagem=mensagem,
            timeout=5,
            icone='info'
        )
    
    def notificar_arquivo_iedcbr_excluido(self, arquivo):
        """Notifica que um arquivo IEDCBR foi excluído"""
        mensagem = f"Arquivo IEDCBR excluído:\n{arquivo}"
        
        return self.enviar(
            titulo="IEDCBR Excluído",
            mensagem=mensagem,
            timeout=5,
            icone='alerta'
        )
    
    def notificar_monitor_parado(self, motivo="Manual"):
        """Notifica que o monitor foi parado"""
        mensagem = f"Motivo: {motivo}"
        
        return self.enviar(
            titulo="Monitor Parado",
            mensagem=mensagem,
            timeout=5,
            icone='alerta'
        )
    
    def notificar_monitor_caiu(self):
        """Notifica que o monitor caiu (alerta crítico)"""
        mensagem = "O monitor parou de funcionar!\nTentando reiniciar automaticamente..."
        
        return self.enviar(
            titulo="ALERTA: Monitor Caiu",
            mensagem=mensagem,
            timeout=20,
            icone='erro'
        )
    
    def notificar_monitor_caiu_reiniciando(self):
        """Notifica que o monitor caiu e está tentando reiniciar"""
        mensagem = "Monitor não está rodando!\n🔄 Tentando reiniciar automaticamente..."
        
        return self.enviar(
            titulo="⚠️ Monitor Caiu",
            mensagem=mensagem,
            timeout=15,
            icone='alerta'
        )
    
    def notificar_monitor_reiniciado(self, pid=None):
        """Notifica que o monitor foi reiniciado com sucesso"""
        mensagem = "Monitor reiniciado com sucesso!"
        if pid:
            mensagem += f"\nPID: {pid}"
        
        return self.enviar(
            titulo="Monitor Reiniciado",
            mensagem=mensagem,
            timeout=8,
            icone='sucesso'
        )
    
    def notificar_erro_critico(self, titulo, mensagem):
        """Notifica um erro crítico"""
        return self.enviar(
            titulo=f"🚨 {titulo}",
            mensagem=mensagem,
            timeout=30,
            icone='erro'
        )
    
    def notificar_falha_reiniciar(self, tentativas):
        """Notifica falha ao reiniciar após múltiplas tentativas"""
        mensagem = f"Falha após {tentativas} tentativas.\n"
        mensagem += "AÇÃO NECESSÁRIA: Verificar manualmente!"
        
        return self.enviar(
            titulo="CRÍTICO: Falha ao Reiniciar",
            mensagem=mensagem,
            timeout=30,
            icone='erro'
        )


# Teste do módulo
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" TESTE DO SISTEMA DE NOTIFICAÇÕES DO WINDOWS")
    print("="*60 + "\n")
    
    if not PLYER_DISPONIVEL:
        print("❌ Biblioteca 'plyer' não está instalada!")
        print("\n📦 Para instalar, execute:")
        print("   pip install plyer\n")
        sys.exit(1)
    
    notificador = NotificadorWindows()
    
    print("📢 Enviando notificação de teste...")
    print("   (Deve aparecer no canto inferior direito da tela)\n")
    
    sucesso = notificador.enviar(
        titulo="Teste de Notificação",
        mensagem="Sistema de notificações funcionando!\nSe você viu isso, está tudo OK! ✅",
        timeout=10,
        icone='sucesso'
    )
    
    if sucesso:
        print("✅ Notificação enviada com sucesso!")
        print("   Verifique o canto da tela (área de notificações)\n")
        
        # Testa outros tipos
        import time
        
        print("📢 Testando notificação de processamento...")
        time.sleep(2)
        notificador.notificar_processamento_sucesso(
            arquivo="CBR724_TESTE.ret",
            titulos_criados=45,
            titulos_pagos=23,
            titulos_cancelados=2
        )
        
        print("✅ Teste completo!\n")
    else:
        print("❌ Falha ao enviar notificação!")
        print("   Verifique se a biblioteca 'plyer' está instalada.\n")
    
    print("="*60 + "\n")
