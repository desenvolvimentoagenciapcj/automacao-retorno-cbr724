"""
Processar apenas um arquivo específico usando o monitor
"""
import os
import shutil
from datetime import datetime
from processador_cbr724 import ProcessadorCBR724
from integrador_access import IntegradorAccess
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Configuração
arquivo = r"D:\Teste_Cobrança_Acess\Retorno\teste_unico.ret"
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

print("\n" + "="*80)
print("🔄 PROCESSANDO: teste_unico.ret (CBR7246250110202521616)")
print("="*80)

# 1. Backup
print("📦 Criando backup dos bancos...")
backup_dir = r'D:\Teste_Cobrança_Acess\Backup'
os.makedirs(backup_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = os.path.join(backup_dir, f'backup_{timestamp}_dbBaixa2025.accdb')
shutil.copy2(config['bancos']['baixa']['caminho'].replace('/', '\\'), backup_path)
logger.info(f"✓ Backup dbBaixa2025: {backup_path}")

# 2. Processar CBR724
print("📄 Processando arquivo CBR724 (160 caracteres)...")
logger.info(f"Processando arquivo CBR724: {arquivo}")

processador = ProcessadorCBR724()
registros = processador.processar_arquivo(arquivo)

logger.info(f"Processados {len(registros)} títulos CBR724 (tipo 7 + tipo 37)")
print(f"✅ {len(registros)} registros encontrados")

# 3. Integrar com Access
print("💾 Integrando com banco Access...")
integrador = IntegradorAccess(config)
resultado = integrador.processar_registros(registros)

# 4. Exibir resultado
print("\n" + "="*80)
print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
print("="*80)

if isinstance(resultado, tuple) and len(resultado) >= 2:
    processados, baixas = resultado[0], resultado[1]
    print(f"📊 Registros processados: {processados}")
    print(f"💰 Baixas realizadas: {baixas}")
else:
    print(f"Resultado: {resultado}")

print("="*80 + "\n")
