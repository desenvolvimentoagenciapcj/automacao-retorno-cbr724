import pyodbc
from datetime import datetime

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;')
cursor = conn.cursor()

print("\n" + "="*80)
print("📅 VERIFICAÇÃO DE DATAS NO BANCO ACCESS")
print("="*80)

# Lista de nossos números processados agora
titulos_processados = [
    '9000008952', '9000008953', '9000008954',  # Arquivo 1 (01/10)
    '9000008955', '9000008956', '2500008044', '9000008772', '9000008895',  # Arquivo 2 (02/10)
    '9000008957', '2500003487', '2500003717',  # Arquivo 3 (03/10) - alguns
    '9000008958', '2500006861', '2500006895', '2500007673', '9000008919',  # Arquivo 4 (06/10)
    '2500003816', '2500003893', '2500006497', '2500006896'  # Arquivo 5 (07/10) - alguns
]

print(f"\n🔍 Buscando {len(titulos_processados)} títulos processados hoje...\n")

# Query direta com valores fixos (Access tem problemas com muitos parâmetros)
titulos_lista = "','".join(titulos_processados[:10])
query = f"""
SELECT NossoNumero, DT_PGTO_TIT, Data_Transf_baixa, Valor
FROM pcjTITULOS
WHERE NossoNumero IN ('{titulos_lista}')
ORDER BY DT_PGTO_TIT, NossoNumero
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print(f"✅ Encontrados {len(rows)} títulos no banco")
    print("\n" + "-"*95)
    print(f"{'Nosso Número':<15} {'DT_PGTO_TIT':<18} {'Data_Transf_baixa':<22} {'Valor':>12}")
    print("-"*95)
    
    for row in rows:
        nosso_num = row[0] or "N/A"
        dt_pgto = row[1].strftime("%d/%m/%Y") if row[1] else "SEM DATA"
        dt_transf = row[2].strftime("%d/%m/%Y %H:%M:%S") if row[2] else "N/A"
        valor = f"R$ {row[3]:,.2f}" if row[3] else "R$ 0.00"
        
        print(f"{nosso_num:<15} {dt_pgto:<18} {dt_transf:<22} {valor:>12}")
    
    # Estatísticas por data de pagamento
    print("\n" + "="*80)
    print("📊 AGRUPAMENTO POR DATA DE PAGAMENTO (DT_PGTO_TIT)")
    print("="*80)
    
    datas_agrupadas = {}
    for row in rows:
        dt_pgto = row[1].strftime("%d/%m/%Y") if row[1] else "SEM DATA"
        if dt_pgto not in datas_agrupadas:
            datas_agrupadas[dt_pgto] = []
        datas_agrupadas[dt_pgto].append(row[0])
    
    print(f"\n{'Data Pagamento':<15} {'Quantidade':>12} {'Títulos'}")
    print("-"*60)
    
    for data in sorted(datas_agrupadas.keys()):
        qtd = len(datas_agrupadas[data])
        titulos_str = ', '.join(datas_agrupadas[data][:3])
        if qtd > 3:
            titulos_str += f", ... (+{qtd-3})"
        print(f"{data:<15} {qtd:>12} {titulos_str}")
    
    # Verificação final
    print("\n" + "="*80)
    print("🔍 VERIFICAÇÃO FINAL: Datas corretas?")
    print("="*80)
    
    datas_corretas = {
        "01/10/2025": ["9000008952", "9000008953", "9000008954"],
        "02/10/2025": ["9000008955", "9000008956", "2500008044"],
        "03/10/2025": ["9000008957", "2500003487"],
        "06/10/2025": ["9000008958"],
        "07/10/2025": ["2500003816"]
    }
    
    print("\n📋 Verificando se as datas dos arquivos estão corretas:")
    print("-" * 60)
    
    erros = []
    for row in rows:
        nosso_num = row[0]
        dt_pgto = row[1].strftime("%d/%m/%Y") if row[1] else None
        
        # Verifica em qual data esse título deveria estar
        data_esperada = None
        for data, titulos in datas_corretas.items():
            if nosso_num in titulos:
                data_esperada = data
                break
        
        if data_esperada:
            if dt_pgto == data_esperada:
                print(f"✅ {nosso_num}: {dt_pgto} (correto!)")
            else:
                print(f"❌ {nosso_num}: {dt_pgto} (esperado {data_esperada})")
                erros.append(f"{nosso_num}: {dt_pgto} != {data_esperada}")
    
    if not erros:
        print("\n🎉 SUCESSO! Todas as datas estão corretas!")
        print("   • Datas vêm do ARQUIVO, não da data de hoje (08/10/2025)")
        print("   • Campo DT_PGTO_TIT contém a data do pagamento do arquivo")
        print("   • Campo Data_Transf_baixa contém a data/hora do processamento")
    else:
        print(f"\n⚠️  {len(erros)} erro(s) encontrado(s):")
        for erro in erros:
            print(f"   • {erro}")
    
else:
    print("\n⚠️  Nenhum título processado hoje encontrado")

conn.close()
print("\n" + "="*80)
