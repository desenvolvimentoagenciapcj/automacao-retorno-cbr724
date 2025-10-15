#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Notificação de Erro no Boot
Envia email quando sistema não inicia após reinicialização do Windows
"""

import sys
from pathlib import Path

# Adiciona path do projeto
script_dir = Path(__file__).parent
projeto_dir = script_dir.parent.parent
sys.path.insert(0, str(projeto_dir / 'scripts' / 'python'))

try:
    from notificador_email import NotificadorEmail
    from datetime import datetime
    
    notificador = NotificadorEmail()
    
    if notificador.habilitado:
        notificador.notificar_erro(
            "🚨 Monitor NÃO Iniciou Após Reinicialização",
            f"""ATENÇÃO: O monitor não iniciou automaticamente após reinicialização do Windows!

⏰ Horário do Problema: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

❌ STATUS: Monitor NÃO está rodando

🔄 TENTATIVAS AUTOMÁTICAS:
   • Sistema tentou iniciar automaticamente após boot (2 min)
   • Sistema tentou recuperar após 10 minutos
   • Ambas as tentativas falharam

⚠️  AÇÃO URGENTE NECESSÁRIA:
1. Fazer login na máquina
2. Executar manualmente: .\\INICIAR.bat
3. Verificar logs em: logs\\boot_check.log
4. Verificar se servidor está acessível
5. Executar: .\\STATUS.bat

📁 Pasta do Projeto:
   {projeto_dir}

🔍 POSSÍVEIS CAUSAS:
   • Servidor ainda não estava acessível 10 min após boot
   • Problema de rede/conectividade
   • Credenciais de acesso expiradas
   • Erro no script de inicialização

Arquivos de retorno NÃO estão sendo processados até o monitor ser iniciado manualmente!"""
        )
        print("Email de alerta enviado com sucesso")
    else:
        print("Email desabilitado - notificação não enviada")
        
except Exception as e:
    print(f"Erro ao enviar email: {e}")
    sys.exit(1)
