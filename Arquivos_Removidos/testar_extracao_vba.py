#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testar processador CBR724 com extração VBA correta
Nosso Número extraído da posição [11:21]
"""

import sys
sys.path.insert(0, '.')

from processador_cbr724 import ProcessadorCBR724
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

arquivo = r"d:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

print("="*80)
print("TESTE DO PROCESSADOR CBR724 - EXTRAÇÃO VBA FIEL")
print("="*80)

processador = ProcessadorCBR724()
registros = processador.processar_arquivo(arquivo)

print(f"\n📦 Total de registros extraídos: {len(registros)}")

if registros:
    print("\n" + "-"*80)
    print("TÍTULOS EXTRAÍDOS:")
    print("-"*80)
    
    for i, reg in enumerate(registros, 1):
        nn = reg.get('nosso_numero', '')
        cliente = reg.get('nome_cliente', '')
        valor = reg.get('valor_pago', 0.0)
        
        print(f"\n{i}. Nosso Número: {nn}")
        print(f"   Cliente: {cliente[:40]}")
        print(f"   Valor: R$ {valor:,.2f}")

print("\n" + "="*80)
