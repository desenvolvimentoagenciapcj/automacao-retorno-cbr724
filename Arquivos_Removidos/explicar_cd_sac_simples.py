#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explicar CD_SAC de forma simples
"""

import pyodbc

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("="*80)
print("O QUE É CD_SAC (ID_PCJ)?")
print("="*80)

print("""
CD_SAC = Código do Sacado (Cliente/Pagador)
ID_PCJ = Identificação PCJ (MESMO campo, nome diferente na interface)

É como um CPF/CNPJ interno do sistema.
Identifica QUEM deve pagar o título.
""")

print("\n" + "="*80)
print("EXEMPLO PRÁTICO:")
print("="*80)

# Buscar título 1227008952
cursor.execute("""
    SELECT CD_SAC, NR_NNR_TIT, VL_PGTO_TIT, DT_PGTO_TIT
    FROM pcjTITULOS 
    WHERE NR_NNR_TIT = '1227008952'
""")

result = cursor.fetchone()

if result:
    print(f"""
Título: {result[1]}
CD_SAC (ID_PCJ): {result[0]}  ← ESTE é o código do cliente
Valor Pago: R$ {result[2]}
Data Pagamento: {result[3]}
""")

# Buscar todos os títulos desse cliente
print(f"Buscando TODOS os títulos do cliente {result[0]}...")
cursor.execute("""
    SELECT NR_NNR_TIT, VL_PGTO_TIT, DT_PGTO_TIT
    FROM pcjTITULOS 
    WHERE CD_SAC = ?
    AND DT_PGTO_TIT IS NOT NULL
    ORDER BY DT_PGTO_TIT DESC
""", result[0])

titulos = cursor.fetchall()[:10]  # Primeiros 10

print(f"\nCliente {result[0]} tem {len(titulos)} títulos pagos (mostrando 10):")
print("-"*80)
for t in titulos:
    print(f"  Título: {t[0]} | Valor: R$ {t[1]} | Data: {t[2]}")

cursor.close()
conn.close()

print("\n" + "="*80)
print("DIFERENÇA: CD_SAC vs Número no arquivo")
print("="*80)
print("""
NO ARQUIVO DE RETORNO:
  Linha: "411 - IOCHPE-MAXION S/A"
  └─ "411" é um código de IDENTIFICAÇÃO INTERNA do boleto
  
NO BANCO DE DADOS:
  CD_SAC (ID_PCJ): 2525
  └─ Este é o código REAL do cliente no sistema
  
⚠️ O número "411" do arquivo NÃO é o CD_SAC!
⚠️ Para ver o título no Access, filtre por ID_PCJ = 2525, não 411!
""")
print("="*80)
