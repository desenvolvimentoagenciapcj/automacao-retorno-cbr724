#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Web para Monitoramento
Interface web para acompanhar o processamento de arquivos de retorno
"""

import os
import json
import yaml
import logging
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from processador_cnab import ProcessadorCNAB
from integrador_access import IntegradorAccess

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # ALTERAR EM PRODUÇÃO

# Configurações globais
config = None
logger = None

def carregar_configuracoes():
    """Carrega configurações do arquivo YAML"""
    global config
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return True
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return False

def verificar_autenticacao():
    """Verifica se o usuário está autenticado"""
    return session.get('autenticado', False)

@app.route('/')
def index():
    """Página inicial do dashboard"""
    if not verificar_autenticacao():
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == config['web']['senha_admin']:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro="Senha incorreta")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do sistema"""
    session.pop('autenticado', None)
    return redirect(url_for('login'))

@app.route('/api/status')
def api_status():
    """API para obter status do sistema"""
    if not verificar_autenticacao():
        return jsonify({'erro': 'Não autenticado'}), 401
    
    try:
        # Verificar conexão com Access
        integrador = IntegradorAccess(config)
        conexao_ok = integrador.testar_conexao()
        
        # Contar arquivos pendentes
        pasta_entrada = config['diretorios']['entrada']
        arquivos_pendentes = len([f for f in os.listdir(pasta_entrada) 
                                if os.path.isfile(os.path.join(pasta_entrada, f))])
        
        # Estatísticas do dia
        estatisticas_hoje = obter_estatisticas_hoje()
        
        return jsonify({
            'status': 'online',
            'conexao_access': conexao_ok,
            'arquivos_pendentes': arquivos_pendentes,
            'estatisticas': estatisticas_hoje,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/arquivos')
def api_arquivos():
    """API para listar arquivos processados"""
    if not verificar_autenticacao():
        return jsonify({'erro': 'Não autenticado'}), 401
    
    try:
        arquivos = []
        
        # Arquivos processados
        pasta_processados = config['diretorios']['processados']
        if os.path.exists(pasta_processados):
            for arquivo in os.listdir(pasta_processados):
                caminho = os.path.join(pasta_processados, arquivo)
                if os.path.isfile(caminho):
                    stat = os.stat(caminho)
                    arquivos.append({
                        'nome': arquivo,
                        'status': 'Processado',
                        'data_modificacao': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'tamanho': stat.st_size
                    })
        
        # Arquivos com erro
        pasta_erro = config['diretorios']['erro']
        if os.path.exists(pasta_erro):
            for arquivo in os.listdir(pasta_erro):
                caminho = os.path.join(pasta_erro, arquivo)
                if os.path.isfile(caminho):
                    stat = os.stat(caminho)
                    arquivos.append({
                        'nome': arquivo,
                        'status': 'Erro',
                        'data_modificacao': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'tamanho': stat.st_size
                    })
        
        # Ordenar por data (mais recente primeiro)
        arquivos.sort(key=lambda x: x['data_modificacao'], reverse=True)
        
        return jsonify(arquivos[:50])  # Últimos 50 arquivos
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/logs')
def api_logs():
    """API para obter logs recentes"""
    if not verificar_autenticacao():
        return jsonify({'erro': 'Não autenticado'}), 401
    
    try:
        pasta_logs = config['diretorios']['logs']
        log_hoje = os.path.join(pasta_logs, f"monitor_{datetime.now().strftime('%Y%m%d')}.log")
        
        logs = []
        if os.path.exists(log_hoje):
            with open(log_hoje, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                # Pegar últimas 100 linhas
                for linha in linhas[-100:]:
                    linha = linha.strip()
                    if linha:
                        logs.append(linha)
        
        return jsonify(logs)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/processar/<arquivo>')
def api_processar_arquivo(arquivo):
    """API para processar arquivo específico manualmente"""
    if not verificar_autenticacao():
        return jsonify({'erro': 'Não autenticado'}), 401
    
    try:
        pasta_entrada = config['diretorios']['entrada']
        caminho_arquivo = os.path.join(pasta_entrada, arquivo)
        
        if not os.path.exists(caminho_arquivo):
            return jsonify({'erro': 'Arquivo não encontrado'}), 404
        
        # Processar arquivo
        processador = ProcessadorCNAB(config)
        integrador = IntegradorAccess(config)
        
        registros = processador.processar_arquivo(caminho_arquivo)
        resultado = integrador.processar_registros(registros)
        
        return jsonify({
            'sucesso': True,
            'resultado': resultado,
            'total_registros': len(registros)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

def obter_estatisticas_hoje():
    """Obtém estatísticas do dia atual"""
    try:
        hoje = datetime.now().date()
        
        # Contar arquivos processados hoje
        pasta_processados = config['diretorios']['processados']
        arquivos_hoje = 0
        
        if os.path.exists(pasta_processados):
            for arquivo in os.listdir(pasta_processados):
                caminho = os.path.join(pasta_processados, arquivo)
                if os.path.isfile(caminho):
                    data_mod = datetime.fromtimestamp(os.path.getmtime(caminho)).date()
                    if data_mod == hoje:
                        arquivos_hoje += 1
        
        # Contar arquivos com erro hoje
        pasta_erro = config['diretorios']['erro']
        erros_hoje = 0
        
        if os.path.exists(pasta_erro):
            for arquivo in os.listdir(pasta_erro):
                caminho = os.path.join(pasta_erro, arquivo)
                if os.path.isfile(caminho):
                    data_mod = datetime.fromtimestamp(os.path.getmtime(caminho)).date()
                    if data_mod == hoje:
                        erros_hoje += 1
        
        return {
            'arquivos_processados': arquivos_hoje,
            'arquivos_erro': erros_hoje,
            'total_arquivos': arquivos_hoje + erros_hoje
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return {
            'arquivos_processados': 0,
            'arquivos_erro': 0,
            'total_arquivos': 0
        }

# Templates HTML embutidos (para simplificar a instalação)
@app.route('/templates/dashboard.html')
def template_dashboard():
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Retorno Bancário</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .status-card { transition: all 0.3s ease; }
        .status-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .log-container { max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <span class="navbar-brand">🏦 Sistema de Retorno Bancário</span>
            <a href="/logout" class="btn btn-outline-light">Sair</a>
        </div>
    </nav>
    
    <div class="container mt-4">
        <!-- Status Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card status-card bg-primary text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>Status do Sistema</h6>
                                <h4 id="system-status">Carregando...</h4>
                            </div>
                            <i class="fas fa-server fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card bg-success text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>Arquivos Processados</h6>
                                <h4 id="arquivos-processados">0</h4>
                            </div>
                            <i class="fas fa-check-circle fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card bg-warning text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>Arquivos Pendentes</h6>
                                <h4 id="arquivos-pendentes">0</h4>
                            </div>
                            <i class="fas fa-clock fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card bg-danger text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>Arquivos com Erro</h6>
                                <h4 id="arquivos-erro">0</h4>
                            </div>
                            <i class="fas fa-exclamation-triangle fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tabelas -->
        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-alt"></i> Arquivos Recentes</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped" id="tabela-arquivos">
                                <thead>
                                    <tr>
                                        <th>Nome do Arquivo</th>
                                        <th>Status</th>
                                        <th>Data/Hora</th>
                                        <th>Tamanho</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td colspan="4" class="text-center">Carregando...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-list-alt"></i> Log do Sistema</h5>
                    </div>
                    <div class="card-body">
                        <div class="log-container bg-dark text-light p-3 rounded" id="log-container">
                            Carregando logs...
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Atualizar dados a cada 30 segundos
        setInterval(atualizarDados, 30000);
        
        // Carregar dados iniciais
        atualizarDados();
        
        function atualizarDados() {
            // Status do sistema
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('system-status').textContent = data.status === 'online' ? 'Online' : 'Offline';
                    document.getElementById('arquivos-processados').textContent = data.estatisticas.arquivos_processados;
                    document.getElementById('arquivos-pendentes').textContent = data.arquivos_pendentes;
                    document.getElementById('arquivos-erro').textContent = data.estatisticas.arquivos_erro;
                });
            
            // Lista de arquivos
            fetch('/api/arquivos')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.querySelector('#tabela-arquivos tbody');
                    tbody.innerHTML = '';
                    
                    data.forEach(arquivo => {
                        const tr = document.createElement('tr');
                        const statusBadge = arquivo.status === 'Processado' ? 
                            '<span class="badge bg-success">Processado</span>' : 
                            '<span class="badge bg-danger">Erro</span>';
                        
                        const data_formatada = new Date(arquivo.data_modificacao).toLocaleString('pt-BR');
                        const tamanho_formatado = (arquivo.tamanho / 1024).toFixed(1) + ' KB';
                        
                        tr.innerHTML = `
                            <td>${arquivo.nome}</td>
                            <td>${statusBadge}</td>
                            <td>${data_formatada}</td>
                            <td>${tamanho_formatado}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                });
            
            // Logs
            fetch('/api/logs')
                .then(response => response.json())
                .then(data => {
                    const logContainer = document.getElementById('log-container');
                    logContainer.innerHTML = data.slice(-20).join('<br>');
                    logContainer.scrollTop = logContainer.scrollHeight;
                });
        }
    </script>
</body>
</html>
    '''

@app.route('/templates/login.html')
def template_login():
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sistema de Retorno</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-primary">
    <div class="container">
        <div class="row justify-content-center" style="min-height: 100vh; align-items: center;">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h4 class="card-title text-center mb-4">🏦 Sistema de Retorno</h4>
                        <form method="POST">
                            <div class="mb-3">
                                <label for="senha" class="form-label">Senha de Acesso</label>
                                <input type="password" class="form-control" id="senha" name="senha" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Entrar</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    '''

def main():
    """Função principal para executar o dashboard"""
    if not carregar_configuracoes():
        print("Erro ao carregar configurações!")
        return
    
    global logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Configurações do Flask
    host = config['web']['host']
    porta = config['web']['porta']
    debug = config['web']['debug']
    
    print(f"🌐 Dashboard iniciado em: http://{host}:{porta}")
    print(f"👤 Senha de acesso: {config['web']['senha_admin']}")
    
    app.run(host=host, port=porta, debug=debug)

if __name__ == '__main__':
    main()