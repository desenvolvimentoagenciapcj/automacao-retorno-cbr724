# -*- coding: utf-8 -*-
"""
ANALISAR LAYOUT REAL DOS ARQUIVOS CBR724
"""

import re

arquivo = r"D:\Teste_Cobrança_Acess\Retorno\CBR7246254310202521228_id.ret"

print("="*100)
print("ANÁLISE DO LAYOUT REAL - ARQUIVO CBR724")
print("="*100)

with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = f.readlines()

print(f"\nTotal de linhas: {len(linhas)}")

# Contar tipos de registro
tipos = {}
for linha in linhas:
    if len(linha.strip()) > 0:
        tipo = linha[0:2]
        tipos[tipo] = tipos.get(tipo, 0) + 1

print("\nTIPOS DE REGISTRO ENCONTRADOS:")
print("-"*50)
for tipo, count in sorted(tipos.items()):
    print(f"  '{tipo}': {count} linhas")

# Analisar linha 159 em detalhes (MD PAPEIS - 880)
print("\n" + "="*100)
print("LINHA 159 - MD PAPEIS (ID 880) - ANÁLISE DETALHADA")
print("="*100)

linha_159 = linhas[158]  # índice 158 = linha 159
print(f"\nLinha completa ({len(linha_159.rstrip())} chars):")
print(linha_159.rstrip())
print("\n" + "-"*100)

# Mostrar posições de 10 em 10
print("\nPOSIÇÕES DE 10 EM 10:")
for i in range(0, min(160, len(linha_159)), 10):
    conteudo = linha_159[i:i+10]
    print(f"[{i:3d}-{i+9:3d}]: '{conteudo}'")

# Identificar campos
print("\n" + "="*100)
print("IDENTIFICAÇÃO DE CAMPOS:")
print("="*100)

linha = linha_159.rstrip()
print(f"\n[0-2]   Tipo registro: '{linha[0:2]}'")
print(f"[3-20]  Código banco: '{linha[3:21]}'")
print(f"[21-32] Campo 1: '{linha[21:33]}'")
print(f"[33-37] Campo 2: '{linha[33:38]}' ← Possível Nosso Número")
print(f"[38-65] Nome: '{linha[38:66]}'")
print(f"[66-74] Data: '{linha[66:74]}'")
print(f"[75-90] Campo: '{linha[75:91]}'")

# Procurar o 880
print("\n" + "="*100)
print("BUSCANDO O NÚMERO 880:")
print("="*100)

for match in re.finditer(r'\b880\b', linha):
    pos = match.start()
    print(f"  Posição {pos}: '{linha[pos-5:pos+10]}'")

# Extrair valores monetários
print("\n" + "="*100)
print("VALORES MONETÁRIOS:")
print("="*100)

for match in re.finditer(r'(\d{1,10}\.?\d{0,3},\d{2})', linha):
    valor = match.group()
    pos = match.start()
    print(f"  Posição {pos}: {valor}")

# Analisar TODAS as linhas tipo 37
print("\n" + "="*100)
print("TODAS AS LINHAS TIPO 37 (primeiras 10):")
print("="*100)

print(f"\n{'Linha':<8} {'Código':<20} {'Campo1':<15} {'NN?':<8} {'Nome':<30}")
print("-"*100)

count = 0
for i, linha in enumerate(linhas, 1):
    linha = linha.rstrip()
    if linha.startswith('37') and len(linha) >= 65:
        tipo = linha[0:2]
        codigo = linha[3:21]
        campo1 = linha[21:33]
        nn = linha[33:38].strip()
        nome = linha[38:66].strip()
        
        print(f"{i:<8} {codigo:<20} {campo1:<15} {nn:<8} {nome:<30}")
        
        count += 1
        if count >= 15:
            break

print(f"\n✓ Total de linhas tipo 37: {tipos.get('37', 0)}")

print("\n" + "="*100)
print("CONCLUSÃO:")
print("="*100)
print("O layout REAL é diferente do manual:")
print("  - Tipo registro: '37' (2 chars, não ' 7' com 3 chars)")
print("  - Nosso Número: posição [33-37] (não [21-30])")
print("  - Tamanho da linha pode variar")
print("="*100)
