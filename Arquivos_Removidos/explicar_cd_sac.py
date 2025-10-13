#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explicar estrutura da tabela pcjTITULOS
"""

import pyodbc

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("="*80)
print("ESTRUTURA DA TABELA pcjTITULOS")
print("="*80)

# Pegar estrutura da tabela
cursor.execute("SELECT TOP 1 * FROM pcjTITULOS WHERE NR_NNR_TIT = '1227008952'")
columns = [column[0] for column in cursor.description]

print("\nCampos principais da tabela:")
print("-"*80)
for i, col in enumerate(columns[:15], 1):  # Primeiros 15 campos
    print(f"{i:2d}. {col}")

# Buscar exemplo
cursor.execute("""
    SELECT CD_SAC, NR_NNR_TIT, VL_NOM_TIT, DT_VCM_TIT, DT_PGTO_TIT, VL_PGTO_TIT
    FROM pcjTITULOS 
    WHERE NR_NNR_TIT = '1227008952'
""")

result = cursor.fetchone()

print("\n" + "="*80)
print("EXEMPLO - Título 1227008952:")
print("="*80)
if result:
    print(f"""
CD_SAC (Código do Sacado/Cliente): {result[0]}
  └─ É o ID do CLIENTE que deve pagar
  └─ Também chamado de ID_PCJ na interface do Access
  
NR_NNR_TIT (Nosso Número): {result[1]}
  └─ É o número ÚNICO do título/boleto
  
VL_NOM_TIT (Valor Nominal): R$ {result[2]}
  └─ Valor original do título
  
DT_VCM_TIT (Data Vencimento): {result[3]}
  └─ Quando o título vence
  
DT_PGTO_TIT (Data Pagamento): {result[4]}
  └─ Quando o título foi pago
  
VL_PGTO_TIT (Valor Pago): R$ {result[5]}
  └─ Quanto foi efetivamente pago
""")

# Buscar nome do cliente
cursor.execute("SELECT ID_PCJ, RazaoSocial FROM pcjMODULO WHERE ID_PCJ = ?", result[0])
cliente = cursor.fetchone()

if cliente:
    print("="*80)
    print("DADOS DO CLIENTE (tabela pcjMODULO):")
    print("="*80)
    print(f"""
ID_PCJ: {cliente[0]}
  └─ É o MESMO valor que CD_SAC na tabela pcjTITULOS
  
Razão Social: {cliente[1]}
  └─ Nome da empresa/pessoa
""")

cursor.close()
conn.close()

print("="*80)
print("RESUMO:")
print("="*80)
print("""
CD_SAC = ID_PCJ = Código do Cliente
  
É como um CPF/CNPJ interno do sistema.
Cada cliente tem UM código único (CD_SAC/ID_PCJ).
Cada cliente pode ter VÁRIOS títulos (NR_NNR_TIT).

Exemplo:
  Cliente 2525 (IOCHPE-MAXION S/A) tem os títulos:
    - 1227008952
    - 1227008953
    - 1227008951
    
  Cliente 2528 (INDUSTRIA CERAMICA) tem o título:
    - 1227008954

No arquivo de retorno, o número "411" é apenas um código
de identificação interna do boleto, NÃO é o CD_SAC real!
""")
print("="*80)
