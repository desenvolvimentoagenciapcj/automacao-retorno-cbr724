#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Arquivos CNAB
Classe responsável por interpretar arquivos de retorno bancário
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Any

class ProcessadorCNAB:
    """Processador de arquivos CNAB240 e CNAB400"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Códigos de ocorrência mais comuns
        self.ocorrencias = {
            '02': 'Entrada Confirmada',
            '03': 'Entrada Rejeitada',
            '06': 'Liquidação',
            '09': 'Baixa',
            '10': 'Baixa Solicitada via Arquivo',
            '11': 'Em Ser - Arquivo de Títulos Pendentes',
            '12': 'Abatimento Concedido',
            '13': 'Abatimento Cancelado',
            '14': 'Vencimento Alterado',
            '15': 'Baixas rejeitadas',
            '16': 'Instruções rejeitadas',
            '17': 'Alteração de dados rejeitada',
            '18': 'Cobrança contratual',
            '19': 'Recebimento de instrução de protesto',
            '20': 'Recebimento de instrução de sustação de protesto',
            '21': 'Recebimento de instrução de não protestar',
            '23': 'Título enviado a cartório',
            '24': 'Instrução de protesto rejeitada/sustada/pendente',
            '25': 'Alegações do pagador',
            '26': 'Tarifa de aviso de cobrança',
            '27': 'Tarifa de extrato posição',
            '28': 'Tarifa de relação das liquidações',
            '29': 'Tarifa de manutenção de títulos vencidos',
            '30': 'Débito mensal de tarifas'
        }
    
    def processar_arquivo(self, caminho_arquivo: str) -> List[Dict[str, Any]]:
        """Processa um arquivo CNAB e retorna lista de registros"""
        self.logger.info(f"Processando arquivo: {caminho_arquivo}")
        
        try:
            with open(caminho_arquivo, 'r', encoding='latin1') as arquivo:
                linhas = arquivo.readlines()
            
            # Detectar tipo de CNAB
            primeira_linha = linhas[0].rstrip('\r\n')
            tamanho_linha = len(primeira_linha)
            
            # Aceitar variações de tamanho (linhas podem ter espaços cortados)
            if tamanho_linha >= 390 and tamanho_linha <= 400:
                return self._processar_cnab400(linhas)
            elif tamanho_linha >= 230 and tamanho_linha <= 240:
                return self._processar_cnab240(linhas)
            else:
                raise ValueError(f"Formato de arquivo não reconhecido. Tamanho da linha: {tamanho_linha}")
                
        except Exception as e:
            self.logger.error(f"Erro ao processar arquivo {caminho_arquivo}: {e}")
            raise
    
    def _processar_cnab400(self, linhas: List[str]) -> List[Dict[str, Any]]:
        """Processa arquivo CNAB400"""
        registros = []
        
        for i, linha in enumerate(linhas):
            linha = linha.rstrip('\r\n')
            
            # Aceitar linhas com pequenas variações
            if len(linha) < 390:
                self.logger.warning(f"Linha {i+1} muito curta: {len(linha)}")
                continue
            
            # Tipo de registro (posição 1)
            tipo_registro = linha[0:1]
            
            if tipo_registro == '0':  # Header
                self.logger.debug("Processando header CNAB400")
                continue
            elif tipo_registro == '1':  # Detalhe
                registro = self._processar_detalhe_cnab400(linha, i+1)
                if registro:
                    registros.append(registro)
            elif tipo_registro == '9':  # Trailer
                self.logger.debug("Processando trailer CNAB400")
                continue
        
        self.logger.info(f"Processados {len(registros)} registros CNAB400")
        return registros
    
    def _processar_cnab240(self, linhas: List[str]) -> List[Dict[str, Any]]:
        """Processa arquivo CNAB240"""
        registros = []
        
        for i, linha in enumerate(linhas):
            linha = linha.rstrip('\r\n')
            
            # Aceitar linhas com pequenas variações
            if len(linha) < 230:
                self.logger.warning(f"Linha {i+1} muito curta: {len(linha)}")
                continue
            
            # Código do banco (posições 1-3)
            # Tipo de registro (posições 8-8)
            tipo_registro = linha[7:8]
            
            if tipo_registro == '0':  # Header do arquivo
                continue
            elif tipo_registro == '1':  # Header do lote
                continue
            elif tipo_registro == '3':  # Detalhe
                # Tipo de segmento (posição 14)
                segmento = linha[13:14]
                if segmento in ['T', 'U']:  # Segmentos de retorno de cobrança
                    registro = self._processar_detalhe_cnab240(linha, i+1, segmento)
                    if registro:
                        registros.append(registro)
            elif tipo_registro == '5':  # Trailer do lote
                continue
            elif tipo_registro == '9':  # Trailer do arquivo
                continue
        
        self.logger.info(f"Processados {len(registros)} registros CNAB240")
        return registros
    
    def _processar_detalhe_cnab400(self, linha: str, numero_linha: int) -> Dict[str, Any]:
        """Processa linha de detalhe CNAB400"""
        try:
            registro = {
                'tipo': 'CNAB400',
                'linha': numero_linha,
                'nosso_numero': linha[62:70].strip(),
                'seu_numero': linha[116:126].strip(),
                'data_ocorrencia': self._converter_data(linha[110:116]),
                'codigo_ocorrencia': linha[108:110],
                'descricao_ocorrencia': self.ocorrencias.get(linha[108:110], 'Ocorrência não catalogada'),
                'valor_titulo': float(linha[152:165]) / 100,  # Valor em centavos
                'valor_pago': float(linha[253:266]) / 100 if linha[253:266].strip() else 0,
                'data_credito': self._converter_data(linha[175:181]) if linha[175:181].strip() != '000000' else None,
                'tarifa': float(linha[181:194]) / 100 if linha[181:194].strip() else 0,
                'juros_multa': float(linha[266:279]) / 100 if linha[266:279].strip() else 0,
                'desconto': float(linha[240:253]) / 100 if linha[240:253].strip() else 0,
                'numero_documento': linha[116:126].strip(),
                'data_vencimento': self._converter_data(linha[146:152]),
                'banco': linha[1:4],
                'agencia': linha[17:21],
                'conta': linha[21:29]
            }
            
            return registro
            
        except Exception as e:
            self.logger.error(f"Erro ao processar linha {numero_linha} CNAB400: {e}")
            return None
    
    def _processar_detalhe_cnab240(self, linha: str, numero_linha: int, segmento: str) -> Dict[str, Any]:
        """Processa linha de detalhe CNAB240"""
        try:
            if segmento == 'T':  # Segmento T - Dados do título
                registro = {
                    'tipo': 'CNAB240',
                    'segmento': segmento,
                    'linha': numero_linha,
                    'nosso_numero': linha[40:60].strip(),
                    'seu_numero': linha[105:130].strip(),
                    'codigo_ocorrencia': linha[15:17],
                    'descricao_ocorrencia': self.ocorrencias.get(linha[15:17], 'Ocorrência não catalogada'),
                    'data_ocorrencia': self._converter_data(linha[143:151]),
                    'valor_titulo': float(linha[81:96]) / 100,
                    'valor_pago': float(linha[77:92]) / 100 if linha[77:92].strip() else 0,
                    'data_credito': self._converter_data(linha[175:183]) if linha[175:183].strip() != '00000000' else None,
                    'numero_documento': linha[105:130].strip(),
                    'data_vencimento': self._converter_data(linha[73:81]),
                    'banco': linha[0:3],
                    'agencia': linha[17:22],
                    'conta': linha[23:35]
                }
                
            elif segmento == 'U':  # Segmento U - Dados do pagamento
                registro = {
                    'tipo': 'CNAB240',
                    'segmento': segmento,
                    'linha': numero_linha,
                    'juros_multa': float(linha[17:32]) / 100 if linha[17:32].strip() else 0,
                    'desconto': float(linha[32:47]) / 100 if linha[32:47].strip() else 0,
                    'abatimento': float(linha[47:62]) / 100 if linha[47:62].strip() else 0,
                    'iof': float(linha[62:77]) / 100 if linha[62:77].strip() else 0,
                    'valor_pago': float(linha[77:92]) / 100,
                    'valor_liquido': float(linha[92:107]) / 100,
                    'tarifa': float(linha[198:213]) / 100 if linha[198:213].strip() else 0
                }
            
            return registro
            
        except Exception as e:
            self.logger.error(f"Erro ao processar linha {numero_linha} CNAB240 segmento {segmento}: {e}")
            return None
    
    def _converter_data(self, data_str: str) -> datetime:
        """Converte string de data DDMMAA ou DDMMAAAA para datetime"""
        if not data_str or data_str.strip() == '000000' or data_str.strip() == '00000000':
            return None
        
        try:
            data_str = data_str.strip()
            
            if len(data_str) == 6:  # DDMMAA
                dia = int(data_str[0:2])
                mes = int(data_str[2:4])
                ano = int(data_str[4:6])
                # Assumir que anos 00-30 são 2000-2030, 31-99 são 1931-1999
                if ano <= 30:
                    ano += 2000
                else:
                    ano += 1900
                    
            elif len(data_str) == 8:  # DDMMAAAA ou AAAAMMDD
                if data_str[2:3] in ['/', '-'] or int(data_str[0:2]) <= 31:  # DDMMAAAA
                    dia = int(data_str[0:2])
                    mes = int(data_str[2:4])
                    ano = int(data_str[4:8])
                else:  # AAAAMMDD
                    ano = int(data_str[0:4])
                    mes = int(data_str[4:6])
                    dia = int(data_str[6:8])
            else:
                raise ValueError(f"Formato de data inválido: {data_str}")
            
            return datetime(ano, mes, dia)
            
        except (ValueError, IndexError) as e:
            self.logger.warning(f"Erro ao converter data '{data_str}': {e}")
            return None
    
    def validar_arquivo(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Valida um arquivo CNAB e retorna informações básicas"""
        try:
            with open(caminho_arquivo, 'r', encoding='latin1') as arquivo:
                linhas = arquivo.readlines()
            
            if not linhas:
                return {'valido': False, 'erro': 'Arquivo vazio'}
            
            primeira_linha = linhas[0].strip()
            
            # Detectar tipo
            if len(primeira_linha) == 400:
                tipo = 'CNAB400'
                banco = primeira_linha[1:4]
            elif len(primeira_linha) == 240:
                tipo = 'CNAB240'
                banco = primeira_linha[0:3]
            else:
                return {'valido': False, 'erro': f'Formato não reconhecido (tamanho: {len(primeira_linha)})'}
            
            return {
                'valido': True,
                'tipo': tipo,
                'banco': banco,
                'total_linhas': len(linhas),
                'tamanho_arquivo': sum(len(linha) for linha in linhas)
            }
            
        except Exception as e:
            return {'valido': False, 'erro': str(e)}