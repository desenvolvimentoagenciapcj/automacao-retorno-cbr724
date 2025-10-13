#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste e Validação
Testa todos os componentes do sistema antes da execução
"""

import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path

def testar_configuracoes():
    """Testa se as configurações estão corretas"""
    print("🔧 Testando configurações...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        erros = []
        
        # Testar diretórios
        for nome, caminho in config['diretorios'].items():
            if not os.path.exists(caminho):
                erros.append(f"Diretório '{nome}' não existe: {caminho}")
        
        # Testar banco
        if not os.path.exists(config['banco']['caminho']):
            erros.append(f"Banco Access não encontrado: {config['banco']['caminho']}")
        
        # Testar email
        if config['email']['usuario'] == 'seu_email@gmail.com':
            erros.append("Configure o email no config.yaml")
        
        if erros:
            print("❌ Erros encontrados:")
            for erro in erros:
                print(f"   - {erro}")
            return False
        else:
            print("✅ Configurações OK")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao testar configurações: {e}")
        return False

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("📦 Testando dependências...")
    
    dependencias = [
        ('watchdog', 'Monitoramento de arquivos'),
        ('pyodbc', 'Conexão com Access'),
        ('pyyaml', 'Leitura de configurações'),
        ('pandas', 'Manipulação de dados'),
        ('flask', 'Interface web'),
        ('schedule', 'Agendamento de tarefas')
    ]
    
    erros = []
    
    for modulo, descricao in dependencias:
        try:
            __import__(modulo)
            print(f"✅ {modulo} - {descricao}")
        except ImportError:
            erros.append(f"{modulo} - {descricao}")
            print(f"❌ {modulo} - {descricao}")
    
    if erros:
        print(f"\n❌ {len(erros)} dependências faltando:")
        print("Execute: pip install -r requirements.txt")
        return False
    else:
        print("✅ Todas as dependências OK")
        return True

def testar_processador_cnab():
    """Testa o processador CNAB"""
    print("📄 Testando processador CNAB...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        from processador_cnab import ProcessadorCNAB
        processador = ProcessadorCNAB(config)
        
        # Criar arquivo de teste CNAB400
        arquivo_teste = "teste_cnab400.txt"
        conteudo_teste = "0" + "1" * 399  # Header básico CNAB400
        
        with open(arquivo_teste, 'w') as f:
            f.write(conteudo_teste)
        
        # Testar validação
        resultado = processador.validar_arquivo(arquivo_teste)
        
        # Limpar arquivo de teste
        os.remove(arquivo_teste)
        
        if resultado['valido']:
            print("✅ Processador CNAB OK")
            return True
        else:
            print(f"❌ Erro no processador: {resultado.get('erro', 'Desconhecido')}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar processador CNAB: {e}")
        return False

def testar_integrador_access():
    """Testa a integração com Access"""
    print("💾 Testando integração Access...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        from integrador_access import IntegradorAccess
        integrador = IntegradorAccess(config)
        
        if integrador.testar_conexao():
            print("✅ Conexão Access OK")
            return True
        else:
            print("❌ Falha na conexão Access")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar Access: {e}")
        return False

def testar_notificador():
    """Testa o sistema de notificações"""
    print("📧 Testando notificador...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        from notificador import Notificador
        notificador = Notificador(config)
        
        # Apenas testar se as configurações estão corretas
        if (config['email']['usuario'] != 'seu_email@gmail.com' and 
            config['email']['senha'] != 'sua_senha_app'):
            print("✅ Configurações de email OK")
            
            # Perguntar se quer testar envio real
            resposta = input("Deseja testar o envio de email? (s/N): ").lower()
            if resposta == 's':
                if notificador.testar_configuracao():
                    print("✅ Teste de email enviado com sucesso!")
                else:
                    print("❌ Erro no teste de email")
                    return False
            
            return True
        else:
            print("⚠️  Configure email e senha no config.yaml")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar notificador: {e}")
        return False

def criar_arquivo_exemplo():
    """Cria um arquivo de exemplo para teste"""
    print("📝 Criando arquivo de exemplo...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pasta_entrada = config['diretorios']['entrada']
        arquivo_exemplo = os.path.join(pasta_entrada, "exemplo_retorno.txt")
        
        # Conteúdo de exemplo CNAB400
        conteudo = """01RETORNO01COBRANCA       00000000000004444444EMPRESA TESTE               341ITAU      270320210000000000000000000000000000000000000000000                                                                                                                                                                   000001
10200000000000000000000004444444000000000000000001234567890123456                         000002120032021000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000PAGADOR TESTE                                   000000000000000000000000000002
9201234          0000000010000000000000000100000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003"""
        
        with open(arquivo_exemplo, 'w', encoding='latin1') as f:
            f.write(conteudo)
        
        print(f"✅ Arquivo exemplo criado: {arquivo_exemplo}")
        print("Use este arquivo para testar o sistema")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo exemplo: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA - AUTOMAÇÃO RETORNO BANCÁRIO")
    print("=" * 60)
    
    testes = [
        ("Configurações", testar_configuracoes),
        ("Dependências", testar_dependencias),
        ("Processador CNAB", testar_processador_cnab),
        ("Integração Access", testar_integrador_access),
        ("Notificador", testar_notificador)
    ]
    
    resultados = []
    
    for nome, funcao_teste in testes:
        print(f"\n--- {nome} ---")
        try:
            resultado = funcao_teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:<20} {status}")
        if resultado:
            sucessos += 1
    
    print(f"\nResultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("Sistema pronto para uso!")
        
        # Oferecer para criar arquivo exemplo
        resposta = input("\nDeseja criar um arquivo de exemplo para teste? (s/N): ").lower()
        if resposta == 's':
            criar_arquivo_exemplo()
        
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM!")
        print("Corrija os problemas antes de usar o sistema.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()