#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação e Configuração
Automatiza a instalação das dependências e configuração inicial
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_python():
    """Verifica se o Python está instalado e a versão"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8 ou superior é necessário!")
            print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Python: {e}")
        return False

def instalar_dependencias():
    """Instala as dependências do Python"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Atualizar pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar dependências do requirements.txt
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print("Tente executar manualmente:")
        print("pip install -r requirements.txt")
        return False

def criar_estrutura_diretorios():
    """Cria a estrutura de diretórios necessária"""
    print("\n📁 Criando estrutura de diretórios...")
    
    diretorios = [
        "D:\\Retornos\\Entrada",
        "D:\\Retornos\\Processados", 
        "D:\\Retornos\\Erro",
        "D:\\Retornos\\Backup",
        "logs"
    ]
    
    for diretorio in diretorios:
        try:
            Path(diretorio).mkdir(parents=True, exist_ok=True)
            print(f"✅ {diretorio}")
        except Exception as e:
            print(f"⚠️  Erro ao criar {diretorio}: {e}")
    
    print("✅ Estrutura de diretórios criada!")

def configurar_banco_access():
    """Verifica e configura a conexão com o banco Access"""
    print("\n💾 Verificando banco Access...")
    
    # Verificar se o Access Database Engine está instalado
    try:
        import pyodbc
        drivers = [x for x in pyodbc.drivers() if 'Access' in x]
        
        if drivers:
            print(f"✅ Driver Access encontrado: {drivers[0]}")
        else:
            print("⚠️  Driver Access não encontrado!")
            print("Instale o Microsoft Access Database Engine 2016 Redistributable")
            print("https://www.microsoft.com/en-us/download/details.aspx?id=54920")
    
    except ImportError:
        print("⚠️  pyodbc não instalado. Execute: pip install pyodbc")

def criar_scripts_inicializacao():
    """Cria scripts para facilitar a inicialização"""
    print("\n🚀 Criando scripts de inicialização...")
    
    # Script para Windows
    script_bat = """@echo off
echo Iniciando Sistema de Automacao de Retorno Bancario...
echo.
cd /d "%~dp0"
python monitor_arquivos.py
pause
"""
    
    with open("iniciar_monitor.bat", "w", encoding="utf-8") as f:
        f.write(script_bat)
    
    # Script para dashboard
    dashboard_bat = """@echo off
echo Iniciando Dashboard Web...
echo.
cd /d "%~dp0"
python dashboard.py
pause
"""
    
    with open("iniciar_dashboard.bat", "w", encoding="utf-8") as f:
        f.write(dashboard_bat)
    
    print("✅ Scripts de inicialização criados:")
    print("   - iniciar_monitor.bat (Monitor de arquivos)")
    print("   - iniciar_dashboard.bat (Interface web)")

def criar_servico_windows():
    """Cria um serviço do Windows para o monitor"""
    print("\n🔧 Para executar como serviço do Windows:")
    print("1. Instale o NSSM (Non-Sucking Service Manager)")
    print("2. Execute como administrador:")
    print(f"   nssm install RetornoBancario {os.path.abspath('monitor_arquivos.py')}")
    print("3. Configure o serviço para iniciar automaticamente")

def validar_configuracoes():
    """Valida as configurações do arquivo config.yaml"""
    print("\n⚙️  Validando configurações...")
    
    try:
        import yaml
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Verificar configurações críticas
        if not os.path.exists(config['banco']['caminho']):
            print(f"⚠️  Banco Access não encontrado: {config['banco']['caminho']}")
            print("   Atualize o caminho no arquivo config.yaml")
        else:
            print("✅ Banco Access encontrado")
        
        # Verificar email
        if not config['email']['usuario'] or config['email']['usuario'] == 'seu_email@gmail.com':
            print("⚠️  Configure o email no arquivo config.yaml")
        else:
            print("✅ Configurações de email definidas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao validar configurações: {e}")
        return False

def main():
    """Função principal de instalação"""
    print("=" * 60)
    print("🏦 INSTALAÇÃO - SISTEMA DE AUTOMAÇÃO RETORNO BANCÁRIO")
    print("=" * 60)
    
    # Verificações iniciais
    if not verificar_python():
        return False
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n⚠️  Algumas dependências podem não ter sido instaladas.")
        print("Verifique manualmente executando: pip install -r requirements.txt")
    
    # Criar estrutura
    criar_estrutura_diretorios()
    
    # Configurar Access
    configurar_banco_access()
    
    # Criar scripts
    criar_scripts_inicializacao()
    
    # Validar configurações
    validar_configuracoes()
    
    # Instruções finais
    print("\n" + "=" * 60)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Edite o arquivo 'config.yaml' com suas configurações")
    print("2. Configure o caminho do banco Access")
    print("3. Configure as credenciais de email")
    print("4. Execute 'iniciar_monitor.bat' para iniciar o monitoramento")
    print("5. Execute 'iniciar_dashboard.bat' para acessar a interface web")
    print("\n🌐 Dashboard Web: http://localhost:5000")
    print("👤 Senha padrão: admin123 (ALTERE no config.yaml)")
    
    # Criar serviço Windows
    criar_servico_windows()
    
    print("\n🎉 Sistema pronto para uso!")
    return True

if __name__ == "__main__":
    main()