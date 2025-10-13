#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa TODOS os arquivos .ret da pasta Retorno
Para cada arquivo processado com sucesso:
- Adiciona sufixo "-processado" no nome
- Move para pasta Processados
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from processador_cnab import ProcessadorCNAB
from processador_cbr724 import ProcessadorCBR724
from integrador_access import IntegradorAccess

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuração
config = {
    'bancos': {
        'baixa': {
            'caminho': r'D:/Teste_Cobrança_Acess/dbBaixa2025.accdb',
            'habilitado': True
        },
        'cobranca': {
            'caminho': r'D:/Teste_Cobrança_Acess/Cobranca2019.accdb',
            'ativo': False
        }
    },
    'diretorios': {
        'entrada': r'D:\Teste_Cobrança_Acess\Retorno',
        'processados': r'D:\Teste_Cobrança_Acess\Retorno\Processados',
        'erro': r'D:\Teste_Cobrança_Acess\Retorno\Erro',
        'backup': r'D:\Teste_Cobrança_Acess\Backup'
    }
}

def detectar_tipo_arquivo(caminho_arquivo):
    """Detecta se é CBR724 ou CNAB240 pelo tamanho da linha"""
    try:
        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            primeira_linha = f.readline().rstrip('\n\r')
            tamanho = len(primeira_linha)
            
            # CBR724: 160 caracteres, contém "CBR724" no header
            if tamanho == 160 and 'CBR' in primeira_linha:
                return 'CBR724'
            # CNAB240: 240 caracteres, começa com '0'
            elif tamanho == 240 and primeira_linha[0] == '0':
                return 'CNAB240'
            else:
                return 'DESCONHECIDO'
    except Exception as e:
        logger.error(f"Erro ao detectar tipo: {e}")
        return 'ERRO'

def processar_arquivo(caminho_arquivo):
    """Processa um arquivo individual"""
    nome_arquivo = os.path.basename(caminho_arquivo)
    
    print(f"\n{'='*80}")
    print(f">>> PROCESSANDO: {nome_arquivo}")
    print(f"{'='*80}")
    
    try:
        # Detectar tipo
        tipo = detectar_tipo_arquivo(caminho_arquivo)
        logger.info(f"Tipo detectado: {tipo}")
        
        if tipo == 'DESCONHECIDO' or tipo == 'ERRO':
            logger.warning(f"Arquivo {nome_arquivo} - tipo não suportado ou erro")
            return False
        
        # Fazer backup
        print(">> Criando backup dos bancos...")
        integrador = IntegradorAccess(config)
        backups = integrador.fazer_backup()
        
        # Processar conforme o tipo
        print(f">> Processando arquivo {tipo}...")
        
        if tipo == 'CBR724':
            processador = ProcessadorCBR724()
        else:  # CNAB240
            processador = ProcessadorCNAB()
        
        registros = processador.processar_arquivo(caminho_arquivo)
        
        if not registros:
            logger.warning(f"Nenhum registro encontrado em {nome_arquivo}")
            return False
        
        print(f"OK - {len(registros)} registros encontrados")
        
        # Integrar com Access
        print(">> Integrando com banco Access...")
        resultado = integrador.processar_registros(registros)
        
        # Exibir resultado
        print(f"\n{'='*80}")
        print(f">>> PROCESSAMENTO CONCLUIDO COM SUCESSO!")
        print(f"{'='*80}")
        print(f"Resultado: {resultado}")
        print(f"{'='*80}\n")
        
        return True
        
    except Exception as e:
        logger.error(f"ERRO ao processar {nome_arquivo}: {e}")
        print(f"\n{'='*80}")
        print(f">>> ERRO NO PROCESSAMENTO!")
        print(f"{'='*80}")
        print(f"Erro: {str(e)}")
        print(f"{'='*80}\n")
        return False

def main():
    """Processa todos os arquivos .ret"""
    
    pasta_retorno = Path(config['diretorios']['entrada'])
    pasta_processados = Path(config['diretorios']['processados'])
    pasta_erro = Path(config['diretorios']['erro'])
    
    # Criar pastas se não existirem
    pasta_processados.mkdir(parents=True, exist_ok=True)
    pasta_erro.mkdir(parents=True, exist_ok=True)
    
    # Listar todos os arquivos .ret
    arquivos = list(pasta_retorno.glob('*.ret'))
    
    if not arquivos:
        print("\nNenhum arquivo .ret encontrado na pasta Retorno")
        return
    
    print(f"\n{'='*80}")
    print(f">>> PROCESSAMENTO EM LOTE")
    print(f"{'='*80}")
    print(f"Pasta: {pasta_retorno}")
    print(f"Total de arquivos: {len(arquivos)}")
    print(f"{'='*80}\n")
    
    # Contadores
    total = len(arquivos)
    sucesso = 0
    erro = 0
    
    # Processar cada arquivo
    for i, arquivo in enumerate(arquivos, 1):
        nome_original = arquivo.name
        
        print(f"\n[{i}/{total}] Processando: {nome_original}")
        
        # Processar
        resultado = processar_arquivo(str(arquivo))
        
        if resultado:
            # SUCESSO: Adicionar "-processado" e mover para Processados
            nome_sem_ext = arquivo.stem
            extensao = arquivo.suffix
            novo_nome = f"{nome_sem_ext}-processado{extensao}"
            
            destino = pasta_processados / novo_nome
            
            try:
                shutil.move(str(arquivo), str(destino))
                print(f"OK - Movido para: Processados/{novo_nome}")
                sucesso += 1
            except Exception as e:
                logger.error(f"Erro ao mover arquivo: {e}")
                erro += 1
        else:
            # ERRO: Mover para pasta Erro (sem renomear)
            destino = pasta_erro / nome_original
            
            try:
                shutil.move(str(arquivo), str(destino))
                print(f"ERRO - Movido para: Erro/{nome_original}")
                erro += 1
            except Exception as e:
                logger.error(f"Erro ao mover arquivo com erro: {e}")
    
    # Resumo final
    print(f"\n{'='*80}")
    print(f">>> RESUMO DO PROCESSAMENTO EM LOTE")
    print(f"{'='*80}")
    print(f"Total de arquivos: {total}")
    print(f"Processados com sucesso: {sucesso}")
    print(f"Com erro: {erro}")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
