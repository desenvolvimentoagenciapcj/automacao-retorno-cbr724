# -*- coding: utf-8 -*-
"""
TESTAR PROCESSAMENTO DO ARQUIVO COM TÍTULO 880
"""

import sys
sys.path.insert(0, r'D:\Teste_Cobrança_Acess\AutomacaoRetorno')

from processador_cbr724 import ProcessadorCBR724
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s'
)

print("="*80)
print("TESTE DE PROCESSAMENTO - ARQUIVO COM TÍTULO 880")
print("="*80)

arquivo = r"D:\Teste_Cobrança_Acess\Retorno\CBR7246254310202521228_id.ret"

processador = ProcessadorCBR724()

print(f"\nProcessando: {arquivo}")
print("-"*80)

registros = processador.processar_arquivo(arquivo)

print(f"\n{'='*80}")
print(f"TOTAL DE REGISTROS PROCESSADOS: {len(registros)}")
print("="*80)

# Procurar o título 880
titulo_880 = None
for reg in registros:
    if reg['nosso_numero'] == '880':
        titulo_880 = reg
        break

if titulo_880:
    print("\n✓✓✓ TÍTULO 880 ENCONTRADO! ✓✓✓")
    print("-"*80)
    print(f"Tipo registro: {titulo_880['tipo_registro']}")
    print(f"Nosso Número: {titulo_880['nosso_numero']}")
    print(f"Nome Cliente: {titulo_880['nome_cliente']}")
    print(f"Valor Pago: R$ {titulo_880['valor_pago']:,.2f}")
    print(f"Data Vencimento: {titulo_880['data_vencimento']}")
    print(f"Código Ocorrência: {titulo_880['codigo_ocorrencia']}")
    print(f"Data Processamento: {titulo_880['data_ocorrencia']}")
else:
    print("\n✗ TÍTULO 880 NÃO ENCONTRADO")
    print("\nTítulos processados:")
    for reg in registros[:20]:
        print(f"  NN: {reg['nosso_numero']:>6} - {reg['nome_cliente'][:30]}")

print("\n" + "="*80)
print("ESTATÍSTICAS:")
print("-"*80)

# Contar por tipo
tipos = {}
for reg in registros:
    tipo = reg['tipo_registro']
    tipos[tipo] = tipos.get(tipo, 0) + 1

for tipo, count in tipos.items():
    print(f"  Tipo {tipo}: {count} registros")

# Total de valores
total_valor = sum(reg['valor_pago'] for reg in registros)
print(f"\nValor total: R$ {total_valor:,.2f}")

print("="*80)
