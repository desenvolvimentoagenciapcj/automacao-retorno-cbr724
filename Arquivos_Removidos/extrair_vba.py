#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrair código VBA do Access para análise
"""

import win32com.client
import os

print("="*80)
print("EXTRAINDO CÓDIGO VBA DO ACCESS")
print("="*80)

try:
    # Abrir Access
    access = win32com.client.Dispatch("Access.Application")
    db_path = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"
    
    print(f"\nAbrindo: {db_path}")
    access.OpenCurrentDatabase(db_path)
    
    # Listar módulos VBA
    print("\n📋 Módulos VBA encontrados:")
    print("-"*80)
    
    for i in range(access.CurrentProject.AllModules.Count):
        module = access.CurrentProject.AllModules.Item(i)
        print(f"{i+1}. {module.Name}")
    
    # Buscar o módulo "Novo importar arquivo retorno"
    print("\n🔍 Procurando módulo 'Novo importar arquivo retorno'...")
    
    vba_code = None
    module_name = None
    
    # Tentar variações do nome
    possible_names = [
        "Novo importar arquivo retorno",
        "Novo_importar_arquivo_retorno", 
        "NovoImportarArquivoRetorno",
        "ImportarRetorno"
    ]
    
    for name in possible_names:
        try:
            vba_module = access.VBE.ActiveVBProject.VBComponents(name)
            module_name = name
            vba_code = vba_module.CodeModule.Lines(1, vba_module.CodeModule.CountOfLines)
            print(f"✅ Módulo encontrado: {name}")
            break
        except:
            continue
    
    if vba_code:
        # Salvar código
        output_file = r"D:\Teste_Cobrança_Acess\AutomacaoRetorno\codigo_vba_original.vb"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(vba_code)
        
        print(f"\n✅ Código VBA salvo em: {output_file}")
        print(f"\nPrimeiras 50 linhas do código:")
        print("-"*80)
        lines = vba_code.split('\n')
        for i, line in enumerate(lines[:50], 1):
            print(f"{i:3d}: {line}")
    else:
        print("\n❌ Módulo VBA não encontrado automaticamente")
        print("\nPor favor, me informe:")
        print("1. Qual é o nome EXATO do módulo VBA?")
        print("2. Ou copie e cole aqui as primeiras 30 linhas do código VBA")
    
    access.CloseCurrentDatabase()
    access.Quit()
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    print("\n⚠️  Método alternativo necessário")
    print("\nPor favor:")
    print("1. Abra o Access (dbBaixa2025.accdb)")
    print("2. Pressione Alt+F11 para abrir o VBA")
    print("3. Encontre o módulo 'Novo importar arquivo retorno'")
    print("4. Copie TODO o código e cole em um arquivo .txt")
    print("5. Me envie o arquivo")

print("\n" + "="*80)
