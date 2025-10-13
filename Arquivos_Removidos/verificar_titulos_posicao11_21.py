#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar se os títulos '500002487', '500002517', etc existem no banco
Esses são os Nosso Números extraídos da posição [11:21]
"""

import pyodbc

# Nosso Números extraídos do campo [11:21]
nosso_numeros = [
    '500002487',
    '500002517',
    '500002586',
    '500003689',
    '500005726',
    '500007974'
]

# Conectar ao banco
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("="*80)
print("VERIFICANDO TÍTULOS EXTRAÍDOS DA POSIÇÃO [11:21] (DENTRO DO CÓDIGO BANCO)")
print("="*80)

encontrados = 0
nao_encontrados = 0

for nn in nosso_numeros:
    print(f"\nBuscando '{nn}'...")
    
    # Busca exata
    cursor.execute("SELECT NR_NNR_TIT, CD_SAC, VL_PGTO_TIT, DT_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", nn)
    result = cursor.fetchone()
    
    if result:
        print(f"  ✅ ENCONTRADO: {result[0]} | CD_SAC: {result[1]} | Valor: R$ {result[2]}")
        encontrados += 1
    else:
        # Busca parcial
        cursor.execute("SELECT NR_NNR_TIT, CD_SAC, VL_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT LIKE ?", f"%{nn}")
        result = cursor.fetchone()
        
        if result:
            print(f"  ⚠️  ENCONTRADO (parcial): {result[0]} | CD_SAC: {result[1]} | Valor: R$ {result[2]}")
            encontrados += 1
        else:
            # Buscar só os últimos 4 dígitos
            ultimos_4 = nn[-4:]
            cursor.execute("SELECT NR_NNR_TIT, CD_SAC, VL_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT LIKE ?", f"%{ultimos_4}")
            results = cursor.fetchall()
            
            if results:
                print(f"  ⚠️  Encontrados {len(results)} título(s) terminando em '{ultimos_4}':")
                for r in results[:3]:  # Mostrar até 3
                    print(f"     - {r[0]} | CD_SAC: {r[1]} | Valor: R$ {r[2]}")
                encontrados += len(results)
            else:
                print(f"  ❌ NÃO ENCONTRADO")
                nao_encontrados += 1

cursor.close()
conn.close()

print("\n" + "="*80)
print(f"RESUMO: {encontrados} encontrados, {nao_encontrados} não encontrados")
print("="*80)
