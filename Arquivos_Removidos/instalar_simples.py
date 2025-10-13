#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Simplificado
Prepara o ambiente para execução do sistema MVP
"""

import os
import sys
import subprocess
from pathlib import Path

def verificar_python():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        return False
    
    print("✅ Versão do Python OK")
    return True

def instalar_dependencias():
    """Instala dependências básicas"""
    print("\n📦 Instalando dependências...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências:")
        print(e.stderr)
        return False

def criar_diretorios():
    """Cria estrutura de diretórios"""
    print("\n📁 Criando diretórios...")
    
    diretorios = [
        "D:\\Retornos\\Entrada",
        "D:\\Retornos\\Processados",
        "D:\\Retornos\\Erro",
        "D:\\Retornos\\Backup",
        "logs"
    ]
    
    for diretorio in diretorios:
        Path(diretorio).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {diretorio}")
    
    print("✅ Diretórios criados!")

def verificar_access_driver():
    """Verifica driver do Access"""
    print("\n🔍 Verificando driver Access...")
    
    try:
        import pyodbc
        drivers = [x for x in pyodbc.drivers() if 'Access' in x]
        
        if drivers:
            print(f"✅ Driver encontrado: {drivers[0]}")
            return True
        else:
            print("⚠️  Driver Access não encontrado!")
            print("📥 Baixe em: https://www.microsoft.com/download/details.aspx?id=54920")
            return False
    except ImportError:
        print("⚠️  pyodbc não instalado ainda")
        return False

def criar_script_bat():
    """Cria script .bat para execução"""
    print("\n📝 Criando script de inicialização...")
    
    script = """@echo off
title Monitor de Retorno Bancario
echo.
echo ========================================
echo    MONITOR DE RETORNO BANCARIO
echo ========================================
echo.
cd /d "%~dp0"
python monitor_arquivos_simples.py
pause
"""
    
    with open("iniciar.bat", "w", encoding="utf-8") as f:
        f.write(script)
    
    print("✅ Script 'iniciar.bat' criado!")

def main():
    """Instalação principal"""
    print("=" * 60)
    print("🔧 INSTALAÇÃO SIMPLIFICADA - RETORNO BANCÁRIO MVP")
    print("=" * 60 + "\n")
    
    if not verificar_python():
        return
    
    instalar_dependencias()
    criar_diretorios()
    verificar_access_driver()
    criar_script_bat()
    
    print("\n" + "=" * 60)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. ✏️  Edite 'config.yaml' e configure o caminho do banco Access")
    print("2. 🧪 Execute 'python testar_simples.py' para validar")
    print("3. 🚀 Execute 'iniciar.bat' para iniciar o monitor")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()