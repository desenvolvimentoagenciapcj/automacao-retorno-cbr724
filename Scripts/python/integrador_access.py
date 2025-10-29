#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrador com Microsoft Access - dbBaixa2025 e Cobranca2019
Versão atualizada para trabalhar com os bancos corretos
"""

import os
import shutil
import pyodbc
import logging
from datetime import datetime
from typing import List, Dict, Any

class IntegradorAccess:
    """Integrador com bancos de dados Access (dbBaixa2025 e Cobranca2019)"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.conn_baixa = None
        self.conn_cobranca = None
        
        # String de conexão para Access
        self.driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        self.caminho_baixa = config['bancos']['baixa']['caminho']
        
        # Banco Cobranca2019 é opcional (pode ter dependências de rede)
        self.usar_cobranca = config['bancos']['cobranca'].get('ativo', True)
        self.caminho_cobranca = config['bancos']['cobranca']['caminho'] if self.usar_cobranca else None
    
    def conectar(self):
        """Estabelece conexão com os bancos Access"""
        try:
            # Conecta no banco de baixas (onde importa os retornos)
            if not self.conn_baixa or self.conn_baixa.closed:
                if not os.path.exists(self.caminho_baixa):
                    raise FileNotFoundError(f"Banco dbBaixa2025 não encontrado: {self.caminho_baixa}")
                
                conn_str = f'DRIVER={self.driver};DBQ={self.caminho_baixa};'
                self.conn_baixa = pyodbc.connect(conn_str)
                self.conn_baixa.autocommit = False
                self.logger.info("✓ Conectado ao dbBaixa2025.accdb")
            
            # Conecta no banco de cobrança APENAS se estiver ativo
            if self.usar_cobranca:
                if not self.conn_cobranca or self.conn_cobranca.closed:
                    if not os.path.exists(self.caminho_cobranca):
                        self.logger.warning(f"Banco Cobranca2019 não encontrado: {self.caminho_cobranca}")
                        self.logger.warning("Continuando apenas com dbBaixa2025...")
                        self.usar_cobranca = False
                    else:
                        try:
                            conn_str = f'DRIVER={self.driver};DBQ={self.caminho_cobranca};'
                            self.conn_cobranca = pyodbc.connect(conn_str)
                            self.conn_cobranca.autocommit = False
                            self.logger.info("✓ Conectado ao Cobranca2019.accdb")
                        except Exception as e:
                            self.logger.warning(f"Erro ao conectar Cobranca2019: {e}")
                            self.logger.warning("Continuando apenas com dbBaixa2025...")
                            self.usar_cobranca = False
            else:
                self.logger.info("ℹ️  Cobranca2019.accdb desabilitado (usando apenas dbBaixa2025)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao conectar com Access: {e}")
            return False
    
    def desconectar(self):
        """Fecha conexões com os bancos"""
        try:
            if self.conn_baixa and not self.conn_baixa.closed:
                self.conn_baixa.close()
                self.logger.debug("Conexão dbBaixa2025 fechada")
            
            if self.conn_cobranca and not self.conn_cobranca.closed:
                self.conn_cobranca.close()
                self.logger.debug("Conexão Cobranca2019 fechada")
        except Exception as e:
            self.logger.error(f"Erro ao fechar conexões: {e}")
    
    def processar_registros(self, registros: List[Dict[str, Any]]) -> Dict[str, int]:
        """Processa lista de registros do arquivo de retorno"""
        # FAZER BACKUP ANTES DE PROCESSAR
        self.logger.info("💾 Criando backup dos bancos...")
        backups = self.fazer_backup()
        for backup in backups:
            self.logger.info(f"   ✓ {backup}")
        
        if not self.conectar():
            raise Exception("Não foi possível conectar aos bancos de dados")
        
        resultado = {
            'total_processados': 0,
            'baixas': 0,
            'criados': 0,
            'cancelados': 0,
            'atualizacoes': 0,
            'erros': 0,
            'nao_encontrados': 0
        }
        
        try:
            cursor_baixa = self.conn_baixa.cursor()
            
            for registro in registros:
                try:
                    resultado_registro = self._processar_registro(cursor_baixa, registro)
                    
                    if resultado_registro == 'baixa':
                        resultado['baixas'] += 1
                    elif resultado_registro == 'criado':
                        resultado['criados'] += 1
                    elif resultado_registro == 'cancelado':
                        resultado['cancelados'] += 1
                    elif resultado_registro == 'atualizacao':
                        resultado['atualizacoes'] += 1
                    elif resultado_registro == 'nao_encontrado':
                        resultado['nao_encontrados'] += 1
                    
                    resultado['total_processados'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Erro ao processar registro {registro.get('nosso_numero', 'N/A')}: {e}")
                    resultado['erros'] += 1
            
            # Commit das alterações
            self.conn_baixa.commit()
            self.logger.info(f"✓ Transação commitada. Processados: {resultado['total_processados']}, "
                           f"Criados: {resultado['criados']}, Baixas: {resultado['baixas']}, "
                           f"Cancelados: {resultado['cancelados']}, Não encontrados: {resultado['nao_encontrados']}")
            
            # Executar as 3 consultas do Alexandre (passos 1, 2 e 3)
            self.logger.info("🔄 Executando consultas de atualização (Alexandre Passos 1, 2 e 3)...")
            self._executar_consultas_alexandre(cursor_baixa)
            
        except Exception as e:
            # Rollback em caso de erro
            self.conn_baixa.rollback()
            self.logger.error(f"✗ Erro no processamento. Rollback executado: {e}")
            raise
        
        finally:
            self.desconectar()
        
        return resultado
    
    def _extrair_id_pcj_do_nome(self, nome_cliente: str) -> int:
        """
        Extrai o ID_PCJ (CD_SAC) do nome do cliente.
        VBA: Verifica se começa com dígito e extrai até encontrar não-dígito.
        
        Exemplo: "880 JOSE DA SILVA" -> 880
        """
        if not nome_cliente:
            return None
        
        # VBA: If InStr(1, "0123456789", Left(Sacado, 1)) = 0 Then
        # Se não começa com dígito, retorna None
        if not nome_cliente[0].isdigit():
            return None
        
        # VBA: For i = 2 To 6
        #          If InStr(1, "0123456789", Mid(Sacado, i, 1)) > 0 Then
        #              IdLength = i
        #          End If
        #      Next
        id_pcj_str = ''
        for i, char in enumerate(nome_cliente[:6]):  # Máximo 6 dígitos
            if char.isdigit():
                id_pcj_str += char
            else:
                break
        
        if id_pcj_str:
            return int(id_pcj_str)
        
        return None
    
    def _criar_titulo_novo(self, cursor, registro: Dict[str, Any]) -> str:
        """
        Cria um título novo no banco (VBA: RsTitulo.AddNew).
        Usado quando o título não existe e operação é RG, LQ, LC ou BX.
        """
        try:
            nosso_numero = str(registro.get('nosso_numero', '')).strip()
            operacao = registro.get('operacao', '').strip()
            nome_cliente = registro.get('nome_cliente', '').strip()
            
            # Extrair ID_PCJ do nome do cliente
            id_pcj = self._extrair_id_pcj_do_nome(nome_cliente)
            if not id_pcj:
                self.logger.warning(f"Título {nosso_numero} sem ID_PCJ no nome '{nome_cliente}' - IGNORADO")
                return 'erro'
            
            # Data do arquivo (data de ocorrência)
            data_arquivo = registro.get('data_ocorrencia')
            if data_arquivo and hasattr(data_arquivo, 'date'):
                data_arquivo = data_arquivo.date()
            
            # Vencimento
            data_vencimento = registro.get('data_vencimento')
            if data_vencimento and hasattr(data_vencimento, 'date'):
                data_vencimento = data_vencimento.date()
            
            # Valores
            valor_titulo = registro.get('valor_titulo', 0)
            valor_pago = registro.get('valor_pago', 0)
            juros = registro.get('juros_multa', 0)
            
            # VBA: AnoReferencia = 21
            # Extrair ano de referência do vencimento
            ano_ref = data_vencimento.year % 100 if data_vencimento else 25  # Default: 25
            
            # Determinar ID_CONTROLE baseado na operação
            # VBA: RG=1 (novo), LQ/LC=2 (pago), BX=3 (cancelado)
            id_controle = 1
            if operacao in ['LQ', 'LC']:
                id_controle = 2
            elif operacao == 'BX':
                id_controle = 3
            elif operacao == 'RG':
                id_controle = 1
            
            # INSERT do título novo
            sql = """
                INSERT INTO pcjTITULOS 
                (NR_NNR_TIT, CD_SAC, DT_VCM_TIT, VL_NOM_TIT, AnoRef, Situacao, 
                 Data_Transf_baixa, ID_TIPO_CONTROLE, ID_CONTROLE
            """
            
            # Adicionar campos opcionais para títulos pagos (LQ/LC)
            if operacao in ['LQ', 'LC']:
                sql += ", DT_PGTO_TIT, VL_PGTO_TIT"
                if juros > 0:
                    sql += ", VL_JUROS_TIT"
            
            sql += ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?"
            
            params = [
                nosso_numero,
                id_pcj,
                data_vencimento,
                valor_titulo,
                ano_ref,
                'A',  # Situacao = 'A' (ativo)
                datetime.now(),  # Data_Transf_baixa
                1,  # ID_TIPO_CONTROLE sempre 1
                id_controle
            ]
            
            # Adicionar valores opcionais
            if operacao in ['LQ', 'LC']:
                sql += ", ?, ?"
                params.extend([data_arquivo, valor_pago])
                if juros > 0:
                    sql += ", ?"
                    params.append(juros)
            
            sql += ")"
            
            cursor.execute(sql, params)
            
            self.logger.info(f"✓ Título CRIADO: {nosso_numero} (Operação {operacao}) - "
                           f"ID_PCJ={id_pcj}, Valor={valor_titulo:.2f}")
            return 'criado'
            
        except Exception as e:
            self.logger.error(f"Erro ao criar título {nosso_numero}: {e}")
            raise
    
    def _processar_registro(self, cursor, registro: Dict[str, Any]) -> str:
        """Processa um registro individual no banco dbBaixa2025
        
        LÓGICA VBA:
        1. Busca título com RsTitulo.Seek
        2. Se NoMatch (não achou):
           - RG/LQ/LC/BX: Cria novo (AddNew)
        3. Se achou:
           - RG: IGNORA
           - LQ/LC: Atualiza para pago (Edit)
           - BX: Atualiza para cancelado, exceto BXS (Edit)
           - MT: IGNORA
        """
        nosso_numero = str(registro.get('nosso_numero', '')).strip()
        operacao = registro.get('operacao', '').strip()
        
        if not nosso_numero:
            self.logger.debug("Registro sem Nosso Número - ignorado (pode ser totalizador)")
            return 'ignorado'
        
        self.logger.debug(f"Processando: Nosso Número {nosso_numero}, Operação {operacao}")
        
        # VBA: RsTitulo.Seek "=", NossoNumero
        # Buscar o título na tabela pcjTITULOS
        titulo = self._buscar_titulo(cursor, nosso_numero)
        
        # VBA: If RsTitulo.NoMatch Then
        if not titulo:
            # Título NÃO existe - CRIAR novo
            self.logger.info(f"Título {nosso_numero} NÃO encontrado - Operação {operacao}")
            
            # VBA: Cria novo para BX, LQ, LC ou RG
            if operacao in ['BX', 'LQ', 'LC', 'RG']:
                return self._criar_titulo_novo(cursor, registro)
            else:
                self.logger.warning(f"Operação desconhecida: {operacao} (título {nosso_numero})")
                return 'nao_encontrado'
        
        # VBA: Else (título JÁ existe - ATUALIZAR)
        else:
            self.logger.info(f"Título {nosso_numero} encontrado - Operação {operacao}")
            
            # VBA: If Operacao = "BX" Then
            if operacao == 'BX':
                # VBA: Verifica se é BXS (cancelamento automático do BB)
                # BXS = Mid(MyString, 84, 3)
                # Se for BXS, ignora. Senão, cancela.
                # Por enquanto, vamos cancelar todos BX
                return self._processar_cancelamento(cursor, titulo, registro)
            
            # VBA: If Operacao = "MT" Then (ignora movimentação)
            elif operacao == 'MT':
                self.logger.info(f"Movimentação ignorada: {nosso_numero}")
                return 'ignorado'
            
            # VBA: If (Operacao = "LQ") Or (Operacao = "LC") Then
            elif operacao in ['LQ', 'LC']:
                return self._processar_baixa(cursor, titulo, registro)
            
            # VBA: RG em título existente = IGNORA
            elif operacao == 'RG':
                self.logger.info(f"Operação RG ignorada (título já existe): {nosso_numero}")
                return 'ignorado'
            
            # Operação desconhecida
            else:
                self.logger.warning(f"Operação desconhecida: {operacao} (título {nosso_numero})")
                return 'atualizacao'
    
    def _buscar_titulo(self, cursor, nosso_numero: str) -> Dict[str, Any]:
        """Busca título pelo nosso número na pcjTITULOS"""
        try:
            sql = """
                SELECT CD_SAC, NR_NNR_TIT, VL_NOM_TIT, DT_VCM_TIT, DT_PGTO_TIT, 
                       VL_PGTO_TIT, CodMovimento, NR_SNR_TIT
                FROM pcjTITULOS
                WHERE NR_NNR_TIT = ?
            """
            
            cursor.execute(sql, (nosso_numero,))
            row = cursor.fetchone()
            
            # Se não encontrou com busca exata, tentar busca parcial (termina com o número)
            if not row and nosso_numero and len(nosso_numero) > 0:
                sql_parcial = f"""
                    SELECT CD_SAC, NR_NNR_TIT, VL_NOM_TIT, DT_VCM_TIT, DT_PGTO_TIT, 
                           VL_PGTO_TIT, CodMovimento, NR_SNR_TIT
                    FROM pcjTITULOS
                    WHERE NR_NNR_TIT LIKE '%{nosso_numero}'
                """
                cursor.execute(sql_parcial)
                row = cursor.fetchone()
                
                if row:
                    self.logger.info(f"✓ Título encontrado com busca parcial: {nosso_numero} → {row[1]}")
            
            if row:
                return {
                    'cd_sac': row[0],
                    'nosso_numero': row[1],
                    'valor_titulo': row[2],
                    'data_vencimento': row[3],
                    'data_pagamento': row[4],
                    'valor_pago': row[5],
                    'cod_movimento': row[6],
                    'seu_numero': row[7]
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar título {nosso_numero}: {e}")
            return None
    
    def _processar_cancelamento(self, cursor, titulo: Dict[str, Any], registro: Dict[str, Any]) -> str:
        """Processa cancelamento de título (operação BX)"""
        try:
            nosso_numero = titulo['nosso_numero']
            
            # VBA: RsTitulo.Edit
            #      RsTitulo("ID_CONTROLE") = 3
            #      RsTitulo("Data_Transf_baixa") = Now()
            #      RsTitulo.Update
            
            sql = """
                UPDATE pcjTITULOS
                SET ID_CONTROLE = 3,
                    Data_Transf_baixa = ?
                WHERE NR_NNR_TIT = ?
            """
            
            cursor.execute(sql, (datetime.now(), nosso_numero))
            
            self.logger.info(f"✓ Título CANCELADO: {nosso_numero}")
            return 'cancelado'
            
        except Exception as e:
            self.logger.error(f"Erro ao cancelar título: {e}")
            raise
    
    def _processar_baixa(self, cursor, titulo: Dict[str, Any], registro: Dict[str, Any]) -> str:
        """Processa baixa por pagamento na pcjTITULOS (operações LQ/LC)
        
        VBA: RsTitulo.Edit
             RsTitulo("ID_CONTROLE") = 2
             RsTitulo("DT_PGTO_TIT") = CDate(DataArquivo)
             RsTitulo("VL_PGTO_TIT") = ValorPago
             RsTitulo("Data_Transf_baixa") = Now()
             If Juros > 0 Then RsTitulo("VL_JUROS_TIT") = Juros
             RsTitulo.Update
        """
        try:
            nosso_numero = titulo['nosso_numero']
            
            # Extrair data SEM hora (apenas DD/MM/AAAA)
            data_ocorrencia = registro.get('data_ocorrencia')
            
            # Converter para apenas data (sem hora)
            if data_ocorrencia and hasattr(data_ocorrencia, 'date'):
                data_ocorrencia = data_ocorrencia.date()
            
            # Valores
            valor_pago = registro.get('valor_pago', 0)
            juros = registro.get('juros_multa', 0)
            
            # VBA: Atualizar o registro na pcjTITULOS
            sql = """
                UPDATE pcjTITULOS
                SET ID_CONTROLE = 2,
                    DT_PGTO_TIT = ?, 
                    VL_PGTO_TIT = ?,
                    Data_Transf_baixa = ?
            """
            
            params = [data_ocorrencia, valor_pago, datetime.now()]
            
            # VBA: If Juros > 0 Then RsTitulo("VL_JUROS_TIT") = Juros
            if juros > 0:
                sql += ", VL_JUROS_TIT = ?"
                params.append(juros)
            
            sql += " WHERE NR_NNR_TIT = ?"
            params.append(nosso_numero)
            
            cursor.execute(sql, params)
            
            self.logger.info(f"✓ Título PAGO: {nosso_numero} - "
                           f"Valor: R$ {valor_pago:.2f}, Juros: R$ {juros:.2f}, "
                           f"Data: {data_ocorrencia}")
            return 'baixa'
            
        except Exception as e:
            self.logger.error(f"Erro ao processar baixa: {e}")
            raise
    
    def _executar_consultas_alexandre(self, cursor):
        """
        Executa as 3 consultas do Alexandre após processar os títulos.
        Conforme manual - deve ser executado após importar o arquivo CBR724.
        
        Passo 1: Ativa todos os títulos (Situacao = 'A')
        Passo 2: Ativa todos os módulos (Situacao = 'A')  
        Passo 3: Inativa títulos e módulos vencidos pendentes (Situacao = 'I')
        """
        try:
            # PASSO 1: Ativa todos os títulos
            self.logger.debug("Executando Alexandre Passo 1: Ativando todos os títulos...")
            sql1 = """
                UPDATE pcjTITULOS
                SET pcjTITULOS.Situacao = 'A'
                WHERE pcjTITULOS.Situacao <> 'A'
            """
            cursor.execute(sql1)
            count1 = cursor.rowcount
            self.logger.info(f"✓ Passo 1: {count1} títulos ativados")
            
            # PASSO 2: Ativa todos os módulos
            self.logger.debug("Executando Alexandre Passo 2: Ativando todos os módulos...")
            sql2 = """
                UPDATE pcjMODULO
                SET pcjMODULO.Situacao = 'A'
                WHERE pcjMODULO.Situacao <> 'A'
            """
            cursor.execute(sql2)
            count2 = cursor.rowcount
            self.logger.info(f"✓ Passo 2: {count2} módulos ativados")
            
            # PASSO 3: Inativa títulos vencidos não pagos e seus módulos
            self.logger.debug("Executando Alexandre Passo 3: Inativando títulos vencidos...")
            sql3 = """
                UPDATE pcjMODULO
                INNER JOIN pcjTITULOS ON pcjMODULO.ID_PCJ = pcjTITULOS.CD_SAC
                SET pcjTITULOS.Situacao = 'I',
                    pcjMODULO.Situacao = 'I'
                WHERE pcjTITULOS.ID_CONTROLE = 1
                  AND pcjTITULOS.DT_VCM_TIT < Now()
            """
            cursor.execute(sql3)
            count3 = cursor.rowcount
            self.logger.info(f"✓ Passo 3: {count3} títulos/módulos vencidos inativados")
            
            # Commit das consultas
            self.conn_baixa.commit()
            self.logger.info("✅ Consultas do Alexandre executadas com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao executar consultas do Alexandre: {e}")
            self.conn_baixa.rollback()
            raise
    
    def fazer_backup(self) -> List[str]:
        """Cria backup dos bancos de dados"""
        backups = []
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pasta_backup = self.config['diretorios']['backup']
            
            # Backup do dbBaixa2025 (obrigatório)
            nome_backup_baixa = f"backup_{timestamp}_dbBaixa2025.accdb"
            caminho_backup_baixa = os.path.join(pasta_backup, nome_backup_baixa)
            shutil.copy2(self.caminho_baixa, caminho_backup_baixa)
            backups.append(caminho_backup_baixa)
            self.logger.info(f"✓ Backup dbBaixa2025: {caminho_backup_baixa}")
            
            # Backup do Cobranca2019 (opcional - apenas se estiver ativo)
            if self.usar_cobranca and self.caminho_cobranca and os.path.exists(self.caminho_cobranca):
                try:
                    nome_backup_cobranca = f"backup_{timestamp}_Cobranca2019.accdb"
                    caminho_backup_cobranca = os.path.join(pasta_backup, nome_backup_cobranca)
                    shutil.copy2(self.caminho_cobranca, caminho_backup_cobranca)
                    backups.append(caminho_backup_cobranca)
                    self.logger.info(f"✓ Backup Cobranca2019: {caminho_backup_cobranca}")
                except Exception as e:
                    self.logger.warning(f"⚠️  Não foi possível fazer backup do Cobranca2019: {e}")
            
            return backups
            
        except Exception as e:
            self.logger.error(f"Erro ao criar backups: {e}")
            raise
    
    def testar_conexao(self) -> bool:
        """Testa a conexão com os bancos"""
        try:
            if self.conectar():
                # Testa dbBaixa2025
                cursor_baixa = self.conn_baixa.cursor()
                cursor_baixa.execute("SELECT COUNT(*) FROM pcjTITULOS")
                count_baixa = cursor_baixa.fetchone()[0]
                self.logger.info(f"✓ dbBaixa2025.pcjTITULOS: {count_baixa} registros")
                
                # Testa Cobranca2019
                cursor_cobranca = self.conn_cobranca.cursor()
                cursor_cobranca.execute("SELECT COUNT(*) FROM pcjCOBRANCA")
                count_cobranca = cursor_cobranca.fetchone()[0]
                self.logger.info(f"✓ Cobranca2019.pcjCOBRANCA: {count_cobranca} registros")
                
                self.desconectar()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erro no teste de conexão: {e}")
            return False
