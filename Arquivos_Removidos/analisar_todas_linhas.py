#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise COMPLETA de todas as linhas tipo ' 7' do arquivo
Verifica quais títulos existem no banco de dados
"""

import pyodbc
import re

# Arquivo de teste
arquivo = r"d:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

print("\n" + "="*80)
print("ANÁLISE COMPLETA - TODAS AS LINHAS TIPO ' 7'")
print("="*80)

# Ler arquivo e extrair todas as linhas tipo ' 7'
with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = [l.rstrip('\n\r') for l in f if l.startswith(' 7') and len(l.rstrip('\n\r')) == 160]

print(f"\n📄 Total de linhas tipo ' 7' encontradas: {len(linhas)}")

# Conectar ao banco Access
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("\n" + "-"*80)
print("ANÁLISE LINHA POR LINHA:")
print("-"*80)

titulos_processados = []
titulos_nao_encontrados = []

for i, linha in enumerate(linhas, 1):
    # Extrair Nosso Número (posição 21-30)
    nosso_numero_raw = linha[21:31].strip()
    nosso_numero = nosso_numero_raw.lstrip('0') if nosso_numero_raw else ''
    
    # Extrair nome cliente
    nome_cliente = linha[31:64].strip()
    
    # Extrair valor
    resto = linha[87:]
    valor_match = re.search(r'(\d{1,10}\.?\d{0,3},\d{2})', resto)
    valor_str = valor_match.group(1) if valor_match else '0,00'
    
    print(f"\n#{i} - Linha do arquivo:")
    print(f"   Nosso Número RAW: '{nosso_numero_raw}'")
    print(f"   Nosso Número (sem zeros): '{nosso_numero}'")
    print(f"   Cliente: {nome_cliente}")
    print(f"   Valor: R$ {valor_str}")
    
    # Verificar se é numérico válido
    if not nosso_numero or not nosso_numero.isdigit():
        print(f"   ❌ REJEITADO: Nosso Número inválido")
        titulos_nao_encontrados.append({
            'nn': nosso_numero_raw,
            'motivo': 'Nosso Número inválido'
        })
        continue
    
    # Buscar no banco Access (busca parcial)
    try:
        cursor.execute("""
            SELECT NR_NNR_TIT, CD_SAC, DT_VCM_TIT, DT_PGTO_TIT, VL_PGTO_TIT
            FROM pcjTITULOS
            WHERE NR_NNR_TIT LIKE ?
        """, f"%{nosso_numero}%")
        
        result = cursor.fetchone()
        
        if result:
            print(f"   ✅ ENCONTRADO no banco:")
            print(f"      NR_NNR_TIT: {result[0]}")
            print(f"      CD_SAC: {result[1]}")
            print(f"      DT_VCM_TIT: {result[2]}")
            print(f"      DT_PGTO_TIT: {result[3]}")
            print(f"      VL_PGTO_TIT: {result[4]}")
            titulos_processados.append({
                'nn': nosso_numero,
                'nr_nnr_tit': result[0],
                'cd_sac': result[1]
            })
        else:
            print(f"   ❌ NÃO ENCONTRADO no banco")
            titulos_nao_encontrados.append({
                'nn': nosso_numero,
                'motivo': 'Título não existe na base de dados'
            })
            
    except Exception as e:
        print(f"   ❌ ERRO ao consultar: {e}")
        titulos_nao_encontrados.append({
            'nn': nosso_numero,
            'motivo': f'Erro: {e}'
        })

cursor.close()
conn.close()

# Resumo final
print("\n" + "="*80)
print("RESUMO FINAL:")
print("="*80)
print(f"\n✅ Títulos que PODEM ser processados: {len(titulos_processados)}")
for t in titulos_processados:
    print(f"   - NN {t['nn']} → {t['nr_nnr_tit']} (CD_SAC: {t['cd_sac']})")

print(f"\n❌ Títulos que NÃO podem ser processados: {len(titulos_nao_encontrados)}")
for t in titulos_nao_encontrados:
    print(f"   - NN '{t['nn']}' → {t['motivo']}")

print(f"\n📊 Taxa de sucesso: {len(titulos_processados)}/{len(linhas)} = {100*len(titulos_processados)/len(linhas):.1f}%")
print("="*80 + "\n")
