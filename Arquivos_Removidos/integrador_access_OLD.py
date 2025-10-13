#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrador com Microsoft Access
Classe responsável por integrar os dados processados com o banco Access
"""

import os
import shutil
import pyodbc
import logging
from datetime import datetime
from typing import List, Dict, Any

class IntegradorAccess:
    """Integrador com banco de dados Microsoft Access"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.conexao = None
        
        # String de conexão para Access
        self.driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        self.caminho_banco = config['banco']['caminho']
    
    def conectar(self):
        """Estabelece conexão com o banco Access"""
        try:
            if self.conexao and not self.conexao.closed:
                return True
            
            # Verificar se o arquivo existe
            if not os.path.exists(self.caminho_banco):
                raise FileNotFoundError(f"Banco de dados não encontrado: {self.caminho_banco}")
            
            # String de conexão
            conn_str = f'DRIVER={self.driver};DBQ={self.caminho_banco};'
            
            self.conexao = pyodbc.connect(conn_str)
            self.conexao.autocommit = False  # Controle manual de transações
            
            self.logger.info("Conexão com Access estabelecida")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao conectar com Access: {e}")
            return False
    
    def desconectar(self):
        """Fecha conexão com o banco"""
        try:
            if self.conexao and not self.conexao.closed:
                self.conexao.close()
                self.logger.debug("Conexão com Access fechada")
        except Exception as e:
            self.logger.error(f"Erro ao fechar conexão: {e}")
    
    def processar_registros(self, registros: List[Dict[str, Any]]) -> Dict[str, int]:
        """Processa lista de registros do arquivo de retorno"""
        if not self.conectar():
            raise Exception("Não foi possível conectar ao banco de dados")
        
        resultado = {
            'total_processados': 0,
            'baixas': 0,
            'atualizacoes': 0,
            'erros': 0,
            'duplicatas': 0
        }
        
        try:
            cursor = self.conexao.cursor()
            
            for registro in registros:
                try:
                    resultado_registro = self._processar_registro(cursor, registro)
                    
                    if resultado_registro == 'baixa':
                        resultado['baixas'] += 1
                    elif resultado_registro == 'atualizacao':
                        resultado['atualizacoes'] += 1
                    elif resultado_registro == 'duplicata':
                        resultado['duplicatas'] += 1
                    
                    resultado['total_processados'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Erro ao processar registro {registro.get('nosso_numero', 'N/A')}: {e}")
                    resultado['erros'] += 1
            
            # Commit das alterações
            self.conexao.commit()
            self.logger.info(f"Transação commitada. Total processados: {resultado['total_processados']}")
            
        except Exception as e:
            # Rollback em caso de erro
            self.conexao.rollback()
            self.logger.error(f"Erro no processamento. Rollback executado: {e}")
            raise
        
        finally:
            self.desconectar()
        
        return resultado
    
    def _processar_registro(self, cursor, registro: Dict[str, Any]) -> str:
        """Processa um registro individual"""
        nosso_numero = registro.get('nosso_numero', '').strip()
        codigo_ocorrencia = registro.get('codigo_ocorrencia', '')
        
        if not nosso_numero:
            raise ValueError("Nosso número não encontrado no registro")
        
        # Verificar se o título existe
        titulo = self._buscar_titulo(cursor, nosso_numero)
        
        if not titulo:
            self.logger.warning(f"Título não encontrado: {nosso_numero}")
            return 'erro'
        
        # Verificar duplicata
        if self._verificar_duplicata(cursor, nosso_numero, registro['data_ocorrencia']):
            self.logger.warning(f"Registro duplicado ignorado: {nosso_numero}")
            return 'duplicata'
        
        # Registrar ocorrência
        self._registrar_ocorrencia(cursor, titulo['id'], registro)
        
        # Processar baseado no código de ocorrência
        if codigo_ocorrencia in ['06', '17']:  # Liquidação
            return self._processar_baixa(cursor, titulo, registro)
        elif codigo_ocorrencia in ['09', '10']:  # Baixa manual
            return self._processar_baixa_manual(cursor, titulo, registro)
        elif codigo_ocorrencia in ['02']:  # Confirmação de entrada
            return self._atualizar_status(cursor, titulo['id'], 'Confirmado')
        elif codigo_ocorrencia in ['03']:  # Entrada rejeitada
            return self._atualizar_status(cursor, titulo['id'], 'Rejeitado')
        else:
            # Apenas registrar a ocorrência
            return 'atualizacao'
    
    def _buscar_titulo(self, cursor, nosso_numero: str) -> Dict[str, Any]:
        """Busca título pelo nosso número"""
        try:
            sql = f"""
                SELECT Id, NossoNumero, ValorTitulo, DataVencimento, Status, SeuNumero
                FROM {self.config['banco']['tabela_titulos']}
                WHERE NossoNumero = ?
            """
            
            cursor.execute(sql, (nosso_numero,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'nosso_numero': row[1],
                    'valor_titulo': row[2],
                    'data_vencimento': row[3],
                    'status': row[4],
                    'seu_numero': row[5]
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar título {nosso_numero}: {e}")
            return None
    
    def _verificar_duplicata(self, cursor, nosso_numero: str, data_ocorrencia: datetime) -> bool:
        """Verifica se a ocorrência já foi processada"""
        try:
            sql = f"""
                SELECT COUNT(*) 
                FROM {self.config['banco']['tabela_ocorrencias']}
                WHERE NossoNumero = ? AND DataOcorrencia = ?
            """
            
            cursor.execute(sql, (nosso_numero, data_ocorrencia))
            count = cursor.fetchone()[0]
            
            return count > 0
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar duplicata: {e}")
            return False
    
    def _registrar_ocorrencia(self, cursor, titulo_id: int, registro: Dict[str, Any]):
        """Registra a ocorrência na tabela de ocorrências"""
        try:
            sql = f"""
                INSERT INTO {self.config['banco']['tabela_ocorrencias']}
                (TituloId, NossoNumero, CodigoOcorrencia, DescricaoOcorrencia, 
                 DataOcorrencia, ValorPago, DataProcessamento)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql, (
                titulo_id,
                registro.get('nosso_numero', ''),
                registro.get('codigo_ocorrencia', ''),
                registro.get('descricao_ocorrencia', ''),
                registro.get('data_ocorrencia'),
                registro.get('valor_pago', 0),
                datetime.now()
            ))
            
        except Exception as e:
            self.logger.error(f"Erro ao registrar ocorrência: {e}")
            raise
    
    def _processar_baixa(self, cursor, titulo: Dict[str, Any], registro: Dict[str, Any]) -> str:
        """Processa baixa por pagamento"""
        try:
            # Atualizar status do título
            sql_titulo = f"""
                UPDATE {self.config['banco']['tabela_titulos']}
                SET Status = 'Pago', 
                    DataPagamento = ?, 
                    ValorPago = ?,
                    DataCredito = ?
                WHERE Id = ?
            """
            
            cursor.execute(sql_titulo, (
                registro.get('data_ocorrencia'),
                registro.get('valor_pago', 0),
                registro.get('data_credito'),
                titulo['id']
            ))
            
            # Registrar na tabela de baixas
            sql_baixa = f"""
                INSERT INTO {self.config['banco']['tabela_baixas']}
                (TituloId, NossoNumero, DataBaixa, ValorPago, TipoBaixa, 
                 Juros, Desconto, Tarifa, DataCredito)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql_baixa, (
                titulo['id'],
                registro.get('nosso_numero', ''),
                registro.get('data_ocorrencia'),
                registro.get('valor_pago', 0),
                'Pagamento',
                registro.get('juros_multa', 0),
                registro.get('desconto', 0),
                registro.get('tarifa', 0),
                registro.get('data_credito')
            ))
            
            self.logger.info(f"Baixa processada: {registro.get('nosso_numero')} - Valor: {registro.get('valor_pago', 0)}")
            return 'baixa'
            
        except Exception as e:
            self.logger.error(f"Erro ao processar baixa: {e}")
            raise
    
    def _processar_baixa_manual(self, cursor, titulo: Dict[str, Any], registro: Dict[str, Any]) -> str:
        """Processa baixa manual (sem pagamento)"""
        try:
            # Atualizar status do título
            sql_titulo = f"""
                UPDATE {self.config['banco']['tabela_titulos']}
                SET Status = 'Baixado', 
                    DataBaixa = ?
                WHERE Id = ?
            """
            
            cursor.execute(sql_titulo, (registro.get('data_ocorrencia'), titulo['id']))
            
            # Registrar na tabela de baixas
            sql_baixa = f"""
                INSERT INTO {self.config['banco']['tabela_baixas']}
                (TituloId, NossoNumero, DataBaixa, ValorPago, TipoBaixa)
                VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql_baixa, (
                titulo['id'],
                registro.get('nosso_numero', ''),
                registro.get('data_ocorrencia'),
                0,
                'Baixa Manual'
            ))
            
            self.logger.info(f"Baixa manual processada: {registro.get('nosso_numero')}")
            return 'baixa'
            
        except Exception as e:
            self.logger.error(f"Erro ao processar baixa manual: {e}")
            raise
    
    def _atualizar_status(self, cursor, titulo_id: int, novo_status: str) -> str:
        """Atualiza status do título"""
        try:
            sql = f"""
                UPDATE {self.config['banco']['tabela_titulos']}
                SET Status = ?, DataUltimaAtualizacao = ?
                WHERE Id = ?
            """
            
            cursor.execute(sql, (novo_status, datetime.now(), titulo_id))
            self.logger.info(f"Status atualizado para: {novo_status}")
            return 'atualizacao'
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar status: {e}")
            raise
    
    def fazer_backup(self) -> str:
        """Cria backup do banco de dados"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_original = os.path.basename(self.caminho_banco)
            nome_backup = f"backup_{timestamp}_{nome_original}"
            
            pasta_backup = self.config['diretorios']['backup']
            caminho_backup = os.path.join(pasta_backup, nome_backup)
            
            shutil.copy2(self.caminho_banco, caminho_backup)
            
            self.logger.info(f"Backup criado: {caminho_backup}")
            return caminho_backup
            
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {e}")
            raise
    
    def testar_conexao(self) -> bool:
        """Testa a conexão com o banco"""
        try:
            if self.conectar():
                cursor = self.conexao.cursor()
                cursor.execute("SELECT COUNT(*) FROM MSysObjects")
                self.desconectar()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erro no teste de conexão: {e}")
            return False