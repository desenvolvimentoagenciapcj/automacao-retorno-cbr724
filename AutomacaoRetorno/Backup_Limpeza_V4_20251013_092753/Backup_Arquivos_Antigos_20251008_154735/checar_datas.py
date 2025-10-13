"""
Verificação simples das datas dos títulos processados
"""
import pyodbc

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;')
cursor = conn.cursor()

print("\n" + "="*80)
print("📅 VERIFICAÇÃO DE DATAS - Títulos Processados")
print("="*80)

# Buscar títulos específicos que sabemos que foram processados
titulos = [
    ('9000008952', '01/10/2025'),
    ('9000008953', '01/10/2025'),
    ('9000008955', '02/10/2025'),
    ('9000008956', '02/10/2025'),
    ('9000008957', '03/10/2025'),
    ('9000008958', '06/10/2025'),
    ('2500003816', '07/10/2025'),
    ('2500006861', '06/10/2025'),
    ('2500008044', '02/10/2025'),
]

print(f"\n🔍 Verificando {len(titulos)} títulos...\n")
print(f"{'Nosso Número':<15} {'Data Esperada':<15} {'DT_PGTO_TIT Real':<18} {'Status'}")
print("-"*70)

erros = []
acertos = 0

for nosso_num, data_esperada in titulos:
    try:
        # Query simples título por título
        cursor.execute(f"SELECT NossoNumero, DT_PGTO_TIT FROM pcjTITULOS WHERE NossoNumero = '{nosso_num}'")
        row = cursor.fetchone()
        
        if row:
            dt_pgto_real = row[1].strftime("%d/%m/%Y") if row[1] else "SEM DATA"
            
            if dt_pgto_real == data_esperada:
                status = "✅ OK"
                acertos += 1
            else:
                status = "❌ ERRO"
                erros.append(f"{nosso_num}: esperado {data_esperada}, obteve {dt_pgto_real}")
            
            print(f"{nosso_num:<15} {data_esperada:<15} {dt_pgto_real:<18} {status}")
        else:
            print(f"{nosso_num:<15} {data_esperada:<15} {'NÃO ENCONTRADO':<18} ❌")
            erros.append(f"{nosso_num}: título não encontrado")
    except Exception as e:
        print(f"{nosso_num:<15} {data_esperada:<15} {'ERRO':<18} ❌")
        erros.append(f"{nosso_num}: {e}")

print("\n" + "="*80)
print("📊 RESULTADO")
print("="*80)
print(f"\nAcertos: {acertos}/{len(titulos)}")

if not erros:
    print("\n🎉 SUCESSO TOTAL! Todas as datas estão corretas!")
    print("   • As datas vêm do ARQUIVO (não de hoje - 08/10/2025)")
    print("   • Campo DT_PGTO_TIT contém a data do pagamento do arquivo")
    print("   • Sistema funcionando corretamente!")
else:
    print(f"\n⚠️  {len(erros)} erro(s) encontrado(s):")
    for erro in erros:
        print(f"   • {erro}")

conn.close()
print("\n" + "="*80 + "\n")
