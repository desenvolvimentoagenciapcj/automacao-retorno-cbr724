# -*- coding: utf-8 -*-
"""
RELATORIO FINAL DO PROCESSAMENTO
Sistema de Automacao de Retorno Bancario CBR724
"""

import pyodbc
from datetime import datetime

print("="*70)
print("           RELATORIO FINAL - PROCESSAMENTO CBR724")
print("="*70)
print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*70)

# Conectar ao banco
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 1. Total de titulos processados hoje
cursor.execute("""
    SELECT COUNT(*) as total
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
""")
total_hoje = cursor.fetchone()[0]

print(f"\n1. TITULOS PROCESSADOS HOJE (07/10/2025)")
print("-"*70)
print(f"   Total de baixas realizadas: {total_hoje}")

# 2. Soma dos valores pagos
cursor.execute("""
    SELECT SUM(VL_PGTO_TIT) as total_valor
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
""")
total_valor = cursor.fetchone()[0] or 0.0

print(f"   Valor total processado: R$ {total_valor:,.2f}")

# 3. Top 10 maiores valores
print(f"\n2. TOP 10 MAIORES PAGAMENTOS")
print("-"*70)
print(f"{'Nosso Numero':<15} {'Valor':>15}")
print("-"*70)

cursor.execute("""
    SELECT TOP 10 
        NR_NNR_TIT,
        VL_PGTO_TIT
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
    ORDER BY VL_PGTO_TIT DESC
""")

for row in cursor.fetchall():
    nn = row[0]
    valor = row[1] if row[1] else 0.0
    print(f"{nn:<15} R$ {valor:>12,.2f}")

# 4. Estatisticas gerais
print(f"\n3. ESTATISTICAS GERAIS")
print("-"*70)

cursor.execute("""
    SELECT 
        MIN(VL_PGTO_TIT) as menor,
        MAX(VL_PGTO_TIT) as maior,
        AVG(VL_PGTO_TIT) as media
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
""")

row = cursor.fetchone()
menor = row[0] if row[0] else 0.0
maior = row[1] if row[1] else 0.0
media = row[2] if row[2] else 0.0

print(f"   Menor valor: R$ {menor:,.2f}")
print(f"   Maior valor: R$ {maior:,.2f}")
print(f"   Valor medio: R$ {media:,.2f}")

conn.close()

print("\n" + "="*70)
print("               PROCESSAMENTO CONCLUIDO COM SUCESSO!")
print("="*70)
print("\nPROXIMOS PASSOS:")
print("1. Abrir o Access: dbBaixa2025.accdb (pressione SHIFT ao abrir)")
print("2. Abrir formulario: frmModulo")
print("3. Verificar os registros processados")
print("="*70)
