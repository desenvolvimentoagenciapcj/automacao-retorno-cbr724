"""
Debug detalhado do processamento
"""
from processador_cbr724 import ProcessadorCBR724

arquivo = r"D:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

print("\n" + "="*80)
print("DEBUG: Lendo linha por linha")
print("="*80 + "\n")

with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = f.readlines()

# Encontrar linhas tipo ' 7'
for i, linha in enumerate(linhas, 1):
    if linha.startswith(' 7'):
        print(f"LINHA {i} (comprimento: {len(linha.rstrip())}):")
        print(f"'{linha.rstrip()}'")
        print()
        
        # Tentar extrair campos manualmente
        print("CAMPOS EXTRAÍDOS:")
        print(f"  [0:3]   Tipo: '{linha[0:3]}'")
        print(f"  [21:31] Nosso Número: '{linha[21:31]}'")
        print(f"  [35:61] Cliente: '{linha[35:61]}'")
        print(f"  [61:69] Vencimento: '{linha[61:69]}'")
        print(f"  [80:100] Região aprox: '{linha[80:100]}'")
        print()
        
        # Tentar processar
        processador = ProcessadorCBR724()
        registro = processador._processar_titulo_tipo7(linha)
        
        if registro:
            print("REGISTRO PROCESSADO:")
            for key, value in registro.items():
                print(f"  {key}: {value}")
        else:
            print("❌ Falha ao processar")
        
        print("\n" + "-"*80 + "\n")
