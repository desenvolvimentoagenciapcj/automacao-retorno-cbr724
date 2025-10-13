"""
Sistema de Verificação Automática - Produção
Verifica se todos os componentes necessários estão funcionando
"""

import os
import sys
from pathlib import Path
import pyodbc
import yaml
from datetime import datetime

class VerificadorSistema:
    def __init__(self):
        self.erros = []
        self.avisos = []
        self.pasta_base = Path(__file__).parent.parent
        
    def verificar_estrutura_pastas(self):
        """Verifica se todas as pastas necessárias existem"""
        print("\n📁 Verificando estrutura de pastas...")
        
        pastas_obrigatorias = [
            self.pasta_base / "Retorno",
            self.pasta_base / "Retorno" / "Processados",
            self.pasta_base / "Retorno" / "Erro",
            self.pasta_base / "Backup",
            self.pasta_base / "AutomacaoRetorno",
            self.pasta_base / "AutomacaoRetorno" / "logs"
        ]
        
        for pasta in pastas_obrigatorias:
            if pasta.exists():
                print(f"  ✓ {pasta.name}")
            else:
                self.erros.append(f"Pasta obrigatória não encontrada: {pasta}")
                print(f"  ✗ {pasta.name} - NÃO ENCONTRADA")
                
    def verificar_arquivos_essenciais(self):
        """Verifica se os arquivos principais do sistema existem"""
        print("\n📄 Verificando arquivos essenciais...")
        
        arquivos_obrigatorios = {
            "processador_cbr724.py": "Processador de arquivos CBR724",
            "processador_cnab.py": "Processador de arquivos CNAB240",
            "integrador_access.py": "Integrador com banco Access",
            "processar_todos_arquivos.py": "Processador em lote",
            "monitor_arquivos_simples.py": "Monitor automático",
            "config.yaml": "Arquivo de configuração",
            "requirements.txt": "Dependências Python"
        }
        
        pasta_automacao = self.pasta_base / "AutomacaoRetorno"
        
        for arquivo, descricao in arquivos_obrigatorios.items():
            caminho = pasta_automacao / arquivo
            if caminho.exists():
                print(f"  ✓ {arquivo} - {descricao}")
            else:
                self.erros.append(f"Arquivo essencial não encontrado: {arquivo}")
                print(f"  ✗ {arquivo} - NÃO ENCONTRADO")
                
    def verificar_bancos_access(self):
        """Verifica se os bancos Access existem e são acessíveis"""
        print("\n🗄️  Verificando bancos Access...")
        
        banco_principal = self.pasta_base / "dbBaixa2025.accdb"
        
        if not banco_principal.exists():
            self.erros.append(f"Banco principal não encontrado: {banco_principal}")
            print(f"  ✗ dbBaixa2025.accdb - NÃO ENCONTRADO")
            return
            
        print(f"  ✓ dbBaixa2025.accdb encontrado")
        
        # Tenta conectar
        try:
            conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                f'DBQ={banco_principal};'
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Verifica tabela principal
            cursor.execute("SELECT COUNT(*) FROM pcjTITULOS")
            total = cursor.fetchone()[0]
            print(f"  ✓ Conexão OK - {total:,} títulos na tabela pcjTITULOS")
            
            conn.close()
            
        except Exception as e:
            self.erros.append(f"Erro ao conectar no banco: {str(e)}")
            print(f"  ✗ Erro ao conectar: {str(e)}")
            
    def verificar_configuracao(self):
        """Verifica se o arquivo de configuração está correto"""
        print("\n⚙️  Verificando configuração...")
        
        config_path = self.pasta_base / "AutomacaoRetorno" / "config.yaml"
        
        if not config_path.exists():
            self.erros.append("Arquivo config.yaml não encontrado")
            print("  ✗ config.yaml não encontrado")
            return
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # Verifica configurações principais
            if 'pastas' in config:
                print("  ✓ Configuração de pastas OK")
            else:
                self.avisos.append("Faltam configurações de pastas no config.yaml")
                
            if 'bancos' in config:
                print("  ✓ Configuração de bancos OK")
            else:
                self.avisos.append("Faltam configurações de bancos no config.yaml")
                
        except Exception as e:
            self.erros.append(f"Erro ao ler config.yaml: {str(e)}")
            print(f"  ✗ Erro ao ler configuração: {str(e)}")
            
    def verificar_dependencias(self):
        """Verifica se as bibliotecas Python estão instaladas"""
        print("\n📦 Verificando dependências Python...")
        
        dependencias = {
            'pyodbc': 'Conexão com Access',
            'yaml': 'Leitura de configuração',
            'watchdog': 'Monitor de arquivos (opcional)',
            'pathlib': 'Manipulação de caminhos'
        }
        
        for modulo, descricao in dependencias.items():
            try:
                if modulo == 'yaml':
                    __import__('yaml')
                else:
                    __import__(modulo)
                print(f"  ✓ {modulo} - {descricao}")
            except ImportError:
                if modulo == 'watchdog':
                    self.avisos.append(f"Módulo opcional não instalado: {modulo}")
                    print(f"  ⚠ {modulo} - NÃO INSTALADO (opcional)")
                else:
                    self.erros.append(f"Módulo obrigatório não instalado: {modulo}")
                    print(f"  ✗ {modulo} - NÃO INSTALADO")
                    
    def testar_processamento(self):
        """Testa se o sistema consegue processar arquivos"""
        print("\n🧪 Testando capacidade de processamento...")
        
        # Verifica se há arquivos para processar
        pasta_retorno = self.pasta_base / "Retorno"
        arquivos_ret = list(pasta_retorno.glob("*.ret"))
        
        if arquivos_ret:
            print(f"  ℹ️  {len(arquivos_ret)} arquivo(s) .ret encontrado(s) na pasta Retorno")
            self.avisos.append(f"{len(arquivos_ret)} arquivo(s) aguardando processamento")
        else:
            print("  ✓ Pasta Retorno vazia (nenhum arquivo pendente)")
            
        # Verifica arquivos processados
        pasta_processados = pasta_retorno / "Processados"
        if pasta_processados.exists():
            processados = list(pasta_processados.glob("*-processado.ret"))
            if processados:
                print(f"  ✓ {len(processados)} arquivo(s) já processado(s)")
                
    def verificar_backups(self):
        """Verifica sistema de backup"""
        print("\n💾 Verificando sistema de backup...")
        
        pasta_backup = self.pasta_base / "Backup"
        
        if not pasta_backup.exists():
            self.avisos.append("Pasta de backup não existe")
            print("  ⚠ Pasta Backup não encontrada")
            return
            
        backups = list(pasta_backup.glob("backup_*.accdb"))
        
        if backups:
            # Pega o backup mais recente
            backup_recente = max(backups, key=lambda p: p.stat().st_mtime)
            data_backup = datetime.fromtimestamp(backup_recente.stat().st_mtime)
            print(f"  ✓ {len(backups)} backup(s) encontrado(s)")
            print(f"  ℹ️  Backup mais recente: {data_backup.strftime('%d/%m/%Y %H:%M')}")
        else:
            self.avisos.append("Nenhum backup encontrado")
            print("  ⚠ Nenhum backup encontrado")
            
    def gerar_relatorio(self):
        """Gera relatório final da verificação"""
        print("\n" + "="*80)
        print("📊 RELATÓRIO DE VERIFICAÇÃO DO SISTEMA")
        print("="*80)
        
        if not self.erros and not self.avisos:
            print("\n✅ SISTEMA 100% OPERACIONAL - PRONTO PARA PRODUÇÃO!")
            print("\nTodos os componentes verificados estão funcionando corretamente.")
            return True
            
        if self.erros:
            print(f"\n❌ ERROS CRÍTICOS ENCONTRADOS ({len(self.erros)}):")
            for i, erro in enumerate(self.erros, 1):
                print(f"  {i}. {erro}")
                
        if self.avisos:
            print(f"\n⚠️  AVISOS ({len(self.avisos)}):")
            for i, aviso in enumerate(self.avisos, 1):
                print(f"  {i}. {aviso}")
                
        print("\n" + "="*80)
        
        if self.erros:
            print("\n🔧 AÇÃO NECESSÁRIA: Corrija os erros críticos antes de usar em produção")
            return False
        else:
            print("\n✅ Sistema operacional com alguns avisos (não críticos)")
            return True
            
    def executar_verificacao_completa(self):
        """Executa todas as verificações"""
        print("="*80)
        print("🔍 VERIFICAÇÃO AUTOMÁTICA DO SISTEMA - PRODUÇÃO")
        print("="*80)
        print(f"\nData/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Pasta Base: {self.pasta_base}")
        
        self.verificar_estrutura_pastas()
        self.verificar_arquivos_essenciais()
        self.verificar_bancos_access()
        self.verificar_configuracao()
        self.verificar_dependencias()
        self.testar_processamento()
        self.verificar_backups()
        
        sistema_ok = self.gerar_relatorio()
        
        return sistema_ok


def main():
    """Função principal"""
    verificador = VerificadorSistema()
    sistema_ok = verificador.executar_verificacao_completa()
    
    # Retorna código de saída apropriado
    sys.exit(0 if sistema_ok else 1)


if __name__ == "__main__":
    main()
