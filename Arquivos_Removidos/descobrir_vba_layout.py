#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descobrir como o VBA extrai o Nosso Número
Análise das linhas com '0000000000' na posição [21:31]
"""

arquivo = r"d:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = [l.rstrip('\n\r') for l in f if l.startswith(' 7') and len(l.rstrip('\n\r')) == 160]

print("="*100)
print("DESCOBRINDO O PADRÃO VBA - LINHAS COM NOSSO NÚMERO ZERADO")
print("="*100)

# Analisar linhas que têm '0000000000' na posição [21:31]
linhas_zeradas = [l for l in linhas if l[21:31].strip() == '0000000000']

print(f"\nEncontradas {len(linhas_zeradas)} linhas com Nosso Número zerado na posição [21:31]\n")

for i, linha in enumerate(linhas_zeradas, 1):
    print(f"LINHA #{i}:")
    print("-"*100)
    
    # Mostrar segmentos
    print(f"[0:3]    Tipo:           '{linha[0:3]}'")
    print(f"[3:21]   Código Banco:   '{linha[3:21]}'")
    print(f"[21:31]  Nosso Número?:  '{linha[21:31]}' ← ZERADO")
    print(f"[31:64]  Nome Cliente:   '{linha[31:64]}'")
    print(f"[65:73]  Data:           '{linha[65:73]}'")
    
    # HIPÓTESE VBA: O Nosso Número pode estar DENTRO do campo [3:21]
    codigo_banco = linha[3:21]
    print(f"\nANÁLISE DO CAMPO [3:21]: '{codigo_banco}'")
    print(f"  [3:11]  (8 chars):  '{codigo_banco[0:8]}'  ← Possível CNPJ")
    print(f"  [11:21] (10 chars): '{codigo_banco[8:18]}'  ← Possível Nosso Número")
    print(f"  [16:21] (5 chars):  '{codigo_banco[13:18]}'  ← Últimos 5 dígitos (2487, 2517, etc)")
    
    # Extrair valor do final da linha
    import re
    valor_match = re.search(r'(\d{1,10}\.?\d{0,3},\d{2})', linha[87:])
    valor = valor_match.group(1) if valor_match else '?'
    print(f"\n  Valor: R$ {valor}")
    print()

# Comparar com linhas que TÊM Nosso Número válido
print("="*100)
print("COMPARAÇÃO COM LINHAS VÁLIDAS (Nosso Número NÃO zerado)")
print("="*100)

linhas_validas = [l for l in linhas if l[21:31].strip() != '0000000000'][:3]

for i, linha in enumerate(linhas_validas, 1):
    print(f"\nLINHA VÁLIDA #{i}:")
    print("-"*100)
    
    codigo_banco = linha[3:21]
    nosso_numero = linha[21:31]
    nome_cliente = linha[31:64]
    
    print(f"[3:21]   Código Banco:   '{codigo_banco}'")
    print(f"  [3:11]  (8 chars):  '{codigo_banco[0:8]}'  ← CNPJ?")
    print(f"  [11:21] (10 chars): '{codigo_banco[8:18]}'  ← Coincide com Nosso Número?")
    print(f"[21:31]  Nosso Número:   '{nosso_numero}' ← VÁLIDO")
    print(f"[31:64]  Nome Cliente:   '{nome_cliente}'")
    
    # Comparar se [11:21] == [21:31]
    campo_codigo = codigo_banco[8:18].strip()
    campo_nosso = nosso_numero.strip()
    
    if campo_codigo == campo_nosso:
        print(f"\n  ✅ MATCH! Código[11:21] == NossoNum[21:31]: '{campo_codigo}'")
    else:
        print(f"\n  ❌ DIFERENTE:")
        print(f"     Código[11:21]:  '{campo_codigo}'")
        print(f"     NossoNum[21:31]: '{campo_nosso}'")

print("\n" + "="*100)
print("CONCLUSÃO:")
print("="*100)
print("""
Se as linhas com Nosso Número zerado [21:31]='0000000000' têm valores válidos
no campo [16:21] (últimos 5 dígitos do código banco), então:

HIPÓTESE: O VBA pode estar usando DUAS posições diferentes:
  - Se [21:31] != '0000000000': usar [21:31]
  - Se [21:31] == '0000000000': usar [16:21] ou [11:21]

OU o VBA sempre usa [11:21] dentro do código banco.
""")
print("="*100)
