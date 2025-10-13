# 📚 DOCUMENTAÇÃO COMPLETA DO SISTEMA DE AUTOMAÇÃO CBR724

**Sistema de Monitoramento e Processamento Automático de Retornos Bancários**  
**Versão:** 2.0  
**Data:** 13/10/2025  
**Ambiente:** Windows com Microsoft Access

---

# 📑 ÍNDICE

1. [Visão Geral do Sistema](#visão-geral)
2. [Configuração (config.ini)](#configuração)
3. [Implantação Completa](#implantação)
4. [Sistema em Produção](#produção)
5. [Sistema Watchdog](#watchdog)
6. [Notificações Windows](#notificações)
7. [Comportamento do Monitor](#comportamento)
8. [Changelog](#changelog)
9. [Centralização de Configurações](#centralização)

---

<a name="visão-geral"></a>
# 1️⃣ VISÃO GERAL DO SISTEMA

## O que o sistema faz?

O sistema automatiza o processamento de arquivos de retorno bancário (formato CBR724):

1. **Monitora** pasta de retornos continuamente
2. **Detecta** novos arquivos `.ret` automaticamente
3. **Processa** e integra com banco Access
4. **Gera PDFs** de boletos pagos
5. **Envia notificações** Windows
6. **Move** arquivos processados
7. **Registra logs** de todas operações

## Arquitetura

```
📁 AutomacaoRetorno/
├── 🐍 Python Scripts (7)
│   ├── monitor_retornos.py       → Monitor principal (watchdog)
│   ├── processador_cbr724.py     → Parser formato CBR724
│   ├── integrador_access.py      → Integração Access
│   ├── gerar_pdfs_simples.py     → Geração PDFs
│   ├── notificador_windows.py    → Notificações sistema
│   ├── watchdog_monitor.py       → Monitor do monitor
│   └── config_manager.py         → Gerenciador configuração
│
├── 🔧 PowerShell Scripts (6)
│   ├── _read_config.ps1          → Lê config.ini
│   ├── _start_monitor_hidden.ps1 → Inicia oculto
│   ├── _stop_all_monitors.ps1    → Para monitores
│   ├── _check_monitor.ps1        → Verifica status
│   ├── BACKUP_ONEDRIVE.ps1       → Backup automático
│   └── PROCESSAR_EXISTENTES.ps1  → Processa existentes
│
├── 📝 Interface BAT (6)
│   ├── INICIAR_MONITOR_OCULTO.bat
│   ├── PARAR_MONITOR.bat
│   ├── STATUS_MONITOR.bat
│   ├── PROCESSAR_EXISTENTES.bat
│   ├── INICIAR_WATCHDOG.bat
│   └── PARAR_WATCHDOG.bat
│
└── ⚙️ Configuração
    ├── config.ini               → Configuração central
    └── requirements.txt         → Dependências Python
```

---

<a name="configuração"></a>
# 2️⃣ GUIA DE CONFIGURAÇÃO (config.ini)

## Estrutura Completa

O arquivo `config.ini` centraliza TODAS as configurações do sistema em 8 seções:

### [DIRETORIOS]
```ini
[DIRETORIOS]
dir_trabalho = D:\Teste_Cobrança_Acess\Retorno
dir_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno
```
**Uso:** Monitor detecta ambiente automaticamente

### [ONEDRIVE]
```ini
[ONEDRIVE]
caminho_backup = C:\Users\SeuUsuario\OneDrive\Backup_Retornos
```
**Uso:** Backup automático via BACKUP_ONEDRIVE.ps1

### [CAMINHOS]
```ini
[CAMINHOS]
pasta_retorno = D:\Teste_Cobrança_Acess\Retorno
pasta_processados = D:\Teste_Cobrança_Acess\Retorno\Processados
pasta_erro = D:\Teste_Cobrança_Acess\Retorno\Erro
pasta_backup = D:\Teste_Cobrança_Acess\Backup
```

### [BANCOS_ACCESS]
```ini
[BANCOS_ACCESS]
db_trabalho = D:\Teste_Cobrança_Acess\CBR724.accdb
db_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\CBR724.accdb
```

### [PYTHON]
```ini
[PYTHON]
python_path = python
```

### [LOGS]
```ini
[LOGS]
arquivo_log = monitor_retornos.log
nivel_log = INFO
```

### [PROCESSAMENTO]
```ini
[PROCESSAMENTO]
gerar_pdf = True
mover_processados = True
verificar_duplicados = True
```

### [NOTIFICACOES]
```ini
[NOTIFICACOES]
ativar = True
som = True
duracao = 10
```

### [EMAIL]
```ini
[EMAIL]
ativar = False
smtp_server = smtp.gmail.com
smtp_port = 587
remetente = seu_email@gmail.com
destinatario = destinatario@exemplo.com
senha = sua_senha_app
```

## Como o Sistema Usa config.ini

### Scripts Python
```python
from config_manager import ConfigManager

config = ConfigManager()
pasta = config.pasta_retorno
db = config.banco_access
```

### Scripts PowerShell/BAT
```powershell
. .\AutomacaoRetorno\_read_config.ps1
$pasta = Read-ConfigValue "CAMINHOS" "pasta_retorno"
```

## Alternar Ambientes

**Teste → Produção:**
1. Edite `config.ini`
2. Troque `dir_trabalho` por `dir_producao` na seção `[DIRETORIOS]`
3. Reinicie o monitor

**Produção → Teste:**
1. Volte para `dir_trabalho`
2. Reinicie o monitor

---

<a name="implantação"></a>
# 3️⃣ MANUAL DE IMPLANTAÇÃO COMPLETO

## Pré-requisitos

### Software Necessário
- ✅ Windows 10/11
- ✅ Python 3.8+ instalado
- ✅ Microsoft Access (qualquer versão recente)
- ✅ PowerShell 5.1+

### Verificar Instalações
```powershell
python --version          # Deve mostrar Python 3.8+
Get-Host | Select-Object Version  # PowerShell 5.1+
```

## Passo 1: Instalar Dependências Python

```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
pip install -r requirements.txt
```

**requirements.txt contém:**
```
watchdog==3.0.0
pywin32==306
reportlab==4.0.7
```

## Passo 2: Configurar config.ini

1. Abra `config.ini` no Notepad
2. Configure os caminhos para seu ambiente:
   - `[DIRETORIOS]` - Pastas de retorno
   - `[BANCOS_ACCESS]` - Bancos de dados
   - `[ONEDRIVE]` - Backup (opcional)

## Passo 3: Criar Estrutura de Pastas

```powershell
New-Item -ItemType Directory -Force -Path "D:\Teste_Cobrança_Acess\Retorno"
New-Item -ItemType Directory -Force -Path "D:\Teste_Cobrança_Acess\Retorno\Processados"
New-Item -ItemType Directory -Force -Path "D:\Teste_Cobrança_Acess\Retorno\Erro"
New-Item -ItemType Directory -Force -Path "D:\Teste_Cobrança_Acess\Backup"
```

## Passo 4: Testar Configuração

```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
python config_manager.py
```

Deve mostrar todas as configurações carregadas.

## Passo 5: Primeiro Teste

1. Copie um arquivo `.ret` para a pasta de retorno
2. Execute:
   ```powershell
   .\PROCESSAR_EXISTENTES.bat
   ```
3. Verifique:
   - Log: `monitor_retornos.log`
   - Arquivo movido para `Processados/`
   - PDF gerado (se configurado)
   - Notificação Windows

## Passo 6: Ativar Monitor Permanente

```powershell
.\INICIAR_MONITOR_OCULTO.bat
```

O monitor agora roda em segundo plano!

## Passo 7: Verificar Status

```powershell
.\STATUS_MONITOR.bat
```

## Passo 8: (Opcional) Ativar Watchdog

O watchdog reinicia o monitor se ele cair:

```powershell
.\INICIAR_WATCHDOG.bat
```

---

<a name="produção"></a>
# 4️⃣ SISTEMA EM PRODUÇÃO

## Características do Ambiente de Produção

- **Servidor:** \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\
- **Execução:** Sua máquina monitora o servidor
- **Rede:** SMB/CIFS (compartilhamento Windows)
- **Modo:** Background (oculto)

## Configuração para Produção

### 1. Configurar config.ini

```ini
[DIRETORIOS]
dir_trabalho = D:\Teste_Cobrança_Acess\Retorno
dir_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno  # ← USAR ESTE

[BANCOS_ACCESS]
db_trabalho = D:\Teste_Cobrança_Acess\CBR724.accdb
db_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\CBR724.accdb  # ← USAR ESTE
```

### 2. O Sistema Detecta Automaticamente

O `config_manager.py` detecta qual ambiente usar:
- Se `dir_producao` existe → usa produção
- Se não existe → usa trabalho (teste)

### 3. Iniciar em Produção

```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
.\INICIAR_MONITOR_OCULTO.bat
```

## Monitoramento

### Verificar se está rodando
```powershell
.\STATUS_MONITOR.bat
```

### Ver últimos logs
```powershell
Get-Content monitor_retornos.log -Tail 20
```

### Parar o monitor
```powershell
.\PARAR_MONITOR.bat
```

## Backup Automático

Configure backup no OneDrive:

1. Configure `[ONEDRIVE]` no config.ini
2. Execute:
   ```powershell
   .\BACKUP_ONEDRIVE.ps1
   ```

## Startup Automático

Para iniciar o monitor automaticamente ao ligar o PC:

1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Crie atalho de `INICIAR_MONITOR_OCULTO.bat` nesta pasta

---

<a name="watchdog"></a>
# 5️⃣ SISTEMA WATCHDOG

## O que é o Watchdog?

Um "monitor do monitor" que garante que o sistema principal nunca pare:

- ✅ Verifica se monitor está rodando (60 em 60s)
- ✅ Reinicia automaticamente se detectar queda
- ✅ Envia notificação quando reiniciar
- ✅ Registra tudo em `watchdog.log`

## Como Funciona

```
┌─────────────────────────────────────┐
│     WATCHDOG_MONITOR.PY             │
│  (Verifica a cada 60 segundos)      │
└──────────────┬──────────────────────┘
               │
               ▼
      ┌────────────────┐
      │ Monitor rodando?│
      └────────┬────────┘
               │
        ┌──────┴──────┐
        │             │
       SIM           NÃO
        │             │
        │      ┌──────▼────────┐
        │      │ 1. Notifica   │
        │      │ 2. Reinicia   │
        │      │ 3. Registra   │
        │      └───────────────┘
        │
        ▼
   [Aguarda 60s]
```

## Uso

### Iniciar Watchdog
```powershell
.\INICIAR_WATCHDOG.bat
```

### Parar Watchdog
```powershell
.\PARAR_WATCHDOG.bat
```

### Ver Log do Watchdog
```powershell
Get-Content watchdog.log -Tail 20
```

## Configuração

O watchdog usa `config.ini` automaticamente:
- Lê caminho do Python
- Lê configurações de notificação
- Usa mesmo log do monitor

## Quando Usar

**Recomendado em Produção:**
- Sistema crítico que não pode parar
- Servidor que roda 24/7
- Ambiente sem supervisão constante

**Não necessário em Teste:**
- Desenvolvimento local
- Testes pontuais
- Depuração de problemas

---

<a name="notificações"></a>
# 6️⃣ NOTIFICAÇÕES WINDOWS

## Sistema de Notificações

O sistema envia notificações nativas do Windows 10/11 para eventos importantes.

## Tipos de Notificações

### 1. Arquivo Processado com Sucesso ✅
```
Título: Retorno Processado
Mensagem: arquivo.ret processado com sucesso
         3 registros importados
Ícone: ✅ (verde)
Som: Notificação padrão
```

### 2. Erro no Processamento ❌
```
Título: Erro no Processamento
Mensagem: Falha ao processar arquivo.ret
         Verifique o log para detalhes
Ícone: ❌ (vermelho)
Som: Alerta de erro
```

### 3. Monitor Reiniciado 🔄
```
Título: Monitor Reiniciado
Mensagem: O watchdog detectou queda e reiniciou o monitor
Ícone: 🔄 (azul)
Som: Notificação
```

## Configuração

### Ativar/Desativar Notificações

Edite `config.ini`:
```ini
[NOTIFICACOES]
ativar = True          # True = ligado, False = desligado
som = True             # True = com som, False = silencioso
duracao = 10           # Segundos na tela
```

### Personalizar Mensagens

Edite `notificador_windows.py`:
```python
def notificar_sucesso(arquivo, registros):
    enviar_notificacao(
        titulo="Seu Título",
        mensagem=f"Sua mensagem: {arquivo}",
        icone="info"  # info, warning, error
    )
```

## Requisitos

- ✅ Windows 10/11
- ✅ Biblioteca `pywin32` instalada
- ✅ Central de Notificações ativada no Windows

## Testando Notificações

Execute teste rápido:
```powershell
python -c "from notificador_windows import enviar_notificacao; enviar_notificacao('Teste', 'Sistema funcionando!')"
```

---

<a name="comportamento"></a>
# 7️⃣ COMPORTAMENTO DO MONITOR

## ⚠️ IMPORTANTE: Como o Monitor Detecta Arquivos

### O Que Você Precisa Saber

O monitor usa a biblioteca **watchdog** que:

✅ **DETECTA:** Arquivos criados/copiados DEPOIS que o monitor iniciou  
❌ **NÃO DETECTA:** Arquivos que já estavam na pasta ANTES de iniciar

### Exemplo Prático

```
09:00 → Pasta tem: arquivo1.ret, arquivo2.ret
09:05 → Você inicia o monitor
09:10 → Copia arquivo3.ret para a pasta

RESULTADO:
- arquivo1.ret → NÃO será processado (já estava lá)
- arquivo2.ret → NÃO será processado (já estava lá)
- arquivo3.ret → ✅ SERÁ processado (chegou depois)
```

## Solução: PROCESSAR_EXISTENTES.bat

Para processar arquivos que já estão na pasta:

```powershell
.\PROCESSAR_EXISTENTES.bat
```

Este script:
1. Para o monitor
2. Processa todos `.ret` na pasta
3. Reinicia o monitor

## Workflow Recomendado

### Ao Iniciar o Sistema pela Primeira Vez
```powershell
# 1. Primeiro processe arquivos existentes
.\PROCESSAR_EXISTENTES.bat

# 2. Depois inicie o monitor para novos arquivos
.\INICIAR_MONITOR_OCULTO.bat
```

### Operação Normal
```powershell
# Monitor já rodando detecta automaticamente novos arquivos
# Nenhuma ação necessária
```

### Após Reiniciar o Computador
```powershell
# 1. Processar existentes (caso tenha acumulado)
.\PROCESSAR_EXISTENTES.bat

# 2. Iniciar monitor novamente
.\INICIAR_MONITOR_OCULTO.bat
```

## Detecção de Arquivos

### O que o Monitor Detecta
- ✅ Arquivo copiado para pasta
- ✅ Arquivo criado na pasta
- ✅ Arquivo movido para pasta
- ✅ Arquivo renomeado para `.ret`

### O que o Monitor NÃO Detecta
- ❌ Arquivos já presentes antes do início
- ❌ Modificações em arquivos existentes
- ❌ Arquivos em subpastas

## Logs

Tudo é registrado em `monitor_retornos.log`:

```
2025-10-13 09:27:15 - INFO - Monitor iniciado
2025-10-13 09:27:15 - INFO - Monitorando: D:\Retorno
2025-10-13 09:30:22 - INFO - Novo arquivo detectado: CBR724.ret
2025-10-13 09:30:23 - INFO - Processando: CBR724.ret
2025-10-13 09:30:25 - INFO - Sucesso: 15 registros importados
```

---

<a name="changelog"></a>
# 8️⃣ CHANGELOG - Histórico de Mudanças

## [2.0.0] - 13/10/2025

### 🎯 Centralização de Configurações
- ✅ Criado `config.ini` centralizado (8 seções)
- ✅ Criado `_read_config.ps1` para scripts BAT/PS1
- ✅ Todos scripts agora leem de `config.ini`
- ✅ Eliminados caminhos hardcoded em 100% dos scripts

### 🗑️ Limpeza de Arquivos
- ✅ Removidos 16 arquivos desnecessários (32,7% redução)
- ✅ 49 → 36 arquivos
- ✅ Consolidada documentação em arquivo único
- ✅ Removidas pastas de backup antigas (V2, V3)

### 📚 Documentação
- ✅ Criado `ANALISE_FINAL_POS_LIMPEZA.md`
- ✅ Criado `COMPORTAMENTO_MONITOR.md`
- ✅ Criado `DOCUMENTACAO_SISTEMA.md` (este arquivo)

## [1.5.0] - 10/10/2025

### 🔧 Sistema Watchdog
- ✅ Implementado watchdog_monitor.py
- ✅ Criados INICIAR_WATCHDOG.bat e PARAR_WATCHDOG.bat
- ✅ Auto-restart do monitor em caso de queda
- ✅ Notificações de reinicialização

### 🔔 Notificações Windows
- ✅ Implementado notificador_windows.py
- ✅ Notificações nativas Windows 10/11
- ✅ Configurável via config.ini
- ✅ Sons personalizáveis

## [1.0.0] - 08/10/2025

### 🚀 Versão Inicial
- ✅ Monitor de arquivos com watchdog
- ✅ Processador CBR724
- ✅ Integração com Access
- ✅ Geração de PDFs
- ✅ Scripts BAT de interface
- ✅ Logs detalhados

---

<a name="centralização"></a>
# 9️⃣ CENTRALIZAÇÃO DE CONFIGURAÇÕES

## O Problema Antes

Caminhos espalhados em **15 arquivos diferentes**:
- `monitor_retornos.py` → caminhos hardcoded
- `integrador_access.py` → banco hardcoded
- `INICIAR_MONITOR.bat` → pasta hardcoded
- etc...

**Resultado:** Difícil manter e atualizar

## A Solução: config.ini

**1 arquivo** centraliza TUDO:
- ✅ Caminhos de pastas
- ✅ Bancos de dados
- ✅ Configurações de processamento
- ✅ Configurações de notificações
- ✅ Configurações de log

## Como Foi Implementado

### Estrutura

```
config.ini (FONTE ÚNICA DA VERDADE)
     ↓
     ├─→ config_manager.py (Python lê daqui)
     │        ↓
     │        ├─→ monitor_retornos.py
     │        ├─→ processador_cbr724.py
     │        ├─→ integrador_access.py
     │        ├─→ gerar_pdfs_simples.py
     │        └─→ notificador_windows.py
     │
     └─→ _read_config.ps1 (PowerShell/BAT lê daqui)
              ↓
              ├─→ INICIAR_MONITOR_OCULTO.bat
              ├─→ STATUS_MONITOR.bat
              ├─→ PARAR_MONITOR.bat
              ├─→ PROCESSAR_EXISTENTES.bat
              └─→ BACKUP_ONEDRIVE.ps1
```

## Mudanças Aplicadas

### Antes (hardcoded)
```python
# monitor_retornos.py
PASTA_RETORNO = "D:\\Teste_Cobrança_Acess\\Retorno"
```

### Depois (config.ini)
```python
# monitor_retornos.py
from config_manager import ConfigManager
config = ConfigManager()
PASTA_RETORNO = config.pasta_retorno
```

## Benefícios

### 1. Manutenção Simples
- Mudar caminho? → Edita 1 linha no config.ini
- Antes: Editar 15 arquivos diferentes

### 2. Alternar Ambientes
- Teste → Produção: Troca 1 variável
- Sem reescrever código

### 3. Sem Erros
- Configuração centralizada = sem inconsistências
- Validação automática pelo config_manager

### 4. Fácil Debug
- Todos caminhos visíveis em 1 arquivo
- `python config_manager.py` mostra tudo

## Arquivos Atualizados

### Python (5 arquivos)
- ✅ monitor_retornos.py
- ✅ processador_cbr724.py
- ✅ integrador_access.py
- ✅ gerar_pdfs_simples.py
- ✅ watchdog_monitor.py

### PowerShell (3 arquivos)
- ✅ BACKUP_ONEDRIVE.ps1
- ✅ PROCESSAR_EXISTENTES.ps1
- ✅ _start_monitor_hidden.ps1

### BAT (4 arquivos)
- ✅ INICIAR_MONITOR_OCULTO.bat
- ✅ STATUS_MONITOR.bat
- ✅ PARAR_MONITOR.bat
- ✅ PROCESSAR_EXISTENTES.bat

---

# 🆘 SOLUÇÃO DE PROBLEMAS

## Monitor não detecta arquivos

**Causa:** Arquivos já estavam na pasta antes de iniciar  
**Solução:** Execute `PROCESSAR_EXISTENTES.bat`

## Access não abre banco

**Causa:** Caminho do banco incorreto no config.ini  
**Solução:** 
```powershell
python config_manager.py  # Ver caminho configurado
# Editar config.ini se necessário
```

## Notificações não aparecem

**Causa:** Central de Notificações desativada  
**Solução:**
1. Configurações Windows
2. Sistema → Notificações
3. Ativar notificações

## Erro "watchdog not found"

**Causa:** Biblioteca não instalada  
**Solução:**
```powershell
pip install watchdog
```

## Monitor para sozinho

**Causa:** Erro não tratado  
**Solução:**
1. Ver log: `monitor_retornos.log`
2. Ativar watchdog: `INICIAR_WATCHDOG.bat`

---

# 📞 REFERÊNCIA RÁPIDA

## Comandos Principais

```powershell
# Iniciar sistema
.\INICIAR_MONITOR_OCULTO.bat

# Ver status
.\STATUS_MONITOR.bat

# Parar sistema
.\PARAR_MONITOR.bat

# Processar arquivos existentes
.\PROCESSAR_EXISTENTES.bat

# Fazer backup
.\BACKUP_ONEDRIVE.ps1

# Ver configuração
python config_manager.py

# Ver últimos logs
Get-Content monitor_retornos.log -Tail 20
```

## Estrutura de Pastas

```
D:\Teste_Cobrança_Acess\
├── Retorno\              ← Arquivos de entrada
│   ├── Processados\      ← Sucesso
│   └── Erro\             ← Falhas
├── Backup\               ← Backup local
└── AutomacaoRetorno\     ← Scripts do sistema
```

## Arquivos de Configuração

- `config.ini` - Configuração principal
- `requirements.txt` - Dependências Python
- `.gitignore` - Controle de versão

## Arquivos de Log

- `monitor_retornos.log` - Log principal
- `watchdog.log` - Log do watchdog

---

**📅 Última Atualização:** 13/10/2025  
**👤 Autor:** Sistema de Automação CBR724  
**📧 Suporte:** Verifique os logs em caso de problemas
