import pyodbc

conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:/Teste_Cobrança_Acess/dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("\nExemplos de Nosso Numeros no banco:\n")

cursor.execute("SELECT TOP 10 NR_NNR_TIT FROM pcjTITULOS ORDER BY NR_NNR_TIT DESC")

for row in cursor.fetchall():
    print(f"  {row[0]}")

print("\nPodemos criar um arquivo CBR724 de teste com ESSES numeros!\n")

conn.close()
