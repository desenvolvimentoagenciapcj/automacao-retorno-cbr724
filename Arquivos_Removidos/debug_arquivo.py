"""
Script para debugar o conteúdo de um arquivo CBR724
"""

arquivo = r"D:\Teste_Cobrança_Acess\Retorno\CBR7244179904202115456_Processado.ret"

print("="*60)
print("ANÁLISE DETALHADA DO ARQUIVO CBR724")
print("="*60)

with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = f.readlines()
    
print(f"\n📄 Total de linhas: {len(linhas)}")
print(f"📏 Caracteres por linha: {len(linhas[0]) if linhas else 0}")

# Analisar registros tipo 7
print("\n" + "="*60)
print("REGISTROS TIPO 7 (Títulos)")
print("="*60)

count_tipo7 = 0
for i, linha in enumerate(linhas, 1):
    if len(linha) >= 160:
        tipo = linha[0:1]
        if tipo == '7':
            count_tipo7 += 1
            # Extrair campos conforme manual
            codigo_banco = linha[3:20].strip()
            nosso_numero_pos21_30 = linha[21:30].strip()  # 9 caracteres
            nosso_numero_pos21_31 = linha[21:31].strip()  # 10 caracteres
            nome_cliente = linha[31:64].strip()
            data_venc = linha[65:73].strip()
            
            print(f"\n📌 Linha {i} - Tipo {tipo}")
            print(f"   Código Banco [3:20]: '{codigo_banco}'")
            print(f"   Nosso Número [21:30]: '{nosso_numero_pos21_30}' (9 chars) → sem zeros: '{nosso_numero_pos21_30.lstrip('0')}'")
            print(f"   Nosso Número [21:31]: '{nosso_numero_pos21_31}' (10 chars) → sem zeros: '{nosso_numero_pos21_31.lstrip('0')}'")
            print(f"   Cliente [31:64]: '{nome_cliente}'")
            print(f"   Data Venc [65:73]: '{data_venc}'")
            print(f"   Linha completa: {linha[:80]}")

print(f"\n✅ Total de registros tipo 7: {count_tipo7}")
