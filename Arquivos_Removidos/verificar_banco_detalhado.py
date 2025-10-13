# -*- coding: utf-8 -*-
"""
VERIFICACAO DETALHADA - O que realmente foi gravado no banco?
"""

import pyodbc
from datetime import datetime

print("="*70)
print("VERIFICACAO DETALHADA DO BANCO - dbBaixa2025")
print("="*70)

# Conectar ao banco
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 1. Ver estrutura da tabela
print("\n1. ESTRUTURA DA TABELA pcjTITULOS:")
print("-"*70)
cursor.execute("SELECT * FROM pcjTITULOS WHERE 1=0")
columns = [column[0] for column in cursor.description]
print(f"Total de colunas: {len(columns)}")
print("\nColunas relacionadas a pagamento/retorno:")
for col in columns:
    if any(x in col.upper() for x in ['PGTO', 'RET', 'BAIXA', 'LIB', 'CRED', 'DT_']):
        print(f"  - {col}")

# 2. Verificar ultimas atualizacoes
print("\n2. ULTIMOS REGISTROS MODIFICADOS:")
print("-"*70)

# Tentar diferentes campos de data
campos_data = ['DT_PGTO_TIT', 'DT_LIB_CRED', 'DT_RETORNO', 'DT_BAIXA']
encontrou = False

for campo in campos_data:
    try:
        cursor.execute(f"""
            SELECT TOP 5
                NR_NNR_TIT,
                VL_PGTO_TIT,
                {campo}
            FROM pcjTITULOS
            WHERE {campo} IS NOT NULL
            ORDER BY {campo} DESC
        """)
        
        rows = cursor.fetchall()
        if rows:
            print(f"\nCampo: {campo}")
            print(f"{'Nosso Numero':<15} {'Valor':>15} {'Data':>20}")
            print("-"*70)
            for row in rows:
                print(f"{row[0]:<15} R$ {row[1] if row[1] else 0:>12,.2f} {row[2]}")
            encontrou = True
            break
    except Exception as e:
        continue

if not encontrou:
    print("Nenhum campo de data encontrado com valores!")

# 3. Buscar por Nosso Numero especifico que foi processado
print("\n3. VERIFICAR TITULOS PROCESSADOS RECENTEMENTE:")
print("-"*70)

# Pegar um nosso numero dos logs
nossos_numeros = ['1227008952', '1227008953', '1227008954', '1227006535']

for nn in nossos_numeros:
    cursor.execute(f"""
        SELECT *
        FROM pcjTITULOS
        WHERE NR_NNR_TIT = '{nn}'
    """)
    
    row = cursor.fetchone()
    if row:
        print(f"\n✓ Encontrado: {nn}")
        # Mostrar campos importantes
        cols = [column[0] for column in cursor.description]
        for i, col in enumerate(cols):
            valor = row[i]
            if valor is not None and any(x in col.upper() for x in ['PGTO', 'RET', 'BAIXA', 'LIB', 'CRED', 'VL_', 'DT_']):
                print(f"  {col:<30}: {valor}")
        break
    else:
        print(f"✗ NAO encontrado: {nn}")

# 4. Verificar se campo de arquivo retorno existe
print("\n4. CAMPOS RELACIONADOS A ARQUIVO RETORNO:")
print("-"*70)
campos_ret = [col for col in columns if 'RET' in col.upper() or 'ARQ' in col.upper()]
if campos_ret:
    for col in campos_ret:
        print(f"  - {col}")
else:
    print("  Nenhum campo encontrado relacionado a arquivo retorno")

# 5. Contar registros com DT_PGTO_TIT preenchido
print("\n5. ESTATISTICAS DE PAGAMENTO:")
print("-"*70)

try:
    cursor.execute("""
        SELECT 
            COUNT(*) as total_com_pgto,
            MIN(DT_PGTO_TIT) as primeira_data,
            MAX(DT_PGTO_TIT) as ultima_data
        FROM pcjTITULOS
        WHERE DT_PGTO_TIT IS NOT NULL
    """)
    
    row = cursor.fetchone()
    print(f"Total de titulos com pagamento: {row[0]}")
    print(f"Primeira data: {row[1]}")
    print(f"Ultima data: {row[2]}")
    
    # Contar hoje
    cursor.execute("""
        SELECT COUNT(*)
        FROM pcjTITULOS
        WHERE DT_PGTO_TIT >= #2025-10-07#
    """)
    hoje = cursor.fetchone()[0]
    print(f"\nTitulos com DT_PGTO_TIT em 07/10/2025 ou posterior: {hoje}")
    
except Exception as e:
    print(f"Erro ao buscar estatisticas: {e}")

conn.close()

print("\n" + "="*70)
print("ANALISE CONCLUIDA")
print("="*70)
