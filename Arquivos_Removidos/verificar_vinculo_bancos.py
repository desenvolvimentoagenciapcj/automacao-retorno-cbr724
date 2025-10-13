# -*- coding: utf-8 -*-
"""
VERIFICAR VINCULO ENTRE dbBaixa2025 e Cobranca2019
"""

import pyodbc

print("="*70)
print("VERIFICACAO DE VINCULO ENTRE BANCOS")
print("="*70)

# 1. Conectar ao dbBaixa2025
print("\n1. ANALISANDO dbBaixa2025.accdb:")
print("-"*70)

conn_str_baixa = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn_baixa = pyodbc.connect(conn_str_baixa)
cursor_baixa = conn_baixa.cursor()

# Listar todas as tabelas
print("\nTabelas no dbBaixa2025:")
tables_baixa = []
for table_info in cursor_baixa.tables(tableType='TABLE'):
    table_name = table_info.table_name
    if not table_name.startswith('MSys'):  # Ignorar tabelas do sistema
        tables_baixa.append(table_name)
        
        # Verificar se é tabela vinculada
        try:
            cursor_baixa.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            count = cursor_baixa.fetchone()[0]
            print(f"  - {table_name:<30} ({count:,} registros)")
        except Exception as e:
            error_msg = str(e)
            if "não pôde localizar" in error_msg or "Could not find" in error_msg:
                print(f"  - {table_name:<30} [TABELA VINCULADA - ERRO DE CAMINHO]")
            else:
                print(f"  - {table_name:<30} [ERRO: {str(e)[:50]}]")

# 2. Verificar tabelas vinculadas
print("\n2. VERIFICANDO TABELAS VINCULADAS:")
print("-"*70)

cursor_baixa.execute("""
    SELECT Name, Database
    FROM MSysObjects 
    WHERE Type = 6 AND Name NOT LIKE 'MSys%'
""")

linked_tables = []
try:
    for row in cursor_baixa.fetchall():
        table_name = row[0]
        database_path = row[1] if row[1] else "N/A"
        linked_tables.append((table_name, database_path))
        print(f"Tabela: {table_name}")
        print(f"  Caminho: {database_path}")
        print()
except Exception as e:
    print(f"Erro ao buscar tabelas vinculadas: {e}")

if not linked_tables:
    print("Nenhuma tabela vinculada encontrada ou sem permissao para ler MSysObjects")

# 3. Verificar se pcjTITULOS é vinculada
print("\n3. VERIFICANDO TABELA pcjTITULOS:")
print("-"*70)

try:
    cursor_baixa.execute("""
        SELECT Type, Database
        FROM MSysObjects 
        WHERE Name = 'pcjTITULOS'
    """)
    
    row = cursor_baixa.fetchone()
    if row:
        tipo = row[0]
        db_path = row[1] if row[1] else "N/A"
        
        if tipo == 1:
            print("✓ pcjTITULOS é uma TABELA LOCAL (nao vinculada)")
            print(f"  Tipo: {tipo}")
        elif tipo == 6:
            print("⚠ pcjTITULOS é uma TABELA VINCULADA!")
            print(f"  Caminho do banco vinculado: {db_path}")
        else:
            print(f"Tipo desconhecido: {tipo}")
except Exception as e:
    print(f"Nao foi possivel verificar (erro de permissao): {e}")
    print("\nVamos verificar de outra forma...")
    
    # Tentar contar registros
    try:
        cursor_baixa.execute("SELECT COUNT(*) FROM pcjTITULOS")
        count = cursor_baixa.fetchone()[0]
        print(f"✓ pcjTITULOS acessivel com {count:,} registros")
    except Exception as e2:
        error_msg = str(e2)
        if "não pôde localizar" in error_msg or "Could not find" in error_msg:
            print("✗ pcjTITULOS é VINCULADA e o caminho está INCORRETO!")
            print(f"  Erro: {error_msg}")
        else:
            print(f"✗ Erro ao acessar: {e2}")

# 4. Tentar conectar ao Cobranca2019
print("\n4. VERIFICANDO Cobranca2019.accdb:")
print("-"*70)

try:
    conn_str_cobranca = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\Cobranca2019.accdb;'
    conn_cobranca = pyodbc.connect(conn_str_cobranca)
    cursor_cobranca = conn_cobranca.cursor()
    
    print("✓ Conectado ao Cobranca2019.accdb")
    
    # Listar tabelas
    print("\nTabelas no Cobranca2019:")
    for table_info in cursor_cobranca.tables(tableType='TABLE'):
        table_name = table_info.table_name
        if not table_name.startswith('MSys'):
            try:
                cursor_cobranca.execute(f"SELECT COUNT(*) FROM [{table_name}]")
                count = cursor_cobranca.fetchone()[0]
                print(f"  - {table_name:<30} ({count:,} registros)")
            except Exception as e:
                print(f"  - {table_name:<30} [ERRO ou VINCULADA]")
    
    # Verificar se tem pcjTITULOS
    print("\nVerificando pcjTITULOS no Cobranca2019:")
    try:
        cursor_cobranca.execute("SELECT COUNT(*) FROM pcjTITULOS")
        count = cursor_cobranca.fetchone()[0]
        print(f"✓ pcjTITULOS existe no Cobranca2019 com {count:,} registros")
    except:
        print("✗ pcjTITULOS NAO existe no Cobranca2019")
    
    conn_cobranca.close()
    
except Exception as e:
    print(f"✗ Erro ao conectar ao Cobranca2019: {e}")

conn_baixa.close()

print("\n" + "="*70)
print("ANALISE CONCLUIDA")
print("="*70)

print("\nCONCLUSAO:")
print("-"*70)
print("Se dbBaixa2025 tem tabelas VINCULADAS ao Cobranca2019,")
print("e o Cobranca2019 referencia H:\\CobrancaPCJ\\,")
print("entao o sistema NAO conseguira atualizar corretamente!")
print("\nSOLUCAO: Usar apenas dbBaixa2025 com tabelas LOCAIS")
print("="*70)
