#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscar títulos 1227008952, 1227008953, 1227008954 no banco
"""

import pyodbc

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

titulos_esperados = ['1227008952', '1227008953', '1227008954']

print("="*80)
print("BUSCANDO TÍTULOS SÉRIE 1227 NO BANCO")
print("="*80)

for nn in titulos_esperados:
    print(f"\n🔍 Buscando '{nn}'...")
    
    # Busca exata
    cursor.execute("SELECT NR_NNR_TIT, CD_SAC, DT_PGTO_TIT, VL_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", nn)
    result = cursor.fetchone()
    
    if result:
        print(f"  ✅ ENCONTRADO:")
        print(f"     NR_NNR_TIT: {result[0]}")
        print(f"     CD_SAC: {result[1]}")
        print(f"     DT_PGTO_TIT: {result[2]}")
        print(f"     VL_PGTO_TIT: R$ {result[3]}")
    else:
        # Busca parcial
        cursor.execute("SELECT NR_NNR_TIT, CD_SAC, DT_PGTO_TIT, VL_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT LIKE ?", f"%{nn[-4:]}")
        results = cursor.fetchall()
        
        if results:
            print(f"  ⚠️  Encontrados {len(results)} títulos terminando em '{nn[-4:]}':")
            for r in results:
                print(f"     - {r[0]} | CD_SAC: {r[1]} | DT_PGTO: {r[2]} | Valor: R$ {r[3]}")
        else:
            print(f"  ❌ NÃO ENCONTRADO")

cursor.close()
conn.close()

print("\n" + "="*80)
