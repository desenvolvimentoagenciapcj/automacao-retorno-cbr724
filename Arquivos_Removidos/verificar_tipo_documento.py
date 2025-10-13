#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar diferença entre linhas RG e LQB
"""

arquivo = r"d:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = [l.rstrip('\n\r') for l in f if l.startswith(' 7') and len(l.rstrip('\n\r')) == 160]

print("="*100)
print("ANÁLISE: DIFERENÇA ENTRE LINHAS RG vs LQB")
print("="*100)

linhas_rg = []
linhas_lqb = []

for linha in linhas:
    # Tipo documento está na posição [83:87]
    tipo_doc = linha[83:87].strip()
    
    if 'RG' in tipo_doc:
        linhas_rg.append(linha)
    elif 'LQB' in tipo_doc:
        linhas_lqb.append(linha)

print(f"\n📌 Linhas tipo RG: {len(linhas_rg)}")
print(f"📌 Linhas tipo LQB: {len(linhas_lqb)}")

print("\n" + "="*100)
print("EXEMPLO LINHA RG:")
print("="*100)
if linhas_rg:
    linha = linhas_rg[0]
    print(f"\nLinha completa:\n{linha}\n")
    print(f"[0:3]    Tipo:        '{linha[0:3]}'")
    print(f"[11:21]  Nosso Num:   '{linha[11:21]}' → sem zeros: '{linha[11:21].strip().lstrip('0')}'")
    print(f"[31:64]  Cliente:     '{linha[31:64]}'")
    print(f"[65:73]  Data Venc:   '{linha[65:73]}'")
    print(f"[73:83]  Campo 73-83: '{linha[73:83]}'")
    print(f"[83:87]  Tipo Doc:    '{linha[83:87]}'")
    print(f"[87:160] Resto:       '{linha[87:120]}...'")

print("\n" + "="*100)
print("EXEMPLO LINHA LQB:")
print("="*100)
if linhas_lqb:
    linha = linhas_lqb[0]
    print(f"\nLinha completa:\n{linha}\n")
    print(f"[0:3]    Tipo:        '{linha[0:3]}'")
    print(f"[11:21]  Nosso Num:   '{linha[11:21]}' → sem zeros: '{linha[11:21].strip().lstrip('0')}'")
    print(f"[31:64]  Cliente:     '{linha[31:64]}'")
    print(f"[65:73]  Data Venc:   '{linha[65:73]}'")
    print(f"[73:83]  Campo 73-83: '{linha[73:83]}'")
    print(f"[83:87]  Tipo Doc:    '{linha[83:87]}'")
    print(f"[87:160] Resto:       '{linha[87:120]}...'")

print("\n" + "="*100)
print("COMPARAÇÃO DATA VENCIMENTO:")
print("="*100)

print("\nLinhas RG:")
for i, linha in enumerate(linhas_rg[:3], 1):
    data_venc = linha[65:73]
    print(f"  {i}. '{data_venc}' (tamanho: {len(data_venc.strip())})")

print("\nLinhas LQB:")
for i, linha in enumerate(linhas_lqb[:3], 1):
    data_venc = linha[65:73]
    print(f"  {i}. '{data_venc}' (tamanho: {len(data_venc.strip())})")

print("\n" + "="*100)
