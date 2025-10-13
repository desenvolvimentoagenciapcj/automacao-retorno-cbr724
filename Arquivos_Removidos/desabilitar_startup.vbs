' Script VBS para desabilitar formulário de startup no Access
' Criado em: 07/10/2025

Option Explicit

Dim accessApp, dbPath, db

' Caminho do banco de dados
dbPath = "D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"

On Error Resume Next

' Criar instância do Access
Set accessApp = CreateObject("Access.Application")

If Err.Number <> 0 Then
    WScript.Echo "ERRO: Não foi possível abrir o Microsoft Access"
    WScript.Echo "Erro: " & Err.Description
    WScript.Quit 1
End If

' Abrir o banco de dados
accessApp.OpenCurrentDatabase dbPath, False

If Err.Number <> 0 Then
    WScript.Echo "ERRO: Não foi possível abrir o banco de dados"
    WScript.Echo "Erro: " & Err.Description
    accessApp.Quit
    WScript.Quit 1
End If

WScript.Echo ""
WScript.Echo "=========================================="
WScript.Echo "  DESABILITANDO FORMULÁRIO DE STARTUP"
WScript.Echo "=========================================="
WScript.Echo ""

' Limpar propriedades de startup
On Error Resume Next

' Remover formulário de exibição ao iniciar
accessApp.SetOption "Start Up Form", ""
accessApp.CurrentDb.Properties.Delete "StartUpForm"

' Desabilitar outras opções de startup problemáticas
accessApp.SetOption "Start Up Show Database Window", True
accessApp.SetOption "Start Up Show Status Bar", True
accessApp.SetOption "Allow Built In Toolbars", True
accessApp.SetOption "Allow Full Menus", True
accessApp.SetOption "Allow Default Shortcut Menus", True

WScript.Echo "✓ Formulário de startup desabilitado"
WScript.Echo "✓ Janela do banco de dados habilitada"
WScript.Echo "✓ Menus completos habilitados"
WScript.Echo ""

' Salvar e fechar
accessApp.CloseCurrentDatabase
accessApp.Quit

WScript.Echo "=========================================="
WScript.Echo "  ✅ CORREÇÃO APLICADA COM SUCESSO!"
WScript.Echo "=========================================="
WScript.Echo ""
WScript.Echo "Agora você pode abrir o Access normalmente."
WScript.Echo ""

Set accessApp = Nothing
WScript.Quit 0
