#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Importação - Consulta pcjTITULOS para ver registros processados
"""

import pyodbc
from datetime import datetime, timedelta

def verificar_importacao():
    """Verifica os registros processados recentemente no pcjTITULOS"""
    
    print("\n" + "="*70)
    print("  🔍 VERIFICADOR DE IMPORTAÇÃO - pcjTITULOS")
    print("="*70 + "\n")
    
    try:
        # Conecta ao banco
        caminho_banco = "D:/Teste_Cobrança_Acess/dbBaixa2025.accdb"
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={caminho_banco};'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("✅ Conectado ao dbBaixa2025.accdb\n")
        
        # 1. Total de registros
        cursor.execute("SELECT COUNT(*) FROM pcjTITULOS")
        total = cursor.fetchone()[0]
        print(f"📊 Total de registros na pcjTITULOS: {total:,}\n")
        
        # 2. Registros com baixa (pagos)
        cursor.execute("""
            SELECT COUNT(*) FROM pcjTITULOS 
            WHERE DT_PGTO_TIT IS NOT NULL
        """)
        pagos = cursor.fetchone()[0]
        print(f"💰 Títulos pagos (DT_PGTO_TIT preenchido): {pagos:,}")
        print(f"📈 Percentual pago: {(pagos/total*100):.2f}%\n")
        
        # 3. Últimas atualizações (se houver campo de data de atualização)
        print("-" * 70)
        print("📅 ÚLTIMAS BAIXAS PROCESSADAS (Top 10):\n")
        
        cursor.execute("""
            SELECT TOP 10
                NR_NNR_TIT AS NossoNumero,
                DT_PGTO_TIT AS DataPagamento,
                VL_PGTO_TIT AS ValorPago,
                VL_JUROS_TIT AS Juros,
                DT_LIB_CRED AS DataCredito,
                CodMovimento
            FROM pcjTITULOS
            WHERE DT_PGTO_TIT IS NOT NULL
            ORDER BY DT_PGTO_TIT DESC
        """)
        
        registros = cursor.fetchall()
        
        if registros:
            print(f"{'Nosso Número':<15} {'Data Pgto':<12} {'Valor Pago':<12} {'Juros':<10} {'Dt Créd':<12} {'Mov':<5}")
            print("-" * 70)
            for reg in registros:
                nosso_num = str(reg.NossoNumero or '').strip()
                dt_pgto = reg.DataPagamento.strftime('%d/%m/%Y') if reg.DataPagamento else 'N/A'
                vl_pago = f"R$ {reg.ValorPago:.2f}" if reg.ValorPago else 'R$ 0,00'
                juros = f"R$ {reg.Juros:.2f}" if reg.Juros else 'R$ 0,00'
                dt_cred = reg.DataCredito.strftime('%d/%m/%Y') if reg.DataCredito else 'N/A'
                cod_mov = str(reg.CodMovimento or '').strip()
                
                print(f"{nosso_num:<15} {dt_pgto:<12} {vl_pago:<12} {juros:<10} {dt_cred:<12} {cod_mov:<5}")
        else:
            print("⚠️  Nenhuma baixa encontrada")
        
        print("\n" + "-" * 70)
        
        # 4. Buscar por Nosso Número específico (dos arquivos CBR724 processados)
        print("\n🔎 VERIFICANDO NOSSO NÚMEROS DOS ARQUIVOS CBR724:\n")
        
        nossos_numeros_teste = [
            '0000008952', '0000008953', '0000008954', '0000008955',
            '0000008956', '0000008957', '0000008958'
        ]
        
        encontrados = 0
        for nn in nossos_numeros_teste:
            cursor.execute("""
                SELECT NR_NNR_TIT, DT_PGTO_TIT, VL_PGTO_TIT 
                FROM pcjTITULOS 
                WHERE NR_NNR_TIT = ?
            """, nn)
            
            resultado = cursor.fetchone()
            if resultado:
                encontrados += 1
                status = "✅ PAGO" if resultado.DT_PGTO_TIT else "⏳ Pendente"
                valor = f"R$ {resultado.VL_PGTO_TIT:.2f}" if resultado.VL_PGTO_TIT else "R$ 0,00"
                print(f"  {nn}: {status} - {valor}")
            else:
                print(f"  {nn}: ❌ NÃO ENCONTRADO")
        
        print(f"\n📊 Resumo: {encontrados} de {len(nossos_numeros_teste)} nossos números encontrados\n")
        
        # 5. Estatísticas de processamento
        print("-" * 70)
        print("\n📈 ESTATÍSTICAS DE MOVIMENTAÇÃO:\n")
        
        cursor.execute("""
            SELECT CodMovimento, COUNT(*) as Qtd
            FROM pcjTITULOS
            WHERE CodMovimento IS NOT NULL
            GROUP BY CodMovimento
            ORDER BY COUNT(*) DESC
        """)
        
        movimentos = cursor.fetchall()
        if movimentos:
            for mov in movimentos[:5]:
                cod = str(mov.CodMovimento or '').strip()
                qtd = mov.Qtd
                print(f"  Código {cod}: {qtd:,} ocorrências")
        
        conn.close()
        
        print("\n" + "="*70)
        print("✅ Verificação concluída!\n")
        
    except Exception as e:
        print(f"❌ ERRO: {e}\n")

if __name__ == "__main__":
    # Fecha Access se estiver aberto
    import subprocess
    try:
        subprocess.run(
            'taskkill /F /IM MSACCESS.EXE 2>$null',
            shell=True,
            capture_output=True
        )
    except:
        pass
    
    verificar_importacao()
