#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisar arquivo CBR724 real e verificar no banco
"""

import pyodbc
import os

# Arquivo para analisar
arquivo_processado = r"D:\Teste_Cobrança_Acess\Retorno\Processados"
arquivos = [f for f in os.listdir(arquivo_processado) if 'CBR724' in f and f.endswith('.ret')]

if not arquivos:
    print("Nenhum arquivo CBR724 encontrado!")
    exit()

arquivo = os.path.join(arquivo_processado, arquivos[0])
print(f"\n=== ANALISANDO: {arquivos[0]} ===\n")

# Ler linhas tipo 7
with open(arquivo, 'r', encoding='latin-1') as f:
    linhas = f.readlines()

linhas_tipo7 = [l for l in linhas if l.startswith(' 7') and len(l.strip()) > 0]

print(f"Total de linhas tipo 7: {len(linhas_tipo7)}\n")

if linhas_tipo7:
    linha = linhas_tipo7[0].rstrip('\n\r')
    print(f"Primeira linha tipo 7 (tamanho={len(linha)}):")
    print(linha)
    print("\n--- ANÁLISE DE POSIÇÕES ---")
    print(f"[0:3]   Tipo: [{linha[0:3]}]")
    print(f"[3:20]  Código: [{linha[3:20]}]")
    print(f"[21:31] Nosso Num posição 1: [{linha[21:31]}]")
    
    # Analisar nome cliente
    print(f"[31:64] Nome cliente: [{linha[31:64]}]")
    
    # Data vencimento
    print(f"[65:73] Data venc: [{linha[65:73]}]")
    
    # Extrair nosso número da posição 21-31
    nosso_num = linha[21:31].strip()
    print(f"\n--- NOSSO NÚMERO EXTRAÍDO: {nosso_num} ---\n")
    
    # Buscar no banco
    conn_str = (
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Buscar exatamente como está
        print(f"1. Buscando: '{nosso_num}'")
        cursor.execute("SELECT NR_NNR_TIT, DT_VENC_TIT, VL_NOM_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nosso_num,))
        result = cursor.fetchone()
        if result:
            print(f"   ✓ ENCONTRADO: {result[0]} | Venc: {result[1]} | Valor: {result[2]}")
        else:
            print(f"   ✗ NÃO encontrado")
        
        # Tentar sem zeros à esquerda
        nosso_sem_zeros = nosso_num.lstrip('0')
        print(f"\n2. Buscando sem zeros: '{nosso_sem_zeros}'")
        cursor.execute("SELECT NR_NNR_TIT, DT_VENC_TIT, VL_NOM_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nosso_sem_zeros,))
        result = cursor.fetchone()
        if result:
            print(f"   ✓ ENCONTRADO: {result[0]} | Venc: {result[1]} | Valor: {result[2]}")
        else:
            print(f"   ✗ NÃO encontrado")
        
        # Buscar todos nosso números dos primeiros 5 registros
        print(f"\n--- VERIFICANDO PRIMEIROS 5 REGISTROS ---\n")
        for i, linha in enumerate(linhas_tipo7[:5], 1):
            linha = linha.rstrip('\n\r')
            nn = linha[21:31].strip()
            nn_sem_zeros = nn.lstrip('0')
            
            cursor.execute("SELECT NR_NNR_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nn,))
            result = cursor.fetchone()
            
            if not result and nn_sem_zeros != nn:
                cursor.execute("SELECT NR_NNR_TIT FROM pcjTITULOS WHERE NR_NNR_TIT = ?", (nn_sem_zeros,))
                result = cursor.fetchone()
            
            status = "✓ ENCONTRADO" if result else "✗ NÃO ENCONTRADO"
            if result:
                print(f"{i}. {nn} → {status} como '{result[0]}'")
            else:
                print(f"{i}. {nn} → {status}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")

print("\n" + "="*60)
