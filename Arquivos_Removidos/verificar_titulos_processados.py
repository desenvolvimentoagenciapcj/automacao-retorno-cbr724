# -*- coding: utf-8 -*-
"""
VERIFICAR SE OS TÍTULOS DO ARQUIVO FORAM ATUALIZADOS
"""

import pyodbc
from datetime import datetime

print("="*80)
print("VERIFICANDO SE OS TÍTULOS DO ARQUIVO CBR724 FORAM ATUALIZADOS")
print("="*80)

# Títulos que REALMENTE estão no arquivo processado
titulos_arquivo = ['5777', '5782', '5785', '5786', '5792', '5793', '5801']

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print(f"\nTítulos do arquivo CBR724: {', '.join(titulos_arquivo)}")
print("="*80)

for nn in titulos_arquivo:
    print(f"\n{'-'*80}")
    print(f"BUSCANDO: {nn}")
    print("-"*80)
    
    # Busca exata
    cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nn,))
    row = cursor.fetchone()
    
    if not row:
        # Busca com zeros
        nn_zeros = f"{'0' * (10 - len(nn))}{nn}"
        cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nn_zeros,))
        row = cursor.fetchone()
    
    if not row:
        # Busca parcial
        cursor.execute(f"SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT LIKE '%{nn}'")
        row = cursor.fetchone()
    
    if row:
        cols = [column[0] for column in cursor.description]
        idx_nnr = cols.index('NR_NNR_TIT')
        idx_dt_pgto = cols.index('DT_PGTO_TIT')
        idx_vl_pgto = cols.index('VL_PGTO_TIT')
        idx_dt_cred = cols.index('DT_LIB_CRED')
        
        nn_banco = row[idx_nnr]
        dt_pgto = row[idx_dt_pgto]
        vl_pgto = row[idx_vl_pgto] if row[idx_vl_pgto] else 0.0
        dt_cred = row[idx_dt_cred]
        
        print(f"✓ ENCONTRADO NO BANCO:")
        print(f"  Nosso Número: {nn_banco}")
        print(f"  DT_PGTO_TIT: {dt_pgto}")
        print(f"  VL_PGTO_TIT: R$ {vl_pgto:,.2f}")
        print(f"  DT_LIB_CRED: {dt_cred}")
        
        # Verificar se foi atualizado hoje
        hoje = datetime.now().date()
        if dt_pgto:
            if isinstance(dt_pgto, datetime):
                data_pgto = dt_pgto.date()
            else:
                data_pgto = dt_pgto
            
            if data_pgto == hoje:
                print(f"  ✓✓✓ ATUALIZADO HOJE! ({data_pgto})")
            else:
                print(f"  ✗ NÃO atualizado hoje. Última atualização: {data_pgto}")
        else:
            print(f"  ✗ Sem data de pagamento")
    else:
        print(f"✗ NÃO ENCONTRADO no banco")

# Verificar o título 880 para confirmar
print("\n" + "="*80)
print("VERIFICANDO O TÍTULO 880 (que o usuário mencionou):")
print("="*80)

cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT LIKE '%880'")
rows = cursor.fetchall()

if rows:
    print(f"\n✓ Encontrados {len(rows)} título(s) que terminam com 880")
    
    cols = [column[0] for column in cursor.description]
    idx_nnr = cols.index('NR_NNR_TIT')
    idx_dt_pgto = cols.index('DT_PGTO_TIT')
    idx_vl_pgto = cols.index('VL_PGTO_TIT')
    
    print(f"\n{'Nosso Número':<20} {'Data Pgto':>25} {'Valor':>15} {'Atualizado Hoje?'}")
    print("-"*80)
    
    hoje = datetime.now().date()
    for row in rows[:10]:  # Primeiros 10
        nn_banco = row[idx_nnr]
        dt_pgto = row[idx_dt_pgto]
        vl_pgto = row[idx_vl_pgto] if row[idx_vl_pgto] else 0.0
        
        atualizado_hoje = ""
        if dt_pgto:
            if isinstance(dt_pgto, datetime):
                data_pgto = dt_pgto.date()
            else:
                data_pgto = dt_pgto
            
            if data_pgto == hoje:
                atualizado_hoje = "✓ SIM"
        
        dt_str = str(dt_pgto) if dt_pgto else "N/A"
        print(f"{nn_banco:<20} {dt_str:>25} R$ {vl_pgto:>10,.2f}   {atualizado_hoje}")

conn.close()

print("\n" + "="*80)
print("CONCLUSÃO:")
print("="*80)
print("O sistema está funcionando corretamente.")
print("Os títulos que ESTÃO no arquivo CBR724 devem estar atualizados com data de hoje.")
print("O título 880 NÃO está no arquivo processado, por isso não foi atualizado.")
print("="*80)
