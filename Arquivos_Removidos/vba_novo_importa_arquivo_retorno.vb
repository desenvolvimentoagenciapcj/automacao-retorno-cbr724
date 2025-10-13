Option Compare Database

Public Sub ImportaCBR724()

'Antes de executar o módulo, entre com os valores abaixo:
AnoReferencia = 21
ArquivoRetorno = "CBR72462483009202521607_id.ret"
FilesPath = "\\servidor1\CobrancaPCJ\CobrancaPCJ\Retorno\"

InFileName = FilesPath & ArquivoRetorno
OutFileName = FilesPath & "Log_" & ArquivoRetorno & ".txt"

'Abre arquivos e tabelas
InFile = FreeFile()
Open InFileName For Input As InFile
OutFile = FreeFile()
Open OutFileName For Output As OutFile
Write #OutFile, "Log do arquivo " & InFileName
Write #OutFile, ""
Set RsTitulo = CurrentDb.OpenRecordset("pcjTITULOS")
RsTitulo.Index = "PrimaryKey"

Line Input #InFile, MyString
Line Input #InFile, MyString
Line Input #InFile, MyString
DataArquivo = Mid(MyString, 115, 2) & "/" & Mid(MyString, 117, 2) & "/" & Mid(MyString, 119, 4)

Line Input #InFile, MyString
While Not EOF(InFile)
    'Se linha possui titulo
    If Mid(MyString, 2, 1) = "7" Then
        If Mid(MyString, 4, 1) <> " " Then
            'Obtém dados do título
            NossoNumero = Mid(MyString, 4, 17)
            Sacado = Trim(Mid(MyString, 35, 27))
            Vencimento = CDate(Mid(MyString, 64, 2) & "/" & Mid(MyString, 66, 2) & "/" & Mid(MyString, 70, 2))
            Operacao = Mid(MyString, 84, 2)
            ValorTitulo = CCur(LTrim(Mid(MyString, 88, 19)))
            ValorPago = CCur(LTrim(Mid(MyString, 137, 15)))
            Juros = ValorPago - ValorTitulo

            '1º Verifica se nome do sacado possui ID_PCJ
            If InStr(1, "0123456789", Left(Sacado, 1)) = 0 Then
                'Se título não possui ID_PCJ
                Write #OutFile, "ERRO! Título sem ID_PCJ: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
            Else
                'Obtém ID_PCJ
                IdLength = 1
                For i = 2 To 6
                    If InStr(1, "0123456789", Mid(Sacado, i, 1)) > 0 Then
                        IdLength = i
                    End If
                Next
                ID_PCJ = Int(Left(Sacado, IdLength))

                '3º Verifica se título já está cadastrado
                NossoNumero = Right(NossoNumero, 10)
                RsTitulo.Seek "=", NossoNumero
                If RsTitulo.NoMatch Then
                    'Para título ainda não cadastrado
                    If Operacao = "BX" Then
                        'Cadastra título cancelado
                        RsTitulo.AddNew
                        RsTitulo("NR_NNR_TIT") = NossoNumero
                        RsTitulo("CD_SAC") = ID_PCJ
                        RsTitulo("DT_VCM_TIT") = Vencimento
                        RsTitulo("VL_NOM_TIT") = ValorTitulo
                        RsTitulo("AnoRef") = AnoReferencia
                        RsTitulo("Situacao") = "A"
                        RsTitulo("Data_Transf_baixa") = Now()
                        RsTitulo("ID_TIPO_CONTROLE") = 1
                        RsTitulo("ID_CONTROLE") = 3
                        RsTitulo.Update
                        Write #OutFile, "Cadastrado título cancelado: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                    If Operacao = "LQ" Or (Operacao = "LC") Then
                        'Cadastra título pago
                        RsTitulo.AddNew
                        RsTitulo("NR_NNR_TIT") = NossoNumero
                        RsTitulo("CD_SAC") = ID_PCJ
                        RsTitulo("DT_VCM_TIT") = Vencimento
                        RsTitulo("VL_NOM_TIT") = ValorTitulo
                        RsTitulo("AnoRef") = AnoReferencia
                        RsTitulo("Situacao") = "A"
                        RsTitulo("Data_Transf_baixa") = Now()
                        RsTitulo("ID_TIPO_CONTROLE") = 1
                        RsTitulo("ID_CONTROLE") = 2
                        RsTitulo("DT_PGTO_TIT") = CDate(DataArquivo)
                        RsTitulo("VL_PGTO_TIT") = ValorPago
                        If Juros > 0 Then
                            RsTitulo("VL_JUROS_TIT") = Juros
                        End If
                        RsTitulo.Update
                        Write #OutFile, "Cadastrado título pago: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                    If Operacao = "RG" Then
                        'Cadastra título novo
                        RsTitulo.AddNew
                        RsTitulo("NR_NNR_TIT") = NossoNumero
                        RsTitulo("CD_SAC") = ID_PCJ
                        RsTitulo("DT_VCM_TIT") = Vencimento
                        RsTitulo("VL_NOM_TIT") = ValorTitulo
                        RsTitulo("AnoRef") = AnoReferencia
                        RsTitulo("Situacao") = "A"
                        RsTitulo("Data_Transf_baixa") = Now()
                        RsTitulo("ID_TIPO_CONTROLE") = 1
                        RsTitulo("ID_CONTROLE") = 1
                        RsTitulo.Update
                        Write #OutFile, "Cadastrado título novo: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                    If (Operacao <> "RG") And (Operacao <> "LQ") And (Operacao <> "BX") And (Operacao <> "LC") Then
                        Write #OutFile, "ERRO! Operação desconhecida: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                Else
                    'Para título já cadastrado
                    If Operacao = "BX" Then
                        BXS = Mid(MyString, 84, 3)
                        If BXS = "BXS" Then
                            Write #OutFile, "Ignorado cancelamento automático título: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                        Else
                            'Baixa título apenas se cancelado manualmente, ignora cancelamento automatico do BB
                            RsTitulo.Edit
                            RsTitulo("ID_CONTROLE") = 3
                            RsTitulo("Data_Transf_baixa") = Now()
                            RsTitulo.Update
                            Write #OutFile, "Cancelado título: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                        End If
                    End If
                    If Operacao = "MT" Then 'Ignora movimentação MTV
                       Write #OutFile, "Ignorado cancelamento automático título: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                    If (Operacao = "LQ") Or (Operacao = "LC") Then
                        'Paga título
                        RsTitulo.Edit
                        RsTitulo("ID_CONTROLE") = 2
                        RsTitulo("DT_PGTO_TIT") = CDate(DataArquivo)
                        RsTitulo("VL_PGTO_TIT") = ValorPago
                        RsTitulo("Data_Transf_baixa") = Now()
                        If Juros > 0 Then
                            RsTitulo("VL_JUROS_TIT") = Juros
                        End If
                        RsTitulo.Update
                        Write #OutFile, "Pago título: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                    'Ignorar operação desconhecida
                    If (Operacao <> "RG") And (Operacao <> "LQ") And (Operacao <> "BX") And (Operacao <> "LC") And (Operacao <> "MT") Then
                        Write #OutFile, "ERRO! Operação desconhecida: " & NossoNumero & " " & Sacado & " " & Vencimento & " " & Operacao & " " & ValorTitulo & " " & ValorPago
                    End If
                End If
            End If
        End If
    End If
    
    Line Input #InFile, MyString

Wend

'Fecha arquivos e tabelas
RsTitulo.Close
Close #InFile
Close #OutFile

MsgBox ("Arquivo importado com sucesso!")

End Sub

