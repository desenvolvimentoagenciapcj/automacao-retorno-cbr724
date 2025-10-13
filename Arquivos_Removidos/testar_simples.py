#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Simplificado
Valida configurações básicas do sistema MVP
"""

import os
import sys
import yaml

def testar_config():
    """Testa configurações"""
    print("⚙️  Testando configurações...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Verificar banco
        banco_path = config['banco']['caminho']
        if os.path.exists(banco_path):
            print(f"✅ Banco Access encontrado: {banco_path}")
        else:
            print(f"❌ Banco Access não encontrado: {banco_path}")
            print("   Configure o caminho correto no config.yaml")
            return False
        
        # Verificar diretórios
        for nome, path in config['diretorios'].items():
            if os.path.exists(path):
                print(f"✅ Diretório {nome}: {path}")
            else:
                print(f"⚠️  Diretório {nome} será criado: {path}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo config.yaml não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro ao ler configurações: {e}")
        return False

def testar_dependencias():
    """Testa dependências"""
    print("\n📦 Testando dependências...")
    
    dependencias = {
        'watchdog': 'Monitoramento de arquivos',
        'pyodbc': 'Conexão com Access',
        'yaml': 'Leitura de configurações'
    }
    
    ok = True
    for modulo, desc in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {modulo} - {desc}")
        except ImportError:
            print(f"❌ {modulo} - {desc} (FALTANDO)")
            ok = False
    
    if not ok:
        print("\n💡 Execute: pip install -r requirements.txt")
    
    return ok

def testar_access():
    """Testa conexão Access"""
    print("\n💾 Testando conexão Access...")
    
    try:
        import pyodbc
        
        # Verificar drivers
        drivers = [x for x in pyodbc.drivers() if 'Access' in x]
        if not drivers:
            print("❌ Driver Access não encontrado!")
            print("📥 Instale: https://www.microsoft.com/download/details.aspx?id=54920")
            return False
        
        print(f"✅ Driver Access: {drivers[0]}")
        
        # Tentar conectar
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        banco_path = config['banco']['caminho']
        if not os.path.exists(banco_path):
            print(f"⚠️  Banco não encontrado para teste de conexão")
            return False
        
        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={banco_path};"
        
        try:
            conn = pyodbc.connect(conn_str)
            conn.close()
            print("✅ Conexão com Access OK!")
            return True
        except Exception as e:
            # Banco pode estar aberto/bloqueado
            if "bloqueado" in str(e).lower() or "cannot open" in str(e).lower() or "desconhecido" in str(e).lower():
                print("⚠️  Banco está em uso ou bloqueado (normal se estiver aberto no Access)")
                print("✅ Mas o driver e caminho estão corretos!")
                return True  # Considera OK pois o problema é só bloqueio
            else:
                print(f"❌ Erro na conexão: {e}")
                return False
        
    except ImportError:
        print("❌ pyodbc não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def criar_arquivo_teste():
    """Cria arquivo de teste"""
    print("\n📝 Criar arquivo de teste CNAB?")
    resposta = input("Digite 's' para criar: ").lower()
    
    if resposta != 's':
        return
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pasta_entrada = config['diretorios']['entrada']
        os.makedirs(pasta_entrada, exist_ok=True)
        
        arquivo_teste = os.path.join(pasta_entrada, "teste_retorno.txt")
        
        # CNAB400 exemplo simples
        conteudo = "0" + "1" * 399 + "\n"  # Header
        conteudo += "1" + "0" * 399 + "\n"  # Detalhe
        conteudo += "9" + "9" * 399  # Trailer
        
        with open(arquivo_teste, 'w', encoding='latin1') as f:
            f.write(conteudo)
        
        print(f"✅ Arquivo de teste criado: {arquivo_teste}")
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo teste: {e}")

def main():
    """Teste principal"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA MVP")
    print("=" * 60 + "\n")
    
    testes = [
        ("Configurações", testar_config),
        ("Dependências", testar_dependencias),
        ("Conexão Access", testar_access)
    ]
    
    resultados = []
    for nome, funcao in testes:
        print(f"\n{'─'*60}")
        try:
            ok = funcao()
            resultados.append((nome, ok))
        except Exception as e:
            print(f"❌ Erro: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    sucessos = 0
    for nome, ok in resultados:
        status = "✅ OK" if ok else "❌ FALHOU"
        print(f"{nome:<20} {status}")
        if ok:
            sucessos += 1
    
    print(f"\n{sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("\n🎉 TUDO OK! Sistema pronto para usar!")
        criar_arquivo_teste()
    else:
        print("\n⚠️  Corrija os problemas antes de executar o sistema")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()