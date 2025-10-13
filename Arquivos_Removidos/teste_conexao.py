#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido de conexão com banco Access
"""

import yaml
import logging
from integrador_access import IntegradorAccess

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("\n🔧 TESTANDO CONEXÃO COM BANCOS ACCESS...\n")

# Carregar config
with open('config.yaml', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print(f"📁 Banco Baixa: {config['bancos']['baixa']['caminho']}")
print(f"⚙️  Cobranca Ativo: {config['bancos']['cobranca'].get('ativo', True)}\n")

# Testar integrador
integrador = IntegradorAccess(config)

if integrador.conectar():
    print("\n✅ CONEXÃO BEM-SUCEDIDA!")
    print(f"   - dbBaixa2025: {'Conectado' if integrador.conn_baixa else 'Não conectado'}")
    print(f"   - Cobranca2019: {'Conectado' if integrador.conn_cobranca else 'Desabilitado'}")
    
    # Testar backup
    print("\n📦 Testando backup...")
    backups = integrador.fazer_backup()
    print(f"✓ {len(backups)} backup(s) criado(s)")
    
    integrador.desconectar()
    print("\n✅ Teste concluído com sucesso!\n")
else:
    print("\n❌ ERRO AO CONECTAR!\n")
