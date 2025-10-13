"""
Teste específico do arquivo CBR7246250110202521616_id.ret
"""
import sys
import os
import shutil
from datetime import datetime
sys.path.append(r'D:\Teste_Cobrança_Acess\AutomacaoRetorno')

from processador_cbr724 import ProcessadorCBR724
from integrador_access import IntegradorAccess

print("\n" + "="*80)
print("TESTE: CBR7246250110202521616_id.ret")
print("="*80 + "\n")

arquivo = r"D:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret"

# Configuração dos bancos
config = {
    'bancos': {
        'baixa': {
            'caminho': r'D:/Teste_Cobrança_Acess/dbBaixa2025.accdb',
            'habilitado': True
        },
        'cobranca': {
            'caminho': r'D:/Teste_Cobrança_Acess/Cobranca2019.accdb',
            'habilitado': False
        }
    }
}

try:
    # 1. Criar backup
    print("📦 Criando backup do banco...")
    backup_dir = r'D:\Teste_Cobrança_Acess\Backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}_dbBaixa2025.accdb')
    shutil.copy2(config['bancos']['baixa']['caminho'].replace('/', '\\'), backup_path)
    print(f"✓ Backup: {backup_path}\n")
    
    # 2. Processar arquivo CBR724
    print("📄 Processando arquivo CBR724...")
    processador = ProcessadorCBR724()
    registros = processador.processar_arquivo(arquivo)
    
    print(f"✅ {len(registros)} registros extraídos do arquivo\n")
    
    # Mostrar títulos encontrados
    print("TÍTULOS ENCONTRADOS:")
    for i, reg in enumerate(registros, 1):
        print(f"\n{i}. Nosso Número: {reg.get('nosso_numero', 'N/A')}")
        print(f"   Valor: R$ {reg.get('valor', 0):,.2f}")
        print(f"   Data: {reg.get('data_pagamento', 'N/A')}")
    
    # 3. Integrar com Access
    print("\n" + "="*80)
    print("💾 Integrando com banco Access...")
    print("="*80 + "\n")
    
    integrador = IntegradorAccess(config)
    resultado = integrador.processar_registros(registros)
    
    print("\n" + "="*80)
    print("RESULTADO DO PROCESSAMENTO:")
    print("="*80)
    
    if isinstance(resultado, dict):
        print(f"✅ Registros processados: {resultado.get('processados', 'N/A')}")
        print(f"💰 Baixas realizadas: {resultado.get('baixas_realizadas', 'N/A')}")
        print(f"🔄 Atualizações: {resultado.get('atualizacoes', 'N/A')}")
        print(f"❌ Erros: {resultado.get('erros', 'N/A')}")
        print(f"🔍 Não encontrados: {resultado.get('nao_encontrados', 'N/A')}")
        
        if resultado.get('nao_encontrados', 0) > 0:
            print("\n⚠️ TÍTULOS NÃO ENCONTRADOS:")
            for titulo in resultado.get('detalhes_nao_encontrados', []):
                print(f"   • {titulo}")
    else:
        print(f"Resultado: {resultado}")
    
    print("\n" + "="*80)
    print("✅ TESTE CONCLUÍDO!")
    print("="*80 + "\n")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
