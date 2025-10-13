# -*- coding: utf-8 -*-
"""
VERIFICAR VINCULO - Metodo alternativo
"""

import pyodbc

print("="*70)
print("VERIFICACAO DE ESTRUTURA DOS BANCOS")
print("="*70)

# 1. Analisar dbBaixa2025
print("\n1. TABELAS EM dbBaixa2025:")
print("-"*70)

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

tables_baixa = []
for table_info in cursor.tables(tableType='TABLE'):
    if not table_info.table_name.startswith('MSys'):
        tables_baixa.append(table_info.table_name)

print(f"Total de tabelas: {len(tables_baixa)}\n")

for table_name in sorted(tables_baixa):
    try:
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        count = cursor.fetchone()[0]
        tipo = "LOCAL" if count is not None else "?"
        print(f"  {table_name:<35} {count:>10,} registros  [{tipo}]")
    except Exception as e:
        error_msg = str(e)
        if "não pôde localizar" in error_msg or "Could not find" in error_msg or "H:\\" in error_msg:
            print(f"  {table_name:<35} {'N/A':>10}            [VINCULADA - ERRO]")
        else:
            print(f"  {table_name:<35} {'ERRO':>10}            [{str(e)[:20]}]")

# 2. Verificar especificamente pcjTITULOS
print("\n2. ANALISE DETALHADA - pcjTITULOS:")
print("-"*70)

try:
    cursor.execute("SELECT COUNT(*) FROM pcjTITULOS")
    count = cursor.fetchone()[0]
    print(f"✓ Tabela acessivel: {count:,} registros")
    
    # Ver alguns registros
    cursor.execute("SELECT TOP 3 NR_NNR_TIT, DT_PGTO_TIT FROM pcjTITULOS WHERE DT_PGTO_TIT IS NOT NULL ORDER BY DT_PGTO_TIT DESC")
    print("\nUltimos registros:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]}")
    
    print("\n✓ CONCLUSAO: pcjTITULOS é uma tabela LOCAL e funcional")
    
except Exception as e:
    print(f"✗ ERRO ao acessar pcjTITULOS: {e}")
    if "H:\\" in str(e):
        print("\n⚠ PROBLEMA IDENTIFICADO:")
        print("  pcjTITULOS é uma tabela VINCULADA que aponta para:")
        print("  H:\\CobrancaPCJ\\ (caminho de rede nao acessivel)")
        print("\n  SOLUCAO: Precisamos usar um dbBaixa com tabelas LOCAIS")

conn.close()

# 3. Verificar Cobranca2019
print("\n3. VERIFICANDO Cobranca2019.accdb:")
print("-"*70)

try:
    conn_str2 = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\Cobranca2019.accdb;'
    conn2 = pyodbc.connect(conn_str2)
    cursor2 = conn2.cursor()
    
    tables_cob = []
    for table_info in cursor2.tables(tableType='TABLE'):
        if not table_info.table_name.startswith('MSys'):
            tables_cob.append(table_info.table_name)
    
    print(f"Total de tabelas: {len(tables_cob)}\n")
    
    for table_name in sorted(tables_cob):
        try:
            cursor2.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            count = cursor2.fetchone()[0]
            print(f"  {table_name:<35} {count:>10,} registros")
        except Exception as e:
            if "não pôde localizar" in str(e) or "Could not find" in str(e) or "H:\\" in str(e):
                print(f"  {table_name:<35} {'N/A':>10}            [VINCULADA - ERRO]")
            else:
                print(f"  {table_name:<35} {'ERRO':>10}")
    
    conn2.close()
    
except Exception as e:
    print(f"Erro ao conectar: {e}")

print("\n" + "="*70)
print("RESUMO")
print("="*70)

print("""
INTERPRETACAO DOS RESULTADOS:

1. Se dbBaixa2025 tem APENAS 1 tabela ("Erros ao colar"):
   → Todas as outras tabelas sao VINCULADAS ao Cobranca2019
   → Sistema NAO pode gravar dados (tabelas apontam para H:\\)
   
2. Se dbBaixa2025 tem pcjTITULOS acessivel com muitos registros:
   → pcjTITULOS é LOCAL no dbBaixa2025
   → Sistema PODE gravar dados normalmente
   → Os dados estao sendo gravados corretamente!

3. Para confirmar onde os dados estao:
   → Verificar se Cobranca2019 tem pcjTITULOS
   → Comparar datas de modificacao dos arquivos .accdb
""")

print("="*70)
