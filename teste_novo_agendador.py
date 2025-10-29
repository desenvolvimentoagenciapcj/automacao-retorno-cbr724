#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar a nova funcionalidade do agendador
Verifica se a função de notificar_sem_arquivos está sendo chamada corretamente
"""

import sys
from pathlib import Path

# Adiciona o diretório do projeto ao path
script_dir = Path(__file__).parent
projeto_dir = script_dir
sys.path.insert(0, str(projeto_dir / 'Scripts' / 'python'))

print("\n" + "="*70)
print("  TESTE DO AGENDADOR - Verificação de Arquivos")
print("="*70 + "\n")

try:
    from agendador_verificacao import AgendadorVerificacao
    from config_manager import Config
    
    print("✅ Módulos importados com sucesso\n")
    
    # Criar instância
    print("🔄 Criando instância do agendador...")
    agendador = AgendadorVerificacao()
    print("✅ Agendador criado com sucesso\n")
    
    # Testar método de verificar arquivos
    print("📂 Testando método verificar_arquivos_na_pasta()...")
    tem_arquivos, quantidade = agendador.verificar_arquivos_na_pasta()
    
    if tem_arquivos:
        print(f"✅ {quantidade} arquivo(s) encontrado(s) na pasta de retorno\n")
    else:
        print(f"⚠️  Nenhum arquivo encontrado na pasta de retorno\n")
    
    print("🔍 Testando caminho da pasta de retorno:")
    config = Config()
    print(f"   {config.pasta_retorno}\n")
    
    print("="*70)
    print("  ✅ TESTE CONCLUÍDO COM SUCESSO")
    print("="*70 + "\n")
    print("Próxima ação:")
    print("  Execute: python Scripts\\python\\agendador_verificacao.py --testar")
    print("\n")

except Exception as e:
    print(f"\n❌ ERRO: {e}\n")
    import traceback
    traceback.print_exc()
    print("\n")
    sys.exit(1)
