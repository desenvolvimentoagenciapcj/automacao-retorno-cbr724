#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO COMPLETO - Comparar processo manual vs automático

Por favor, execute o processo MANUAL no Access primeiro, depois rode este script.
"""

import pyodbc
from datetime import datetime

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

print("="*80)
print("DIAGNÓSTICO: PROCESSO MANUAL vs AUTOMÁTICO")
print("="*80)

print("""
ANTES DE RODAR ESTE SCRIPT:
1. Processe o arquivo CBR7246250110202521616_id.ret MANUALMENTE no Access
2. Anote em qual tela você verifica os dados
3. Anote qual filtro você usa para encontrar o título 8952

Depois pressione ENTER para continuar...
""")
input()

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Buscar título 1227008952 (que o Python processou)
print("\n" + "="*80)
print("TÍTULO 1227008952 - Processado pelo PYTHON:")
print("="*80)

cursor.execute("""
    SELECT CD_SAC, NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT, VL_NOM_TIT, 
           DT_VCM_TIT, CodMovimento, NR_SNR_TIT
    FROM pcjTITULOS
    WHERE NR_NNR_TIT = '1227008952'
""")

result = cursor.fetchone()

if result:
    print(f"""
CD_SAC (ID_PCJ): {result[0]}
NR_NNR_TIT: {result[1]}
DT_PGTO_TIT: {result[2]}
VL_PGTO_TIT: R$ {result[3]}
VL_NOM_TIT: R$ {result[4]}
DT_VCM_TIT: {result[5]}
CodMovimento: {result[6]}
NR_SNR_TIT: {result[7]}
""")

print("\n" + "-"*80)
print("PERGUNTAS:")
print("-"*80)
print("""
1. No processo MANUAL, este título aparece com qual CD_SAC (ID_PCJ)?
2. No processo MANUAL, a DT_PGTO_TIT é a data de hoje?
3. No processo MANUAL, o VL_PGTO_TIT é R$ 13.299,07?
4. Em qual TELA/ABA do Access você verifica esses dados?
5. Qual FILTRO você usa para encontrar esse título?
""")

print("\n" + "="*80)
print("BUSCAR TODOS OS TÍTULOS ATUALIZADOS HOJE:")
print("="*80)

hoje = datetime.now().date()
cursor.execute("""
    SELECT CD_SAC, NR_NNR_TIT, VL_PGTO_TIT, DT_PGTO_TIT
    FROM pcjTITULOS
    WHERE DATEVALUE(DT_PGTO_TIT) = ?
    ORDER BY DT_PGTO_TIT DESC
""", hoje)

titulos_hoje = cursor.fetchall()

print(f"\nEncontrados {len(titulos_hoje)} títulos com pagamento em {hoje}:")
print("-"*80)
for t in titulos_hoje[:20]:  # Primeiros 20
    print(f"ID_PCJ: {t[0]:5d} | NN: {t[1]:15s} | Valor: R$ {t[2]:>10.2f} | Data: {t[3]}")

print("\n" + "="*80)
print("COMPARAÇÃO:")
print("="*80)
print("""
Se o processo MANUAL criou títulos DIFERENTES dos listados acima,
então o VBA está fazendo algo que o Python não está fazendo.

Me diga:
1. Quantos títulos o processo MANUAL criou/atualizou?
2. Quais são os NR_NNR_TIT (Nosso Número) deles?
3. Eles aparecem na lista acima? SIM ou NÃO?
""")

cursor.close()
conn.close()

print("\n" + "="*80)
print("PRÓXIMO PASSO:")
print("="*80)
print("""
Com essas informações, vou descobrir a diferença exata entre
o processo manual (VBA) e o automático (Python).
""")
print("="*80)
