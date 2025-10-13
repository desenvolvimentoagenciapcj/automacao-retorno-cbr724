# -*- coding: utf-8 -*-
"""
BUSCAR TITULO COM NOSSO NUMERO 880
"""

import pyodbc

print("="*70)
print("BUSCA POR NOSSO NUMERO: 880")
print("="*70)

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Buscar por Nosso Numero exato
print("\n1. BUSCA EXATA - NR_NNR_TIT = '880':")
print("-"*70)
cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = '880'")
row = cursor.fetchone()

if row:
    cols = [column[0] for column in cursor.description]
    print("\n✓ Encontrado!")
    for i, col in enumerate(cols):
        if row[i]:
            print(f"  {col}: {row[i]}")
else:
    print("✗ Nao encontrado")

# Busca com zeros a esquerda
print("\n2. BUSCA COM ZEROS - NR_NNR_TIT = '0000000880':")
print("-"*70)
cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = '0000000880'")
row = cursor.fetchone()

if row:
    cols = [column[0] for column in cursor.description]
    print("\n✓ Encontrado!")
    for i, col in enumerate(cols):
        if row[i]:
            print(f"  {col}: {row[i]}")
else:
    print("✗ Nao encontrado")

# Busca parcial (LIKE)
print("\n3. BUSCA PARCIAL - NR_NNR_TIT LIKE '%880':")
print("-"*70)
cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT LIKE '%880'")
rows = cursor.fetchall()

if rows:
    print(f"\n✓ Encontrado {len(rows)} registro(s)!")
    print(f"\n{'Nosso Numero':<20} {'Data Pgto':>20} {'Valor':>15}")
    print("-"*70)
    
    cols = [column[0] for column in cursor.description]
    idx_nnr = cols.index('NR_NNR_TIT')
    idx_dt = cols.index('DT_PGTO_TIT')
    idx_vl = cols.index('VL_PGTO_TIT')
    
    for row in rows:
        dt = row[idx_dt] if row[idx_dt] else "N/A"
        vl = row[idx_vl] if row[idx_vl] else 0.0
        print(f"{row[idx_nnr]:<20} {str(dt):>20} R$ {vl:>10,.2f}")
        
    # Mostrar detalhes do primeiro
    print(f"\n{'='*70}")
    print("DETALHES DO PRIMEIRO REGISTRO ENCONTRADO:")
    print("="*70)
    for i, col in enumerate(cols):
        if rows[0][i]:
            print(f"  {col}: {rows[0][i]}")
else:
    print("✗ Nenhum registro encontrado")

# Busca em todos os Nosso Numero que terminam com 880
print("\n4. VERIFICAR ULTIMAS ATUALIZACOES:")
print("-"*70)
cursor.execute("""
    SELECT TOP 10 NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT
    FROM pcjTITULOS
    WHERE DT_PGTO_TIT >= #10/07/2025#
    ORDER BY DT_PGTO_TIT DESC
""")

print(f"\n{'Nosso Numero':<20} {'Data Pgto':>25} {'Valor':>15}")
print("-"*70)
for row in cursor.fetchall():
    dt = row[1] if row[1] else "N/A"
    vl = row[2] if row[2] else 0.0
    print(f"{row[0]:<20} {str(dt):>25} R$ {vl:>10,.2f}")

conn.close()
