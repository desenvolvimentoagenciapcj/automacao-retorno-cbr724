# -*- coding: utf-8 -*-
"""
TESTE - Verificar se arquivos IEDCBR sao apagados automaticamente
"""

import os
import shutil
from pathlib import Path

print("="*70)
print("TESTE: APAGAR ARQUIVOS IEDCBR AUTOMATICAMENTE")
print("="*70)

# Caminhos
pasta_retorno = r"D:\Teste_Cobrança_Acess\Retorno"
pasta_origem = r"d:\Teste_Cobrança_Acess\Retorno\Processados"

# Verificar se existem arquivos IEDCBR para testar
print("\n1. Procurando arquivos IEDCBR para teste...")

arquivos_ied = []
for arquivo in os.listdir(pasta_origem):
    if arquivo.upper().startswith('IEDCBR'):
        arquivos_ied.append(arquivo)

if not arquivos_ied:
    print("   Nenhum arquivo IEDCBR encontrado na pasta Processados")
    print("\n2. Criando arquivo IEDCBR de teste...")
    # Criar um arquivo de teste
    arquivo_teste = os.path.join(pasta_retorno, "IEDCBR_TESTE_DELETE.ret")
    with open(arquivo_teste, 'w') as f:
        f.write("Arquivo de teste IEDCBR - deve ser apagado automaticamente")
    print(f"   Arquivo criado: {os.path.basename(arquivo_teste)}")
else:
    print(f"   Encontrados {len(arquivos_ied)} arquivo(s) IEDCBR")
    
    print("\n2. Copiando 1 arquivo IEDCBR para pasta de entrada...")
    arquivo_origem = os.path.join(pasta_origem, arquivos_ied[0])
    arquivo_teste = os.path.join(pasta_retorno, f"TESTE_{arquivos_ied[0]}")
    
    shutil.copy2(arquivo_origem, arquivo_teste)
    print(f"   Copiado: {os.path.basename(arquivo_teste)}")

print("\n3. STATUS DO ARQUIVO:")
print(f"   Caminho: {arquivo_teste}")
print(f"   Existe: {os.path.exists(arquivo_teste)}")
print(f"   Tamanho: {os.path.getsize(arquivo_teste)} bytes")

print("\n" + "="*70)
print("IMPORTANTE:")
print("- Quando o monitor_arquivos_simples.py processar este arquivo,")
print("  ele sera APAGADO AUTOMATICAMENTE (nao vai para Processados)")
print("- Verifique os logs para confirmar: '🗑️ Arquivo IEDCBR APAGADO'")
print("="*70)

print("\nPROXIMOS PASSOS:")
print("1. Execute: python monitor_arquivos_simples.py")
print(f"2. O arquivo '{os.path.basename(arquivo_teste)}' sera detectado")
print("3. O sistema vai apagar o arquivo automaticamente")
print("4. Verifique que o arquivo NAO existe mais na pasta")
print("="*70)
