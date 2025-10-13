"""
Relatório do processamento - verificar baixas realizadas hoje
"""
import pyodbc
from datetime import datetime

# Conectar ao banco
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("="*60)
print("RELATORIO DE PROCESSAMENTO - 07/10/2025")
print("="*60)

# Contar registros atualizados hoje
cursor.execute("""
    SELECT COUNT(*) as total
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
""")
total_hoje = cursor.fetchone()[0]

print(f"\nTotal de titulos com DT_PGTO_TIT = 07/10/2025: {total_hoje}")

# Mostrar alguns exemplos
cursor.execute("""
    SELECT TOP 10 NR_NNR_TIT, VL_PGTO_TIT, DT_PGTO_TIT
    FROM pcjTITULOS
    WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
    ORDER BY NR_NNR_TIT
""")

print("\nExemplos de titulos processados hoje:")
print("-"*60)
print(f"{'Nosso Numero':<15} {'Valor Pago':>15} {'Data Pagamento':>20}")
print("-"*60)

for row in cursor.fetchall():
    nosso_num = row[0]
    valor = row[1] if row[1] else 0.0
    data = row[2]
    print(f"{nosso_num:<15} R$ {valor:>12.2f} {data}")

conn.close()

print("\n" + "="*60)
print("Relatorio concluido!")
print("="*60)
