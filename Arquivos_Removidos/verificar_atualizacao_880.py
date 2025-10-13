"""
Script para verificar se o título do ID_PCJ 880 foi atualizado corretamente
"""
import pyodbc
from datetime import datetime

# Caminho do banco
DB_PATH = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"

# String de conexão
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={DB_PATH};'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("VERIFICANDO ATUALIZAÇÃO DO TÍTULO 1227008958 (ID_PCJ 880)")
    print("="*80 + "\n")
    
    # Buscar o título específico que foi processado
    query = """
    SELECT 
        NR_NNR_TIT,
        CD_SAC,
        DT_VCM_TIT,
        VL_TIT,
        DT_PGTO_TIT,
        VL_PGTO_TIT,
        VL_JUROS_TIT,
        DT_LIB_CRED,
        CodMovimento,
        Situacao,
        DT_TRANSF_BAIXA
    FROM pcjTITULOS
    WHERE NR_NNR_TIT = '1227008958'
    """
    query = "SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?"
    
    cursor.execute(query, '1227008958')
    row = cursor.fetchone()
    
    if row:
        print("✅ TÍTULO ENCONTRADO E ATUALIZADO!\n")
        columns = [column[0] for column in cursor.description]
        
        # Encontrar índices das colunas
        idx_nnr = columns.index('NR_NNR_TIT')
        idx_sac = columns.index('CD_SAC')
        idx_vcm = columns.index('DT_VCM_TIT')
        idx_vl_tit = columns.index('VL_TIT')
        idx_dt_pgto = columns.index('DT_PGTO_TIT')
        idx_vl_pgto = columns.index('VL_PGTO_TIT')
        idx_juros = columns.index('VL_JUROS_TIT') if 'VL_JUROS_TIT' in columns else None
        idx_cred = columns.index('DT_LIB_CRED') if 'DT_LIB_CRED' in columns else None
        idx_mov = columns.index('CodMovimento') if 'CodMovimento' in columns else None
        idx_sit = columns.index('Situacao') if 'Situacao' in columns else None
        idx_transf = columns.index('DT_TRANSF_BAIXA') if 'DT_TRANSF_BAIXA' in columns else None
        
        print(f"  Nosso Número: {row[idx_nnr]}")
        print(f"  ID_PCJ (Cliente): {row[idx_sac]}")
        print(f"  Vencimento: {row[idx_vcm]}")
        print(f"  Valor Título: R$ {row[idx_vl_tit]:,.2f}" if row[idx_vl_tit] else "  Valor Título: N/A")
        print(f"  📅 Data Pagamento: {row[idx_dt_pgto]} {'✅ ATUALIZADO HOJE!' if row[idx_dt_pgto] and row[idx_dt_pgto].date() == datetime.now().date() else ''}")
        print(f"  💰 Valor Pago: R$ {row[idx_vl_pgto]:,.2f}" if row[idx_vl_pgto] else "  Valor Pago: N/A")
        if idx_juros:
            print(f"  Juros: R$ {row[idx_juros]:,.2f}" if row[idx_juros] else "  Juros: N/A")
        if idx_cred:
            print(f"  Data Crédito: {row[idx_cred]}")
        if idx_mov:
            print(f"  Código Movimento: {row[idx_mov]}")
        if idx_sit:
            print(f"  Situação: {row[idx_sit]}")
        if idx_transf:
            print(f"  Data Transf/Baixa: {row[idx_transf]}")
        
        if row[idx_dt_pgto] and row[idx_dt_pgto].date() == datetime.now().date():
            print("\n" + "="*80)
            print("✅ CONFIRMADO: Pagamento processado com sucesso em 08/10/2025!")
            print("="*80 + "\n")
        else:
            print("\n⚠️ Data de pagamento não foi atualizada para hoje")
    else:
        print("❌ Título 1227008958 não encontrado no banco!")
    
    # Também verificar o título 2500003711 que apareceu na busca anterior
    print("\n" + "="*80)
    print("VERIFICANDO TÍTULO 2500003711 (Vencimento 31/10/2025)")
    print("="*80 + "\n")
    
    query2 = "SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?"
    
    cursor.execute(query2, '2500003711')
    row2 = cursor.fetchone()
    
    if row2:
        columns = [column[0] for column in cursor.description]
        idx_nnr = columns.index('NR_NNR_TIT')
        idx_sac = columns.index('CD_SAC')
        idx_vcm = columns.index('DT_VCM_TIT')
        idx_vl_tit = columns.index('VL_TIT')
        idx_dt_pgto = columns.index('DT_PGTO_TIT')
        idx_vl_pgto = columns.index('VL_PGTO_TIT')
        idx_sit = columns.index('Situacao') if 'Situacao' in columns else None
        
        print(f"  Nosso Número: {row2[idx_nnr]}")
        print(f"  ID_PCJ (Cliente): {row2[idx_sac]}")
        print(f"  Vencimento: {row2[idx_vcm]}")
        print(f"  Valor: R$ {row2[idx_vl_tit]:,.2f}" if row2[idx_vl_tit] else "  Valor: N/A")
        print(f"  Data Pagamento: {row2[idx_dt_pgto] if row2[idx_dt_pgto] else 'Não pago'}")
        print(f"  Valor Pago: R$ {row2[idx_vl_pgto]:,.2f}" if row2[idx_vl_pgto] else "  Valor Pago: N/A")
        if idx_sit:
            print(f"  Situação: {row2[idx_sit]}")
        
        if row2[idx_sac] == 880 and not row2[idx_dt_pgto]:
            print("\n⚠️ Este é OUTRO título do ID_PCJ 880 que ainda não foi pago")
            print("   (Diferente do título 1227008958 que acabamos de processar)")
    
    # Listar TODOS os títulos do ID_PCJ 880 com vencimento em outubro/2025
    print("\n" + "="*80)
    print("TODOS OS TÍTULOS DO ID_PCJ 880 COM VENCIMENTO EM OUT/2025")
    print("="*80 + "\n")
    
    query3 = """
    SELECT * FROM pcjTITULOS
    WHERE CD_SAC = 880 
    AND DT_VCM_TIT >= #2025-10-01# 
    AND DT_VCM_TIT <= #2025-10-31#
    ORDER BY DT_VCM_TIT
    """
    
    cursor.execute(query3)
    rows = cursor.fetchall()
    
    if rows:
        columns = [column[0] for column in cursor.description]
        idx_nnr = columns.index('NR_NNR_TIT')
        idx_vcm = columns.index('DT_VCM_TIT')
        idx_vl_tit = columns.index('VL_TIT')
        idx_dt_pgto = columns.index('DT_PGTO_TIT')
        idx_vl_pgto = columns.index('VL_PGTO_TIT')
        idx_sit = columns.index('Situacao') if 'Situacao' in columns else None
        
        for i, row in enumerate(rows, 1):
            print(f"\nTÍTULO {i}:")
            print(f"  Nosso Número: {row[idx_nnr]}")
            print(f"  Vencimento: {row[idx_vcm]}")
            print(f"  Valor: R$ {row[idx_vl_tit]:,.2f}" if row[idx_vl_tit] else "  Valor: N/A")
            print(f"  Data Pagamento: {row[idx_dt_pgto] if row[idx_dt_pgto] else '❌ Não pago'}")
            print(f"  Valor Pago: R$ {row[idx_vl_pgto]:,.2f}" if row[idx_vl_pgto] else "  Valor Pago: N/A")
            if idx_sit:
                print(f"  Situação: {row[idx_sit]}")
            
            if row[idx_dt_pgto] and row[idx_dt_pgto].date() == datetime.now().date():
                print("  ✅ PAGO HOJE!")
    else:
        print("Nenhum título encontrado para ID_PCJ 880 em outubro/2025")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Erro ao conectar: {e}")
