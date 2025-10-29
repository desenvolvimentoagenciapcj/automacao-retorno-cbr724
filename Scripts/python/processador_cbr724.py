#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de arquivos CBR724
Formato customizado de 160 caracteres por linha
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Any

class ProcessadorCBR724:
    """Processador para arquivos de retorno no formato CBR724"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def processar_arquivo(self, caminho_arquivo: str) -> List[Dict[str, Any]]:
        """Processa arquivo CBR724 e retorna lista de registros"""
        try:
            self.logger.info(f"Processando arquivo CBR724: {caminho_arquivo}")
            
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                linhas = f.readlines()
            
            # Extrair data do arquivo (linha tipo 28, posições 115-122: DDMMAAAA)
            # Conforme VBA: DataArquivo = Mid(MyString, 115, 2) & "/" & Mid(MyString, 117, 2) & "/" & Mid(MyString, 119, 4)
            data_arquivo = None
            for linha in linhas:
                if linha.startswith('28') and len(linha) >= 123:
                    try:
                        data_str = linha[114:122].strip()  # Posições 115-122 (índice 114-121)
                        if data_str and len(data_str) == 8:
                            dia = int(data_str[0:2])
                            mes = int(data_str[2:4])
                            ano = int(data_str[4:8])
                            data_arquivo = datetime(ano, mes, dia)
                            self.logger.info(f"📅 Data do arquivo extraída: {data_arquivo.strftime('%d/%m/%Y')}")
                            break
                    except (ValueError, IndexError) as e:
                        self.logger.warning(f"Erro ao extrair data do arquivo: {e}")
            
            if not data_arquivo:
                self.logger.warning("Data do arquivo não encontrada, usando data atual")
                data_arquivo = datetime.now()
            
            registros = []
            
            for numero_linha, linha in enumerate(linhas, 1):
                linha = linha.rstrip('\n\r')
                
                # Ignorar linhas vazias
                if not linha.strip():
                    continue
                
                # Processar registros tipo 7 (layout antigo - 160 chars)
                if linha.startswith(' 7') and len(linha) == 160:
                    try:
                        registro = self._processar_titulo_tipo7(linha, data_arquivo)
                        if registro:
                            registros.append(registro)
                    except Exception as e:
                        self.logger.warning(f"Erro na linha {numero_linha} (tipo 7): {e}")
                
                # Processar registros tipo 37 (layout novo - maioria dos títulos)
                elif linha.startswith('37') and len(linha) >= 100:
                    try:
                        registro = self._processar_titulo_tipo37(linha, data_arquivo)
                        if registro:
                            registros.append(registro)
                    except Exception as e:
                        self.logger.warning(f"Erro na linha {numero_linha} (tipo 37): {e}")
            
            self.logger.info(f"Processados {len(registros)} títulos CBR724 (tipo 7 + tipo 37)")
            return registros
            
        except Exception as e:
            self.logger.error(f"Erro ao processar arquivo CBR724: {e}")
            raise
    
    def _processar_titulo_tipo37(self, linha: str, data_arquivo: datetime) -> Dict[str, Any]:
        """Processa registro tipo 37 (layout principal - maioria dos títulos)
        
        Layout REAL tipo 37:
        Posição  Tamanho  Campo
        -------  -------  -----
        0-2      2        Tipo registro ('37')
        3-20     17       Código banco
        21-32    12       Sequencial
        33-37    5        Nosso número ← CAMPO PRINCIPAL
        38-65    28       Nome do cliente
        66-74    8        Data vencimento (DDMMAAAA)
        75-90    16       Informações adicionais
        90-110   20       Valor pago (formato: 3.898,83)
        """
        try:
            # Extrair campos conforme layout REAL
            tipo = linha[0:2].strip()
            codigo_banco = linha[3:21].strip()
            
            # Nosso Número: posição 33-37 (5 chars)
            nosso_numero_raw = linha[33:38].strip()
            nosso_numero = nosso_numero_raw.lstrip('0') if nosso_numero_raw else nosso_numero_raw
            
            # PULAR registros sem Nosso Número
            if not nosso_numero or not nosso_numero.isdigit():
                self.logger.debug(f"Registro tipo 37 sem Nosso Número válido - ignorado: '{nosso_numero_raw}'")
                return None
            
            nome_cliente = linha[38:66].strip()
            data_venc_str = linha[66:74].strip()
            
            # Resto da linha para buscar valores (após posição 90)
            resto = linha[90:] if len(linha) > 90 else ''
            
            # Extrair valor (formato brasileiro: 3.898,83)
            valor_pago = 0.0
            valor_match = re.search(r'(\d{1,10}\.?\d{0,3},\d{2})', resto)
            if valor_match:
                valor_str = valor_match.group(1)
                # Converter formato brasileiro para float
                valor_pago = float(valor_str.replace('.', '').replace(',', '.'))
            
            # Converter data vencimento (DDMMAAAA)
            data_vencimento = None
            if data_venc_str and len(data_venc_str) == 8:
                try:
                    dia = int(data_venc_str[0:2])
                    mes = int(data_venc_str[2:4])
                    ano = int(data_venc_str[4:8])
                    data_vencimento = datetime(ano, mes, dia)
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"Erro ao converter data '{data_venc_str}': {e}")
            
            # Data de ocorrência = data do arquivo (conforme VBA)
            data_ocorrencia = data_arquivo
            
            # Criar registro
            registro = {
                'tipo_registro': tipo,
                'codigo_banco': codigo_banco,
                'nosso_numero': nosso_numero,
                'nome_cliente': nome_cliente,
                'data_vencimento': data_vencimento,
                'tipo_documento': 'CBR',
                'valor_pago': valor_pago,
                'data_ocorrencia': data_ocorrencia,
                'data_credito': data_ocorrencia,
                'codigo_ocorrencia': '06',  # Liquidação
                'descricao_ocorrencia': 'Liquidação CBR724 tipo 37',
                'juros_multa': 0.0,
                'desconto': 0.0,
                'tarifa': 0.0
            }
            
            self.logger.debug(f"Título tipo 37 processado: NN={nosso_numero}, Cliente={nome_cliente[:20]}, Valor={valor_pago:.2f}")
            
            return registro
            
        except Exception as e:
            self.logger.error(f"Erro ao processar título tipo 37: {e}")
            raise
    
    def _processar_titulo_tipo7(self, linha: str, data_arquivo: datetime) -> Dict[str, Any]:
        """Processa registro tipo 7 (título)
        
        Layout CBR724 (160 caracteres) - CONFORME VBA ORIGINAL:
        Posição  Tamanho  Campo
        -------  -------  -----
        0-2      3        Tipo registro (' 7')
        3-20     17       NossoNumero completo (VBA: Mid(MyString, 4, 17))
        21-30    10       Nosso número repetido
        31-64    34       Sacado/Nome do cliente
        65-72    8        Data vencimento (DDMMAAAA)
        73-82    10       ?
        83-86    4        Operação (RG, LQ, BX, etc)
        87-160   73       Valores
        
        IMPORTANTE VBA: 
        - Extrai posição [4:21] (17 chars): NossoNumero = Mid(MyString, 4, 17)
        - Pega últimos 10: NossoNumero = Right(NossoNumero, 10)
        """
        try:
            # Extrair campos EXATAMENTE como VBA
            tipo = linha[0:3].strip()
            
            # VBA: NossoNumero = Mid(MyString, 4, 17)
            # Mid() no VBA é 1-indexed, então posição 4 = índice 3 em Python
            nosso_numero_completo = linha[3:20].strip()  # 17 caracteres
            
            # VBA: NossoNumero = Right(NossoNumero, 10)
            # Pegar os últimos 10 dígitos
            if len(nosso_numero_completo) >= 10:
                nosso_numero_raw = nosso_numero_completo[-10:]  # Últimos 10
            else:
                nosso_numero_raw = nosso_numero_completo
            
            nosso_numero = nosso_numero_raw.lstrip('0') if nosso_numero_raw else nosso_numero_raw
            
            # PULAR registros sem Nosso Número
            if not nosso_numero or not nosso_numero.isdigit():
                self.logger.debug(f"Registro tipo 7 sem Nosso Número válido - ignorado: '{nosso_numero_raw}'")
                return None
            
            # VBA: Sacado = Trim(Mid(MyString, 35, 27))
            # Mid() posição 35 = índice 34 em Python
            nome_cliente = linha[34:61].strip()  # 27 chars
            
            # VBA: Vencimento = Mid(MyString, 64, 2) & "/" & Mid(MyString, 66, 2) & "/" & Mid(MyString, 70, 2)
            data_venc_str = linha[63:73].strip()  # Posições 64-73 (ajustado)
            
            # VBA: Operacao = Mid(MyString, 84, 2)
            # Mid() posição 84 = índice 83 em Python
            operacao = linha[83:85].strip()  # 2 chars
            
            # VBA: ValorTitulo = CCur(LTrim(Mid(MyString, 88, 19)))
            # Mid() posição 88 = índice 87 em Python
            valor_titulo_str = linha[87:106].strip()  # 19 chars
            valor_titulo = 0.0
            try:
                # Remover pontos e converter vírgula em ponto
                valor_titulo = float(valor_titulo_str.replace('.', '').replace(',', '.')) if valor_titulo_str else 0.0
            except ValueError:
                valor_titulo = 0.0
            
            # VBA: ValorPago = CCur(LTrim(Mid(MyString, 137, 15)))
            # Mid() posição 137 = índice 136 em Python
            valor_pago_str = linha[136:151].strip()  # 15 chars
            valor_pago = 0.0
            try:
                valor_pago = float(valor_pago_str.replace('.', '').replace(',', '.')) if valor_pago_str else 0.0
            except ValueError:
                valor_pago = 0.0
            
            # VBA: Juros = ValorPago - ValorTitulo
            juros = valor_pago - valor_titulo if valor_pago > valor_titulo else 0.0
            
            # Converter data vencimento (DDMMAAAA)
            data_vencimento = None
            if data_venc_str and len(data_venc_str) == 8:
                try:
                    dia = int(data_venc_str[0:2])
                    mes = int(data_venc_str[2:4])
                    ano = int(data_venc_str[4:8])
                    data_vencimento = datetime(ano, mes, dia)
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"Erro ao converter data '{data_venc_str}': {e}")
            
            # Data de ocorrência = data do arquivo (conforme VBA)
            data_ocorrencia = data_arquivo
            
            # Criar registro
            registro = {
                'tipo_registro': tipo,
                'codigo_banco': nosso_numero_completo,
                'nosso_numero': nosso_numero,
                'nome_cliente': nome_cliente,
                'data_vencimento': data_vencimento,
                'operacao': operacao,  # RG, LQ, LC, BX, MT
                'valor_titulo': valor_titulo,  # Valor original do título
                'valor_pago': valor_pago,
                'data_ocorrencia': data_ocorrencia,
                'data_credito': data_ocorrencia,
                'codigo_ocorrencia': '06',  # Liquidação
                'descricao_ocorrencia': f'Operação {operacao} CBR724',
                'juros_multa': juros,  # Calculado: ValorPago - ValorTitulo
                'desconto': 0.0,
                'tarifa': 0.0
            }
            
            self.logger.debug(f"Título processado: NN={nosso_numero}, Valor={valor_pago:.2f}")
            
            return registro
            
        except Exception as e:
            self.logger.error(f"Erro ao processar título: {e}")
            raise
    
    def validar_arquivo(self, caminho_arquivo: str) -> bool:
        """Valida se o arquivo é um CBR724 válido"""
        try:
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                primeira_linha = f.readline().rstrip('\n\r')
            
            # Verificar se começa com código esperado e tem 160 chars
            if len(primeira_linha) == 160 and 'CBR724' in primeira_linha:
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erro ao validar arquivo: {e}")
            return False
