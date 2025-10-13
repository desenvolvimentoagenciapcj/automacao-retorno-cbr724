# ============================================================================
# Watchdog do Monitor - Monitora se o monitor caiu e reinicia automaticamente
# ============================================================================

import time
import subprocess
import psutil
from datetime import datetime
from pathlib import Path
import sys

# Adicionar diretório do script ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from notificador_windows import NotificadorWindows
    NOTIFICACAO_DISPONIVEL = True
except:
    NOTIFICACAO_DISPONIVEL = False
    print("Sistema de notificações não disponível (opcional)")

class WatchdogMonitor:
    """Monitora o monitor de retornos e reinicia se cair"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.bat_iniciar = self.script_dir / "INICIAR_MONITOR_OCULTO.bat"
        self.intervalo_verificacao = 60  # Verifica a cada 60 segundos
        self.max_tentativas_restart = 3
        self.tentativas_consecutivas = 0
        
        if NOTIFICACAO_DISPONIVEL:
            self.notificador = NotificadorWindows()
        else:
            self.notificador = None
        
        # Arquivo de log do watchdog
        self.log_file = self.script_dir / "watchdog.log"
    
    def log(self, mensagem):
        """Registra mensagem no log do watchdog"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        linha = f"{timestamp} - {mensagem}\n"
        
        # Exibir no console
        print(linha.strip())
        
        # Salvar no arquivo (mantém últimas 1000 linhas)
        try:
            if self.log_file.exists():
                linhas = self.log_file.read_text(encoding='utf-8').split('\n')
                linhas = linhas[-999:]  # Manter últimas 999
            else:
                linhas = []
            
            linhas.append(linha.strip())
            self.log_file.write_text('\n'.join(linhas), encoding='utf-8')
        except:
            pass
    
    def monitor_esta_rodando(self):
        """Verifica se o monitor está rodando"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('monitor_retornos.py' in str(arg) for arg in cmdline):
                        return True, proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False, None
    
    def reiniciar_monitor(self):
        """Reinicia o monitor"""
        self.log("🔄 Tentando reiniciar monitor...")
        
        try:
            # Executar BAT de inicialização
            subprocess.run(
                [str(self.bat_iniciar)],
                cwd=str(self.script_dir),
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Aguardar 5 segundos para o monitor iniciar
            time.sleep(5)
            
            # Verificar se iniciou
            rodando, pid = self.monitor_esta_rodando()
            
            if rodando:
                self.log(f"✅ Monitor reiniciado com sucesso (PID: {pid})")
                self.tentativas_consecutivas = 0
                return True
            else:
                self.log("❌ Falha ao reiniciar monitor")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao reiniciar: {e}")
            return False
    
    def executar(self):
        """Loop principal do watchdog"""
        self.log("="*80)
        self.log("🐕 WATCHDOG DO MONITOR INICIADO")
        self.log("="*80)
        self.log(f"Intervalo de verificação: {self.intervalo_verificacao} segundos")
        self.log(f"Máximo de tentativas: {self.max_tentativas_restart}")
        self.log("="*80)
        
        verificacoes = 0
        
        try:
            while True:
                verificacoes += 1
                rodando, pid = self.monitor_esta_rodando()
                
                if rodando:
                    if verificacoes % 10 == 0:  # Log a cada 10 verificações (10 minutos)
                        self.log(f"✅ Monitor OK (PID: {pid}) - {verificacoes} verificações")
                    self.tentativas_consecutivas = 0
                else:
                    self.log("⚠️  MONITOR NÃO ESTÁ RODANDO!")
                    
                    # Notificar por e-mail
                    if self.notificador and self.tentativas_consecutivas == 0:
                        self.notificador.notificar_monitor_caiu()
                    
                    # Tentar reiniciar
                    if self.tentativas_consecutivas < self.max_tentativas_restart:
                        self.tentativas_consecutivas += 1
                        self.log(f"Tentativa {self.tentativas_consecutivas}/{self.max_tentativas_restart}")
                        
                        sucesso = self.reiniciar_monitor()
                        
                        if sucesso:
                            self.log("🎉 Monitor recuperado automaticamente!")
                            # Notificar sucesso
                            if self.notificador:
                                self.notificador.enviar(
                                    "✅ Monitor recuperado automaticamente",
                                    f"O watchdog detectou que o monitor caiu e reiniciou com sucesso.\n\nTentativa: {self.tentativas_consecutivas}/{self.max_tentativas_restart}",
                                    tipo='sucesso'
                                )
                        else:
                            self.log(f"❌ Falha na tentativa {self.tentativas_consecutivas}")
                    else:
                        self.log("🔴 MÁXIMO DE TENTATIVAS ATINGIDO!")
                        self.log("⚠️  INTERVENÇÃO MANUAL NECESSÁRIA")
                        
                        # Notificar falha crítica
                        if self.notificador:
                            self.notificador.enviar(
                                "🔴 CRÍTICO: Falha ao reiniciar monitor",
                                f"O watchdog tentou reiniciar o monitor {self.max_tentativas_restart} vezes sem sucesso.\n\nINTERVENÇÃO MANUAL NECESSÁRIA!",
                                tipo='erro'
                            )
                        
                        # Aguardar 5 minutos antes de tentar novamente
                        self.log("⏳ Aguardando 5 minutos antes de tentar novamente...")
                        time.sleep(300)
                        self.tentativas_consecutivas = 0
                
                # Aguardar próxima verificação
                time.sleep(self.intervalo_verificacao)
                
        except KeyboardInterrupt:
            self.log("")
            self.log("="*80)
            self.log("🛑 Watchdog encerrado pelo usuário")
            self.log("="*80)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("  WATCHDOG DO MONITOR DE RETORNOS")
    print("="*80)
    print("")
    print("  Este programa monitora se o monitor de retornos está rodando")
    print("  e reinicia automaticamente se detectar que ele caiu.")
    print("")
    print("  Pressione Ctrl+C para parar")
    print("")
    print("="*80 + "\n")
    
    watchdog = WatchdogMonitor()
    watchdog.executar()
