"""
Investigar o título 2500003711 que não aparece no sistema
"""
import pyodbc

DB_PATH = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={DB_PATH};'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("INVESTIGAÇÃO: NOSSO NÚMERO 2500003711")
    print("="*80 + "\n")
    
    # Busca 1: Exato
    print("1️⃣ Buscando exatamente '2500003711'...")
    cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?", '2500003711')
    result = cursor.fetchone()
    
    if result:
        columns = [column[0] for column in cursor.description]
        print("✅ ENCONTRADO com busca exata!\n")
        for i, col in enumerate(columns):
            if result[i] is not None:
                print(f"  {col}: {result[i]}")
    else:
        print("❌ Não encontrado com busca exata\n")
    
    # Busca 2: Parcial sem zeros à esquerda
    print("2️⃣ Buscando '3711' (sem zeros)...")
    cursor.execute("SELECT NR_NNR_TIT, CD_SAC, DT_VCM_TIT, DT_PGTO_TIT FROM pcjTITULOS WHERE NR_NNR_TIT LIKE ?", '%3711')
    results = cursor.fetchall()
    
    if results:
        print(f"✅ Encontrados {len(results)} título(s):\n")
        for row in results:
            print(f"  Nosso Número: {row[0]}")
            print(f"  ID_PCJ: {row[1]}")
            print(f"  Vencimento: {row[2]}")
            print(f"  Data Pagamento: {row[3] if row[3] else 'NÃO PAGO'}")
            print()
    else:
        print("❌ Não encontrado\n")
    
    # Busca 3: Variações
    print("3️⃣ Buscando variações do número...")
    variacoes = ['2500003711', '0003711', '003711', '03711', '3711']
    
    for var in variacoes:
        cursor.execute("SELECT COUNT(*) FROM pcjTITULOS WHERE NR_NNR_TIT = ?", var)
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"  ✅ '{var}': {count} registro(s)")
        else:
            print(f"  ❌ '{var}': não encontrado")
    
    # Busca 4: Todos os títulos com ID_PCJ 880 e vencimento 31/10/2025
    print("\n4️⃣ Todos os títulos do ID_PCJ 880 com vencimento 31/10/2025:")
    cursor.execute("""
        SELECT NR_NNR_TIT, DT_VCM_TIT, VL_NOM_TIT, DT_PGTO_TIT, Situacao 
        FROM pcjTITULOS 
        WHERE CD_SAC = 880 
        AND DT_VCM_TIT = #2025-10-31#
    """)
    
    titulos = cursor.fetchall()
    if titulos:
        print(f"\n✅ Encontrados {len(titulos)} título(s):\n")
        for titulo in titulos:
            print(f"  Nosso Número: {titulo[0]}")
            print(f"  Vencimento: {titulo[1]}")
            print(f"  Valor: R$ {titulo[2]:,.2f}" if titulo[2] else "  Valor: N/A")
            print(f"  Situação: {titulo[4]}")
            print(f"  Status: {'PAGO em ' + str(titulo[3]) if titulo[3] else '❌ NÃO PAGO'}")
            print()
    else:
        print("\n❌ Nenhum título encontrado para ID_PCJ 880 em 31/10/2025")
    
    # Busca 5: Verificar se existe em alguma tabela relacionada
    print("\n5️⃣ Verificando estrutura da tabela pcjTITULOS...")
    cursor.execute("SELECT TOP 1 * FROM pcjTITULOS")
    cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    print(f"\nColunas da tabela ({len(columns)} colunas):")
    for col in columns:
        print(f"  • {col}")
    
    # Busca 6: Contar títulos do ID_PCJ 880
    print("\n6️⃣ Estatísticas do ID_PCJ 880:")
    cursor.execute("SELECT COUNT(*) FROM pcjTITULOS WHERE CD_SAC = 880")
    total = cursor.fetchone()[0]
    print(f"  Total de títulos: {total}")
    
    cursor.execute("SELECT COUNT(*) FROM pcjTITULOS WHERE CD_SAC = 880 AND DT_PGTO_TIT IS NULL")
    nao_pagos = cursor.fetchone()[0]
    print(f"  Não pagos: {nao_pagos}")
    
    cursor.execute("SELECT COUNT(*) FROM pcjTITULOS WHERE CD_SAC = 880 AND DT_PGTO_TIT IS NOT NULL")
    pagos = cursor.fetchone()[0]
    print(f"  Pagos: {pagos}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*80)
    print("FIM DA INVESTIGAÇÃO")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
