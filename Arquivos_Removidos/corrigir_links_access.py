#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitário para corrigir links e dependências em bancos Access
Remove referências a caminhos de rede (H:\, \\servidor, etc)
"""

import pyodbc
import sys

def diagnosticar_banco(caminho_banco):
    """Diagnostica problemas de links no banco Access"""
    print(f"\n🔍 DIAGNOSTICANDO: {caminho_banco}\n")
    
    try:
        # Conecta ao banco
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={caminho_banco};'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Lista tabelas locais
        tabelas_locais = [row.table_name for row in cursor.tables(tableType='TABLE')]
        print(f"📊 Tabelas LOCAIS: {len(tabelas_locais)}")
        for t in tabelas_locais:
            print(f"   ✓ {t}")
        
        # Lista tabelas vinculadas
        tabelas_vinculadas = [row.table_name for row in cursor.tables(tableType='LINK')]
        print(f"\n🔗 Tabelas VINCULADAS: {len(tabelas_vinculadas)}")
        for t in tabelas_vinculadas:
            print(f"   ⚠️  {t}")
        
        # Lista views/queries
        views = [row.table_name for row in cursor.tables(tableType='VIEW')]
        print(f"\n📋 VIEWS/QUERIES: {len(views)}")
        for v in views:
            print(f"   • {v}")
        
        conn.close()
        
        print("\n" + "="*60)
        if tabelas_vinculadas:
            print("⚠️  PROBLEMA ENCONTRADO: Existem tabelas vinculadas!")
            print("   Solução: Usar Access para atualizar os links")
        else:
            print("✅ Nenhuma tabela vinculada encontrada via ODBC")
            print("   Se ainda pede caminho de rede ao abrir:")
            print("   - Pode ser referência VBA")
            print("   - Pode ser formulário de startup")
            print("   - Pode ser consulta com link externo")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ ERRO: {e}\n")

def criar_solucao_access_vba():
    """Cria código VBA para executar dentro do Access"""
    codigo_vba = """
' ============================================================
' CÓDIGO VBA PARA REMOVER TABELAS VINCULADAS
' Execute este código no Access (Alt+F11 > Módulo > Colar)
' ============================================================

Sub RemoverTabelasVinculadas()
    Dim db As DAO.Database
    Dim tdf As DAO.TableDef
    Dim contador As Integer
    
    Set db = CurrentDb()
    contador = 0
    
    ' Percorre todas as tabelas
    For Each tdf In db.TableDefs
        ' Verifica se é tabela vinculada (tem Connect)
        If Len(tdf.Connect) > 0 Then
            Debug.Print "Removendo: " & tdf.Name & " (" & tdf.Connect & ")"
            db.TableDefs.Delete tdf.Name
            contador = contador + 1
        End If
    Next tdf
    
    MsgBox "Removidas " & contador & " tabelas vinculadas!", vbInformation
    Set db = Nothing
End Sub

Sub DesabilitarStartup()
    ' Desabilita formulário de inicialização
    On Error Resume Next
    Application.SetOption "Start Form Name", ""
    MsgBox "Formulário de startup desabilitado!", vbInformation
End Sub

Sub ListarReferencias()
    ' Lista todas as referências do projeto
    Dim ref As Reference
    Debug.Print "=== REFERÊNCIAS ==="
    For Each ref In Application.References
        Debug.Print ref.Name & " - " & ref.FullPath
    Next ref
End Sub
"""
    
    arquivo_vba = "D:\\Teste_Cobrança_Acess\\codigo_correcao_access.txt"
    with open(arquivo_vba, 'w', encoding='utf-8') as f:
        f.write(codigo_vba)
    
    print(f"📝 Código VBA salvo em: {arquivo_vba}")
    print("\nPara usar:")
    print("1. Abra dbBaixa2025.accdb no Access (segure SHIFT ao abrir para pular startup)")
    print("2. Pressione Alt+F11 para abrir o editor VBA")
    print("3. Insira > Módulo")
    print("4. Cole o código do arquivo criado")
    print("5. Execute: RemoverTabelasVinculadas()")
    print("6. Execute: DesabilitarStartup()\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  CORRETOR DE LINKS - MICROSOFT ACCESS")
    print("="*60)
    
    # Diagnostica dbBaixa2025
    diagnosticar_banco("D:/Teste_Cobrança_Acess/dbBaixa2025.accdb")
    
    # Diagnostica Cobranca2019
    print("\n" + "-"*60 + "\n")
    diagnosticar_banco("D:/Teste_Cobrança_Acess/Cobranca2019.accdb")
    
    # Cria código VBA para solução
    print("\n" + "-"*60 + "\n")
    criar_solucao_access_vba()
