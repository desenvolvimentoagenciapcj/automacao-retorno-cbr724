"""
Script simplificado para verificar título do ID_PCJ 880
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
    print("VERIFICANDO TÍTULO 1227008958 (ID_PCJ 880 - MD PAPEIS)")
    print("="*80 + "\n")
    
    # Buscar o título processado
    cursor.execute("SELECT * FROM pcjTITULOS WHERE NR_NNR_TIT = ?", '1227008958')
    row = cursor.fetchone()
    
    if row:
        columns = [column[0] for column in cursor.description]
        print("✅ TÍTULO ENCONTRADO!\n")
        print("DADOS ATUALIZADOS:")
        for i, col_name in enumerate(columns):
            value = row[i]
            if value is not None:
                # Formatar datas e valores
                if isinstance(value, datetime):
                    formatted_value = value.strftime('%d/%m/%Y %H:%M:%S')
                    if col_name == 'DT_PGTO_TIT' and value.date() == datetime.now().date():
                        formatted_value += " ✅ ATUALIZADO HOJE!"
                elif col_name in ['VL_TIT', 'VL_PGTO_TIT', 'VL_JUROS_TIT'] and isinstance(value, (int, float)):
                    formatted_value = f"R$ {value:,.2f}"
                else:
                    formatted_value = str(value)
                print(f"  {col_name}: {formatted_value}")
        
        # Verificar se foi pago hoje
        idx_dt_pgto = columns.index('DT_PGTO_TIT') if 'DT_PGTO_TIT' in columns else None
        if idx_dt_pgto and row[idx_dt_pgto] and row[idx_dt_pgto].date() == datetime.now().date():
            print("\n" + "="*80)
            print("✅ CONFIRMADO: Pagamento processado com sucesso em 08/10/2025!")
            print("="*80)
    else:
        print("❌ Título não encontrado!")
    
    print("\n" + "="*80)
    print("TODOS OS TÍTULOS DO ID_PCJ 880 COM VENCIMENTO 31/10/2025")
    print("="*80 + "\n")
    
    cursor.execute("""
        SELECT NR_NNR_TIT, DT_VCM_TIT, DT_PGTO_TIT 
        FROM pcjTITULOS 
        WHERE CD_SAC = 880 AND DT_VCM_TIT = #2025-10-31#
        ORDER BY NR_NNR_TIT
    """)
    
    titles = cursor.fetchall()
    if titles:
        for title in titles:
            status = "✅ PAGO HOJE" if title[2] and title[2].date() == datetime.now().date() else ("PAGO" if title[2] else "NÃO PAGO")
            print(f"  • {title[0]} - Vencimento: {title[1]} - Status: {status}")
    else:
        print("  Nenhum título encontrado com vencimento 31/10/2025")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
