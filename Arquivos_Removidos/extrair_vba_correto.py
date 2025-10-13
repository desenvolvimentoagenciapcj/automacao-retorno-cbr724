#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrair código VBA - nome correto
"""

import win32com.client

print("="*80)
print("EXTRAINDO CÓDIGO VBA")
print("="*80)

try:
    access = win32com.client.Dispatch("Access.Application")
    access.OpenCurrentDatabase(r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb")
    
    module_name = "Novo importa arquivo retorno"
    
    print(f"\n📖 Extraindo módulo: {module_name}")
    
    vba_module = access.VBE.ActiveVBProject.VBComponents(module_name)
    vba_code = vba_module.CodeModule.Lines(1, vba_module.CodeModule.CountOfLines)
    
    # Salvar
    output_file = r"D:\Teste_Cobrança_Acess\AutomacaoRetorno\vba_novo_importa_arquivo_retorno.vb"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(vba_code)
    
    print(f"✅ Código salvo em: {output_file}")
    print(f"\n📄 Total de linhas: {vba_code.count(chr(10)) + 1}")
    
    print("\n" + "="*80)
    print("CÓDIGO VBA COMPLETO:")
    print("="*80)
    print(vba_code)
    
    access.CloseCurrentDatabase()
    access.Quit()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
