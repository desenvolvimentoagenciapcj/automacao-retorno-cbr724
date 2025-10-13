# -*- coding: utf-8 -*-
"""
CONSULTA INTERATIVA DE TITULOS
Permite consultar e validar titulos processados sem abrir o Access
"""

import pyodbc
from datetime import datetime
import sys

def conectar_banco():
    """Conecta ao banco Access"""
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Teste_Cobrança_Acess\dbBaixa2025.accdb;'
    return pyodbc.connect(conn_str)

def menu_principal():
    """Exibe menu de opcoes"""
    print("\n" + "="*70)
    print("           CONSULTA DE TITULOS - dbBaixa2025")
    print("="*70)
    print("\nOpcoes disponiveis:")
    print("  1. Titulos processados HOJE (07/10/2025)")
    print("  2. Buscar por Nosso Numero")
    print("  3. Ultimos 20 titulos processados")
    print("  4. Estatisticas do dia")
    print("  5. Verificar titulo especifico (com todos os detalhes)")
    print("  0. Sair")
    print("="*70)
    
def opcao_1_titulos_hoje(conn):
    """Lista titulos processados hoje"""
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("TITULOS PROCESSADOS HOJE - 07/10/2025")
    print("="*70)
    
    cursor.execute("""
        SELECT 
            NR_NNR_TIT,
            VL_PGTO_TIT,
            DT_PGTO_TIT,
            VL_JUROS_TIT,
            DT_LIB_CRED
        FROM pcjTITULOS
        WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
        ORDER BY DT_PGTO_TIT DESC
    """)
    
    print(f"\n{'Nosso Numero':<15} {'Valor Pago':>15} {'Data Pagamento':>20} {'Juros':>12} {'Dt Credito':>20}")
    print("-"*70)
    
    count = 0
    total = 0.0
    
    for row in cursor.fetchall():
        nn = row[0]
        valor = row[1] if row[1] else 0.0
        dt_pgto = row[2]
        juros = row[3] if row[3] else 0.0
        dt_cred = row[4]
        
        print(f"{nn:<15} R$ {valor:>12,.2f} {dt_pgto} R$ {juros:>8,.2f} {dt_cred}")
        count += 1
        total += valor
        
        # Mostrar em blocos de 20
        if count % 20 == 0:
            resposta = input(f"\nMostrar mais? ({count} exibidos ate agora) [S/n]: ")
            if resposta.lower() == 'n':
                break
    
    print("-"*70)
    print(f"Total exibido: {count} titulos | Valor total: R$ {total:,.2f}")

def opcao_2_buscar_nosso_numero(conn):
    """Busca por nosso numero"""
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("BUSCAR POR NOSSO NUMERO")
    print("="*70)
    
    numero = input("\nDigite o Nosso Numero (ou parte dele): ").strip()
    
    if not numero:
        print("Numero invalido!")
        return
    
    # Buscar com LIKE
    cursor.execute(f"""
        SELECT 
            NR_NNR_TIT,
            VL_PGTO_TIT,
            DT_PGTO_TIT,
            VL_JUROS_TIT,
            DT_LIB_CRED
        FROM pcjTITULOS
        WHERE NR_NNR_TIT LIKE '%{numero}%'
        ORDER BY DT_PGTO_TIT DESC
    """)
    
    rows = cursor.fetchall()
    
    if not rows:
        print(f"\nNenhum titulo encontrado com Nosso Numero contendo: {numero}")
        return
    
    print(f"\nEncontrados {len(rows)} titulo(s):")
    print("-"*70)
    print(f"{'Nosso Numero':<15} {'Valor Pago':>15} {'Data Pagamento':>20} {'Juros':>12}")
    print("-"*70)
    
    for row in rows:
        nn = row[0]
        valor = row[1] if row[1] else 0.0
        dt_pgto = row[2]
        juros = row[3] if row[3] else 0.0
        
        print(f"{nn:<15} R$ {valor:>12,.2f} {dt_pgto} R$ {juros:>8,.2f}")

def opcao_3_ultimos_20(conn):
    """Lista ultimos 20 titulos processados"""
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("ULTIMOS 20 TITULOS PROCESSADOS")
    print("="*70)
    
    cursor.execute("""
        SELECT TOP 20
            NR_NNR_TIT,
            VL_PGTO_TIT,
            DT_PGTO_TIT,
            VL_JUROS_TIT
        FROM pcjTITULOS
        WHERE DT_PGTO_TIT IS NOT NULL
        ORDER BY DT_PGTO_TIT DESC
    """)
    
    print(f"\n{'Nosso Numero':<15} {'Valor Pago':>15} {'Data Pagamento':>20} {'Juros':>12}")
    print("-"*70)
    
    for row in cursor.fetchall():
        nn = row[0]
        valor = row[1] if row[1] else 0.0
        dt_pgto = row[2]
        juros = row[3] if row[3] else 0.0
        
        print(f"{nn:<15} R$ {valor:>12,.2f} {dt_pgto} R$ {juros:>8,.2f}")

def opcao_4_estatisticas(conn):
    """Mostra estatisticas do dia"""
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("ESTATISTICAS - 07/10/2025")
    print("="*70)
    
    # Total do dia
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(VL_PGTO_TIT) as soma_valor,
            MIN(VL_PGTO_TIT) as menor,
            MAX(VL_PGTO_TIT) as maior,
            AVG(VL_PGTO_TIT) as media
        FROM pcjTITULOS
        WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
    """)
    
    row = cursor.fetchone()
    total = row[0] if row[0] else 0
    soma = row[1] if row[1] else 0.0
    menor = row[2] if row[2] else 0.0
    maior = row[3] if row[3] else 0.0
    media = row[4] if row[4] else 0.0
    
    print(f"\nTotal de titulos processados: {total}")
    print(f"Valor total processado: R$ {soma:,.2f}")
    print(f"Menor valor: R$ {menor:,.2f}")
    print(f"Maior valor: R$ {maior:,.2f}")
    print(f"Valor medio: R$ {media:,.2f}")
    
    # Top 5 maiores
    print("\n" + "-"*70)
    print("TOP 5 MAIORES PAGAMENTOS:")
    print("-"*70)
    
    cursor.execute("""
        SELECT TOP 5
            NR_NNR_TIT,
            VL_PGTO_TIT
        FROM pcjTITULOS
        WHERE Format(DT_PGTO_TIT, 'yyyy-mm-dd') = '2025-10-07'
        ORDER BY VL_PGTO_TIT DESC
    """)
    
    print(f"{'Nosso Numero':<15} {'Valor':>15}")
    print("-"*70)
    for row in cursor.fetchall():
        print(f"{row[0]:<15} R$ {row[1]:>12,.2f}")

def opcao_5_detalhes_titulo(conn):
    """Mostra todos os detalhes de um titulo especifico"""
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("DETALHES COMPLETOS DO TITULO")
    print("="*70)
    
    numero = input("\nDigite o Nosso Numero: ").strip()
    
    if not numero:
        print("Numero invalido!")
        return
    
    cursor.execute(f"""
        SELECT *
        FROM pcjTITULOS
        WHERE NR_NNR_TIT LIKE '%{numero}%'
    """)
    
    row = cursor.fetchone()
    
    if not row:
        print(f"\nTitulo nao encontrado: {numero}")
        return
    
    # Pegar nomes das colunas
    columns = [column[0] for column in cursor.description]
    
    print("\n" + "-"*70)
    for i, col_name in enumerate(columns):
        valor = row[i]
        if valor is not None:
            print(f"{col_name:<30}: {valor}")
    print("-"*70)

def main():
    """Funcao principal"""
    try:
        conn = conectar_banco()
        print("\n Conectado ao banco dbBaixa2025.accdb com sucesso!")
        
        while True:
            menu_principal()
            
            opcao = input("\nEscolha uma opcao: ").strip()
            
            if opcao == '0':
                print("\nEncerrando...")
                break
            elif opcao == '1':
                opcao_1_titulos_hoje(conn)
            elif opcao == '2':
                opcao_2_buscar_nosso_numero(conn)
            elif opcao == '3':
                opcao_3_ultimos_20(conn)
            elif opcao == '4':
                opcao_4_estatisticas(conn)
            elif opcao == '5':
                opcao_5_detalhes_titulo(conn)
            else:
                print("\nOpcao invalida!")
            
            input("\nPressione ENTER para continuar...")
        
        conn.close()
        
    except Exception as e:
        print(f"\nErro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
