# -*- coding: utf-8 -*-
"""
DESCOBRIR LAYOUT CORRETO DO CBR724
"""

import os
import re

print("="*100)
print("ANÁLISE DETALHADA DO LAYOUT CBR724 REAL")
print("="*100)

pasta_processados = r"D:\Teste_Cobrança_Acess\Retorno\Processados"
arquivos = [f for f in os.listdir(pasta_processados) if f.startswith('CBR724')]

if arquivos:
    arquivo = os.path.join(pasta_processados, arquivos[0])
    
    with open(arquivo, 'r', encoding='latin-1') as f:
        linhas = f.readlines()
    
    # Pegar a primeira linha tipo 7
    for linha in linhas:
        linha = linha.rstrip('\n\r')
        if linha.startswith(' 7') and len(linha) == 160:
            print(f"\nLINHA TIPO 7 COMPLETA (160 chars):")
            print("="*100)
            print(linha)
            print("="*100)
            
            # Mostrar cada posição de 10 em 10
            print("\nPOSIÇÕES DE 10 EM 10:")
            print("-"*100)
            for i in range(0, len(linha), 10):
                conteudo = linha[i:i+10]
                print(f"[{i:3d}-{i+9:3d}]: '{conteudo}'")
            
            # Buscar padrões numéricos que podem ser Nosso Número
            print("\n" + "="*100)
            print("NÚMEROS ENCONTRADOS NA LINHA:")
            print("="*100)
            
            # Procurar sequências de dígitos
            for match in re.finditer(r'\d+', linha):
                numero = match.group()
                pos_inicio = match.start()
                pos_fim = match.end()
                
                # Se tiver 9-10 dígitos, pode ser Nosso Número
                if 5 <= len(numero) <= 10:
                    print(f"  [{pos_inicio:3d}-{pos_fim:3d}]: {numero} ({len(numero)} dígitos) "
                          f"← Possível Nosso Número")
            
            # Procurar valores monetários (formato brasileiro)
            print("\n" + "="*100)
            print("VALORES MONETÁRIOS ENCONTRADOS:")
            print("="*100)
            
            for match in re.finditer(r'\d{1,10}\.?\d{0,3},\d{2}', linha):
                valor = match.group()
                pos_inicio = match.start()
                pos_fim = match.end()
                print(f"  [{pos_inicio:3d}-{pos_fim:3d}]: {valor}")
            
            # Análise manual do conteúdo
            print("\n" + "="*100)
            print("ANÁLISE MANUAL POR SEGMENTO:")
            print("="*100)
            
            print(f"\nSegmento 1 [0-3]:     '{linha[0:3]}'     ← Tipo registro")
            print(f"Segmento 2 [3-21]:   '{linha[3:21]}'  ← Código banco/título")
            print(f"Segmento 3 [21-31]:  '{linha[21:31]}'   ← Nosso Número? (10 chars)")
            print(f"Segmento 4 [31-65]:  '{linha[31:65]}'  ← Nome cliente (34 chars)")
            print(f"Segmento 5 [65-73]:  '{linha[65:73]}'          ← Data vencimento?")
            print(f"Segmento 6 [73-87]:  '{linha[73:87]}'   ← ?")
            print(f"Segmento 7 [87-160]: '{linha[87:160]}'")
            
            break
    
    # Mostrar TODOS os Nosso Números extraídos
    print("\n" + "="*100)
    print("TODOS OS NOSSO NÚMEROS DO ARQUIVO (posição [21:31]):")
    print("="*100)
    
    nosso_numeros = []
    for i, linha in enumerate(linhas, 1):
        linha = linha.rstrip('\n\r')
        if linha.startswith(' 7') and len(linha) == 160:
            nosso_numero = linha[21:31].strip()
            nosso_numero_limpo = nosso_numero.lstrip('0')
            nosso_numeros.append((i, nosso_numero, nosso_numero_limpo))
    
    print(f"\n{'Linha':<8} {'Nosso Número Original':<25} {'Sem zeros':<15}")
    print("-"*50)
    for linha_num, nn_original, nn_limpo in nosso_numeros:
        print(f"{linha_num:<8} {nn_original:<25} {nn_limpo:<15}")
    
    print(f"\n✓ Total de títulos: {len(nosso_numeros)}")
    
    # Verificar o 880
    print("\n" + "="*100)
    print("VERIFICANDO TÍTULO 880:")
    print("="*100)
    
    encontrado_880 = False
    for linha_num, nn_original, nn_limpo in nosso_numeros:
        if nn_limpo == '880' or nn_original == '880' or nn_original == '0000000880':
            print(f"✓ ENCONTRADO na linha {linha_num}: '{nn_original}' (limpo: '{nn_limpo}')")
            encontrado_880 = True
    
    if not encontrado_880:
        print(f"✗ Título 880 NÃO está neste arquivo")
        print(f"   Títulos que estão: {', '.join([nn for _, _, nn in nosso_numeros[:10]])}")

print("\n" + "="*100)
