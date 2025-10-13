#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar se títulos tipo RG foram salvos no banco
"""

import pyodbc
from datetime import datetime

# Conectar ao banco
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("="*80)
print("VERIFICANDO TÍTULOS DO ARQUIVO NO BANCO")
print("="*80)

# Títulos RG (devem estar salvos mas SEM data de pagamento)
titulos_rg = ['8952', '8953', '8954']

# Títulos LQB (devem estar salvos COM data de pagamento)
titulos_lqb = ['500002487', '500002517', '500002586', '500003689', 
                '500005726', '500007974', '8951']

print("\n📌 TÍTULOS TIPO RG (problemas com data?):")
print("-"*80)
for nn in titulos_rg:
    cursor.execute("""
        SELECT NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT, DT_VCM_TIT
        FROM pcjTITULOS
        WHERE NR_NNR_TIT LIKE ?
        ORDER BY NR_NNR_TIT DESC
    """, f"%{nn}")
    
    result = cursor.fetchone()
    if result:
        dt_pgto = result[1]
        vl_pgto = result[2]
        dt_vcm = result[3]
        
        # Formatar data sem hora
        if dt_pgto:
            if isinstance(dt_pgto, datetime):
                dt_pgto_str = dt_pgto.strftime('%d/%m/%Y %H:%M:%S')
                dt_pgto_data = dt_pgto.date()
            else:
                dt_pgto_str = str(dt_pgto)
                dt_pgto_data = dt_pgto
        else:
            dt_pgto_str = "NÃO PAGO"
            dt_pgto_data = None
            
        print(f"\n  NN {nn} → {result[0]}")
        print(f"    DT_PGTO_TIT: {dt_pgto_str}")
        print(f"    DT_PGTO (só data): {dt_pgto_data}")
        print(f"    VL_PGTO_TIT: R$ {vl_pgto if vl_pgto else 0.00}")
        print(f"    DT_VCM_TIT: {dt_vcm}")
    else:
        print(f"\n  ❌ NN {nn} não encontrado")

print("\n\n📌 TÍTULOS TIPO LQB (devem ter data COM hora):")
print("-"*80)
for nn in titulos_lqb[:3]:  # Só 3 exemplos
    cursor.execute("""
        SELECT NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT
        FROM pcjTITULOS
        WHERE NR_NNR_TIT LIKE ?
        ORDER BY NR_NNR_TIT DESC
    """, f"%{nn}")
    
    result = cursor.fetchone()
    if result:
        dt_pgto = result[1]
        vl_pgto = result[2]
        
        if dt_pgto and isinstance(dt_pgto, datetime):
            dt_pgto_str = dt_pgto.strftime('%d/%m/%Y %H:%M:%S')
            dt_pgto_data = dt_pgto.date()
        else:
            dt_pgto_str = str(dt_pgto) if dt_pgto else "NÃO PAGO"
            dt_pgto_data = None
            
        print(f"\n  NN {nn} → {result[0]}")
        print(f"    DT_PGTO_TIT (com hora): {dt_pgto_str}")
        print(f"    DT_PGTO (só data): {dt_pgto_data}")
        print(f"    VL_PGTO_TIT: R$ {vl_pgto if vl_pgto else 0.00}")

cursor.close()
conn.close()

print("\n" + "="*80)
print("CONCLUSÃO:")
print("="*80)
print("""
Se os títulos RG estão salvos COM HORA, precisamos modificar o integrador
para salvar apenas a DATA (sem hora, minuto, segundo).

Solução: Usar apenas a data no campo DT_PGTO_TIT
  ANTES: datetime.now()  → '2025-10-08 10:33:41'
  DEPOIS: datetime.now().date()  → '2025-10-08'
""")
print("="*80)
