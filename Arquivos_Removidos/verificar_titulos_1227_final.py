#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar títulos 1227008952, 1227008953, 1227008954
Esses são os títulos RG que foram processados
"""

import pyodbc

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

titulos = ['1227008952', '1227008953', '1227008954', '1227008951']

print("="*80)
print("VERIFICANDO TÍTULOS SÉRIE 1227 (TIPO RG)")
print("="*80)

for nn in titulos:
    cursor.execute("""
        SELECT NR_NNR_TIT, CD_SAC, DT_PGTO_TIT, VL_PGTO_TIT, DT_VCM_TIT
        FROM pcjTITULOS
        WHERE NR_NNR_TIT = ?
    """, nn)
    
    result = cursor.fetchone()
    
    if result:
        print(f"\n✅ Título: {result[0]}")
        print(f"   CD_SAC (ID_PCJ): {result[1]}")
        print(f"   DT_PGTO_TIT: {result[2]}")
        print(f"   VL_PGTO_TIT: R$ {result[3]}")
        print(f"   DT_VCM_TIT: {result[4]}")
    else:
        print(f"\n❌ Título {nn} não encontrado")

print("\n" + "="*80)
print("RESUMO:")
print("="*80)
print("""
Os títulos 1227008952, 1227008953, 1227008954 foram processados.

No Access, para ver esses títulos você deve filtrar por:
  - ID_PCJ (CD_SAC) = 2525 (para 8952 e 8953)
  - ID_PCJ (CD_SAC) = 2528 (para 8954)
  - ID_PCJ (CD_SAC) = 2525 (para 8951)

NÃO filtrar por ID_PCJ = 411, pois esse é o código que aparece no
arquivo de retorno, mas NÃO é o CD_SAC real no banco!
""")
print("="*80)

cursor.close()
conn.close()
