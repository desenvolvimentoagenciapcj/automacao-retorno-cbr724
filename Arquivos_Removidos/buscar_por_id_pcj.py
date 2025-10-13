#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca títulos pelo ID_PCJ (CD_SAC) no banco Access
"""

import pyodbc
from datetime import datetime

# Conectar ao banco
caminho_banco = r'D:\Teste_Cobrança_Acess\dbBaixa2025.accdb'
driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
conn_str = f'DRIVER={driver};DBQ={caminho_banco};'

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # ID_PCJ que você está procurando
    id_pcj = 880
    
    print(f"\n{'='*80}")
    print(f"BUSCANDO TÍTULOS DO ID_PCJ: {id_pcj}")
    print(f"{'='*80}\n")
    
    # Buscar todos os títulos desse ID_PCJ
    sql = """
        SELECT 
            NR_NNR_TIT,
            CD_SAC,
            DT_VCM_TIT,
            VL_NOM_TIT,
            DT_PGTO_TIT,
            VL_PGTO_TIT,
            VL_JUROS_TIT,
            DT_LIB_CRED,
            CodMovimento,
            ID_CONTROLE,
            Situacao,
            Data_Transf_baixa
        FROM pcjTITULOS
        WHERE CD_SAC = ?
        ORDER BY DT_VCM_TIT DESC
    """
    
    cursor.execute(sql, (id_pcj,))
    titulos = cursor.fetchall()
    
    if not titulos:
        print(f"❌ Nenhum título encontrado para ID_PCJ = {id_pcj}")
    else:
        print(f"✅ Encontrados {len(titulos)} título(s) para ID_PCJ = {id_pcj}\n")
        
        for i, titulo in enumerate(titulos, 1):
            print(f"TÍTULO {i}:")
            print(f"  Nosso Número: {titulo[0]}")
            print(f"  ID_PCJ (CD_SAC): {titulo[1]}")
            print(f"  Vencimento: {titulo[2]}")
            print(f"  Valor Título: R$ {titulo[3]:,.2f}" if titulo[3] else "  Valor Título: N/A")
            print(f"  Data Pagamento: {titulo[4]}")
            print(f"  Valor Pago: R$ {titulo[5]:,.2f}" if titulo[5] else "  Valor Pago: N/A")
            print(f"  Juros: R$ {titulo[6]:,.2f}" if titulo[6] else "  Juros: N/A")
            print(f"  Data Crédito: {titulo[7]}")
            print(f"  Código Movimento: {titulo[8]}")
            print(f"  ID_CONTROLE: {titulo[9]}")
            print(f"  Situação: {titulo[10]}")
            print(f"  Data Transf/Baixa: {titulo[11]}")
            
            # Verificar se foi atualizado hoje
            if titulo[11]:  # Data_Transf_baixa
                if isinstance(titulo[11], datetime):
                    data_update = titulo[11].date()
                    hoje = datetime.now().date()
                    if data_update == hoje:
                        print(f"  ✅ ATUALIZADO HOJE!")
                    else:
                        print(f"  ⚠️  Última atualização: {data_update}")
            
            print(f"{'-'*80}\n")
    
    # Buscar especificamente título com vencimento 31/10/2025
    print(f"\n{'='*80}")
    print(f"BUSCANDO TÍTULO COM VENCIMENTO 31/10/2025 PARA ID_PCJ {id_pcj}")
    print(f"{'='*80}\n")
    
    sql_venc = """
        SELECT 
            NR_NNR_TIT,
            CD_SAC,
            DT_VCM_TIT,
            VL_NOM_TIT,
            DT_PGTO_TIT,
            VL_PGTO_TIT
        FROM pcjTITULOS
        WHERE CD_SAC = ?
          AND DT_VCM_TIT = #2025-10-31#
    """
    
    cursor.execute(sql_venc, (id_pcj,))
    titulo_venc = cursor.fetchone()
    
    if titulo_venc:
        print(f"✅ TÍTULO ENCONTRADO:")
        print(f"  Nosso Número: {titulo_venc[0]}")
        print(f"  ID_PCJ: {titulo_venc[1]}")
        print(f"  Vencimento: {titulo_venc[2]}")
        print(f"  Valor: R$ {titulo_venc[3]:,.2f}" if titulo_venc[3] else "N/A")
        print(f"  Data Pagamento: {titulo_venc[4]}")
        print(f"  Valor Pago: R$ {titulo_venc[5]:,.2f}" if titulo_venc[5] else "N/A")
    else:
        print(f"❌ Nenhum título encontrado com vencimento 31/10/2025 para ID_PCJ {id_pcj}")
        print(f"\nVerificando se existe algum título próximo dessa data...")
        
        # Buscar em outubro/2025
        sql_mes = """
            SELECT 
                NR_NNR_TIT,
                DT_VCM_TIT,
                VL_NOM_TIT,
                DT_PGTO_TIT
            FROM pcjTITULOS
            WHERE CD_SAC = ?
              AND DT_VCM_TIT >= #2025-10-01#
              AND DT_VCM_TIT <= #2025-10-31#
            ORDER BY DT_VCM_TIT
        """
        
        cursor.execute(sql_mes, (id_pcj,))
        titulos_mes = cursor.fetchall()
        
        if titulos_mes:
            print(f"\n📅 Encontrados {len(titulos_mes)} título(s) em outubro/2025:")
            for t in titulos_mes:
                print(f"  - NN: {t[0]}, Venc: {t[1]}, Valor: R$ {t[2]:,.2f}, Pago: {t[3]}")
        else:
            print(f"\n❌ Nenhum título encontrado em outubro/2025 para ID_PCJ {id_pcj}")
    
    conn.close()
    print(f"\n{'='*80}\n")
    
except Exception as e:
    print(f"\n❌ Erro: {e}\n")
