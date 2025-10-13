"""
Script para buscar títulos específicos do arquivo CBR724 processado
"""
import pyodbc
import os

# Conectar ao banco
caminho_db = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"
conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={caminho_db};'

print("\n" + "="*70)
print("  🔍 BUSCANDO TÍTULOS DO ARQUIVO CBR724 PROCESSADO")
print("="*70 + "\n")

# Nosso Números extraídos do arquivo que você enviou
nossos_numeros = [
    '000008952',
    '000008953',
    '000008954',
    '000002487',
    '000002517',
    '000002586',
    '000003689',
    '000005726',
    '000007974',
    '000008951'
]

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    print(f"✅ Conectado ao banco: {os.path.basename(caminho_db)}\n")
    print(f"📋 Buscando {len(nossos_numeros)} Nosso Números do arquivo CBR724...\n")
    print("-" * 70)
    
    encontrados = 0
    nao_encontrados = 0
    
    for nn in nossos_numeros:
        # Buscar com zeros à esquerda
        query = "SELECT NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT, DT_LIB_CRED FROM pcjTITULOS WHERE NR_NNR_TIT = ?"
        cursor.execute(query, nn)
        resultado = cursor.fetchone()
        
        if resultado:
            encontrados += 1
            print(f"✅ {nn}: ENCONTRADO!")
            print(f"   Data Pgto: {resultado[1] if resultado[1] else 'Não pago'}")
            print(f"   Valor Pgto: R$ {resultado[2] if resultado[2] else '0,00'}")
            print(f"   Dt Crédito: {resultado[3] if resultado[3] else 'N/A'}")
        else:
            # Tentar sem zeros à esquerda
            nn_sem_zeros = nn.lstrip('0')
            cursor.execute(query, nn_sem_zeros)
            resultado = cursor.fetchone()
            
            if resultado:
                encontrados += 1
                print(f"✅ {nn} (como '{nn_sem_zeros}'): ENCONTRADO!")
                print(f"   Data Pgto: {resultado[1] if resultado[1] else 'Não pago'}")
                print(f"   Valor Pgto: R$ {resultado[2] if resultado[2] else '0,00'}")
            else:
                nao_encontrados += 1
                print(f"❌ {nn}: NÃO ENCONTRADO")
        print()
    
    print("-" * 70)
    print(f"\n📊 RESUMO:")
    print(f"   ✅ Encontrados: {encontrados}")
    print(f"   ❌ Não encontrados: {nao_encontrados}")
    print(f"   📈 Taxa de sucesso: {(encontrados/len(nossos_numeros)*100):.1f}%\n")
    
    # Se encontrou algum, mostrar exemplo de como está gravado
    if encontrados > 0:
        print("="*70)
        print("  💡 VERIFICANDO FORMATO NO BANCO")
        print("="*70 + "\n")
        
        cursor.execute("""
            SELECT TOP 5 NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT 
            FROM pcjTITULOS 
            WHERE NR_NNR_TIT LIKE '00000%'
            ORDER BY NR_NNR_TIT DESC
        """)
        
        print("Exemplos de Nosso Números no banco que começam com '00000':\n")
        for row in cursor.fetchall():
            print(f"   {row[0]} - Pago: {row[1]} - Valor: R$ {row[2] if row[2] else '0,00'}")
    
    conn.close()
    
    print("\n" + "="*70)
    print("  ✅ VERIFICAÇÃO CONCLUÍDA!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}\n")
