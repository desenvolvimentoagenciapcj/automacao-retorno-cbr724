# -*- coding: utf-8 -*-
"""
VERIFICAR TITULO ESPECIFICO - ID 880
"""

import pyodbc

print("="*70)
print("BUSCA DETALHADA - TITULO ID 880")
print("="*70)

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 1. Buscar por ID
print("\n1. BUSCANDO POR ID = 880:")
print("-"*70)

try:
    cursor.execute("SELECT * FROM pcjTITULOS WHERE ID = 880")
    row = cursor.fetchone()
    
    if row:
        cols = [column[0] for column in cursor.description]
        print("\n✓ Registro encontrado!")
        print("\nTODOS OS CAMPOS:")
        print("-"*70)
        for i, col in enumerate(cols):
            valor = row[i]
            if valor is not None:
                print(f"{col:<30}: {valor}")
    else:
        print("✗ Nenhum registro encontrado com ID = 880")
except Exception as e:
    print(f"Erro: {e}")

# 2. Buscar registros proximos ao ID 880
print("\n2. REGISTROS PROXIMOS AO ID 880:")
print("-"*70)

try:
    cursor.execute("""
        SELECT TOP 5 ID, NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT
        FROM pcjTITULOS
        WHERE ID >= 875 AND ID <= 885
        ORDER BY ID
    """)
    
    print(f"\n{'ID':<10} {'Nosso Numero':<15} {'Data Pgto':>20} {'Valor':>15}")
    print("-"*70)
    for row in cursor.fetchall():
        dt_pgto = row[2] if row[2] else "N/A"
        vl_pgto = row[3] if row[3] else 0.0
        print(f"{row[0]:<10} {row[1]:<15} {str(dt_pgto):>20} R$ {vl_pgto:>10,.2f}")
        
except Exception as e:
    print(f"Erro: {e}")

# 3. Verificar se campo ID existe
print("\n3. ESTRUTURA DA TABELA:")
print("-"*70)

cursor.execute("SELECT * FROM pcjTITULOS WHERE 1=0")
cols = [column[0] for column in cursor.description]

print(f"Total de colunas: {len(cols)}\n")

# Procurar campo ID
if 'ID' in cols:
    print("✓ Campo 'ID' encontrado na tabela")
else:
    print("✗ Campo 'ID' NAO encontrado na tabela")
    print("\nCampos disponiveis:")
    for col in cols:
        print(f"  - {col}")

# 4. Ver qual é a chave primaria
print("\n4. VERIFICANDO CHAVE PRIMARIA:")
print("-"*70)

try:
    # Tentar identificar a chave primaria
    cursor.execute("SELECT TOP 1 * FROM pcjTITULOS")
    row = cursor.fetchone()
    cols = [column[0] for column in cursor.description]
    
    print("\nPrimeira linha da tabela:")
    for i, col in enumerate(cols):
        print(f"  {col}: {row[i]}")
        
except Exception as e:
    print(f"Erro: {e}")

conn.close()

print("\n" + "="*70)
print("IMPORTANTE:")
print("Se o campo 'ID' nao existe, precisamos usar outro campo como NR_NNR_TIT")
print("="*70)
