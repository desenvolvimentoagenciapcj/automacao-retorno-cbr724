#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica se o título 880 foi atualizado no banco
"""

import pyodbc
from datetime import datetime

# Caminho do banco
caminho_banco = r"D:/Teste_Cobrança_Acess/dbBaixa2025.accdb"

# Conecta no banco
driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
conn_str = f'DRIVER={driver};DBQ={caminho_banco};'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("\n" + "="*70)
print("🔍 VERIFICANDO TÍTULO 880 NO BANCO DE DADOS")
print("="*70)

# Busca o título 880
sql = """
    SELECT NR_NNR_TIT, CD_SAC, DT_VCM_TIT, VL_NOM_TIT, 
           DT_PGTO_TIT, VL_PGTO_TIT, VL_JUROS_TIT, 
           DT_LIB_CRED, CodMovimento, ID_CONTROLE, Situacao
    FROM pcjTITULOS
    WHERE NR_NNR_TIT LIKE '%880'
    ORDER BY NR_NNR_TIT
"""

cursor.execute(sql)
rows = cursor.fetchall()

if not rows:
    print("\n❌ NENHUM TÍTULO ENCONTRADO COM FINAL '880'")
else:
    print(f"\n✅ Encontrados {len(rows)} título(s) com final '880':\n")
    
    for row in rows:
        print("-" * 70)
        print(f"📋 Nosso Número: {row[0]}")
        print(f"👤 CD_SAC (Cliente): {row[1]}")
        print(f"📅 Data Vencimento: {row[2]}")
        print(f"💰 Valor Título: R$ {row[3]:,.2f}" if row[3] else "💰 Valor Título: -")
        print(f"📅 Data Pagamento: {row[4]}" if row[4] else "📅 Data Pagamento: NÃO PAGO")
        print(f"💵 Valor Pago: R$ {row[5]:,.2f}" if row[5] else "💵 Valor Pago: -")
        print(f"📈 Juros: R$ {row[6]:,.2f}" if row[6] else "📈 Juros: -")
        print(f"🏦 Data Crédito: {row[7]}" if row[7] else "🏦 Data Crédito: -")
        print(f"🔢 Código Movimento: {row[8]}" if row[8] else "🔢 Código Movimento: -")
        print(f"⚙️  ID_CONTROLE: {row[9]}" if row[9] else "⚙️  ID_CONTROLE: -")
        print(f"📊 Situação: {row[10]}" if row[10] else "📊 Situação: -")
        
        # Verifica se foi atualizado hoje
        if row[4]:  # Se tem data de pagamento
            data_pgto = row[4]
            hoje = datetime.now().date()
            
            if hasattr(data_pgto, 'date'):
                data_pgto = data_pgto.date()
            
            if data_pgto == hoje:
                print("\n✅ ATUALIZADO HOJE!")
            else:
                print(f"\n⚠️  Data de pagamento: {data_pgto} (NÃO é hoje)")

print("\n" + "="*70)

# Agora busca especificamente o 0000000880
print("\n🔍 Buscando especificamente '0000000880':")
print("="*70)

sql2 = """
    SELECT NR_NNR_TIT, CD_SAC, DT_VCM_TIT, VL_NOM_TIT, 
           DT_PGTO_TIT, VL_PGTO_TIT, VL_JUROS_TIT, 
           DT_LIB_CRED, CodMovimento, ID_CONTROLE, Situacao
    FROM pcjTITULOS
    WHERE NR_NNR_TIT = '0000000880'
"""

cursor.execute(sql2)
row = cursor.fetchone()

if row:
    print("\n✅ TÍTULO 0000000880 ENCONTRADO:")
    print("-" * 70)
    print(f"📋 Nosso Número: {row[0]}")
    print(f"👤 CD_SAC (Cliente): {row[1]}")
    print(f"📅 Data Vencimento: {row[2]}")
    print(f"💰 Valor Título: R$ {row[3]:,.2f}" if row[3] else "💰 Valor Título: -")
    print(f"📅 Data Pagamento: {row[4]}" if row[4] else "📅 Data Pagamento: NÃO PAGO")
    print(f"💵 Valor Pago: R$ {row[5]:,.2f}" if row[5] else "💵 Valor Pago: -")
    print(f"📈 Juros: R$ {row[6]:,.2f}" if row[6] else "📈 Juros: -")
    print(f"🏦 Data Crédito: {row[7]}" if row[7] else "🏦 Data Crédito: -")
    print(f"🔢 Código Movimento: {row[8]}" if row[8] else "🔢 Código Movimento: -")
    print(f"⚙️  ID_CONTROLE: {row[9]}" if row[9] else "⚙️  ID_CONTROLE: -")
    print(f"📊 Situação: {row[10]}" if row[10] else "📊 Situação: -")
else:
    print("\n❌ TÍTULO 0000000880 NÃO ENCONTRADO")

print("\n" + "="*70)

# Verifica se há títulos com vencimento 31/10/2025
print("\n🔍 Buscando títulos com vencimento 31/10/2025:")
print("="*70)

sql3 = """
    SELECT NR_NNR_TIT, CD_SAC, DT_VCM_TIT, VL_NOM_TIT, 
           DT_PGTO_TIT, VL_PGTO_TIT
    FROM pcjTITULOS
    WHERE DT_VCM_TIT >= #10/31/2025# AND DT_VCM_TIT < #11/01/2025#
    ORDER BY NR_NNR_TIT
"""

cursor.execute(sql3)
rows = cursor.fetchall()

if rows:
    print(f"\n✅ Encontrados {len(rows)} título(s) com vencimento 31/10/2025:\n")
    for row in rows:
        pago = "✅ PAGO" if row[4] else "❌ NÃO PAGO"
        print(f"  • {row[0]} - Vencto: {row[2]} - Valor: R$ {row[3]:,.2f} - {pago}")
else:
    print("\n❌ Nenhum título com vencimento 31/10/2025")

print("\n" + "="*70 + "\n")

cursor.close()
conn.close()
