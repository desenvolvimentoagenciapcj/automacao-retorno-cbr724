# 🚀 Sistema de Automação de Retornos Bancários CBR724

**Versão:** 2.0  
**Data:** 13/10/2025  
**Status:** ✅ Produção

---

## 📁 ESTRUTURA DO PROJETO

```
AutomacaoRetorno/
│
├── 📝 INICIAR.bat          ← Inicia o monitor (ATALHO RÁPIDO)
├── ⏹️  PARAR.bat            ← Para o monitor (ATALHO RÁPIDO)
├── 📊 STATUS.bat           ← Ver status (ATALHO RÁPIDO)
├── 🔄 PROCESSAR.bat        ← Processar existentes (ATALHO RÁPIDO)
│
├── 📂 scripts/
│   ├── python/             ← Scripts Python (7 arquivos)
│   │   ├── config_manager.py
│   │   ├── monitor_retornos.py
│   │   ├── processador_cbr724.py
│   │   ├── integrador_access.py
│   │   ├── gerar_pdfs_simples.py
│   │   ├── notificador_windows.py
│   │   └── watchdog_monitor.py
│   │
│   ├── powershell/         ← Scripts PowerShell (6 arquivos)
│   │   ├── _read_config.ps1
│   │   ├── _start_monitor_hidden.ps1
│   │   ├── _stop_all_monitors.ps1
│   │   ├── _check_monitor.ps1
│   │   ├── BACKUP_ONEDRIVE.ps1
│   │   └── PROCESSAR_EXISTENTES.ps1
│   │
│   └── bat/                ← Scripts BAT (6 arquivos)
│       ├── INICIAR_MONITOR_OCULTO.bat
│       ├── PARAR_MONITOR.bat
│       ├── STATUS_MONITOR.bat
│       ├── PROCESSAR_EXISTENTES.bat
│       ├── INICIAR_WATCHDOG.bat
│       └── PARAR_WATCHDOG.bat
│
├── ⚙️  config/              ← Configurações
│   ├── config.ini          ← Configuração central
│   ├── requirements.txt    ← Dependências Python
│   └── .gitignore
│
├── 📊 logs/                ← Logs do sistema
│   ├── monitor_retornos.log
│   └── watchdog.log
│
└── 📚 docs/                ← Documentação
    └── DOCUMENTACAO_SISTEMA.md  ← Manual completo
```

---

## ⚡ INÍCIO RÁPIDO

### 1️⃣ Iniciar o Sistema
```batch
INICIAR.bat
```

### 2️⃣ Verificar Status
```batch
STATUS.bat
```

### 3️⃣ Parar o Sistema
```batch
PARAR.bat
```

### 4️⃣ Processar Arquivos Existentes
```batch
PROCESSAR.bat
```

---

## 📖 DOCUMENTAÇÃO COMPLETA

Para informações detalhadas, veja:
- **Manual Completo:** `docs\DOCUMENTACAO_SISTEMA.md`
- **Configuração:** `config\config.ini`

---

## 🔧 CONFIGURAÇÃO

Toda configuração está centralizada em: **`config\config.ini`**

### Seções Principais:
- `[DIRETORIOS]` - Pastas de trabalho/produção
- `[BANCOS_ACCESS]` - Caminhos dos bancos de dados
- `[CAMINHOS]` - Pastas retorno/processados/erro
- `[PROCESSAMENTO]` - Opções de processamento
- `[NOTIFICACOES]` - Configuração de alertas

---

## 🎯 ORGANIZAÇÃO POR FUNÇÃO

### Preciso processar arquivos?
→ Use: **`PROCESSAR.bat`** (raiz)
→ Ou: `scripts\bat\PROCESSAR_EXISTENTES.bat`

### Preciso configurar o sistema?
→ Edite: **`config\config.ini`**
→ Veja: `docs\DOCUMENTACAO_SISTEMA.md`

### Preciso ver logs?
→ Veja: **`logs\monitor_retornos.log`**
→ Ou: `logs\watchdog.log`

### Preciso modificar código Python?
→ Edite: **`scripts\python\*.py`**

### Preciso modificar automação?
→ Edite: **`scripts\powershell\*.ps1`**
→ Ou: `scripts\bat\*.bat`

---

## 💡 BENEFÍCIOS DA NOVA ESTRUTURA

### ✅ Organização Clara
- Cada tipo de arquivo em sua pasta
- Fácil localizar o que precisa
- Estrutura profissional

### ✅ Acesso Rápido
- Atalhos na raiz para comandos principais
- Não precisa navegar em pastas
- Uso diário simplificado

### ✅ Manutenção Facilitada
- Código separado por tecnologia
- Configuração centralizada
- Logs isolados

### ✅ Escalabilidade
- Fácil adicionar novos scripts
- Estrutura modular
- Separação de responsabilidades

---

## 📊 ESTATÍSTICAS

- **Total de arquivos:** 29 (25 essenciais + 4 atalhos)
- **Redução da bagunça:** 51% (de 49 para 25 arquivos essenciais)
- **Documentação:** Consolidada em 1 arquivo único
- **Configuração:** 100% centralizada

---

## 🆘 SUPORTE

### Problemas?
1. Veja `logs\monitor_retornos.log`
2. Execute `STATUS.bat`
3. Consulte `docs\DOCUMENTACAO_SISTEMA.md`

### Dúvidas sobre configuração?
→ Veja seção **"Configuração"** na documentação completa

---

## 📅 HISTÓRICO

- **v2.0** (13/10/2025) - Reorganização completa em pastas + Consolidação de docs
- **v1.5** (10/10/2025) - Watchdog + Notificações Windows
- **v1.0** (08/10/2025) - Versão inicial

---

**🎉 Sistema Otimizado, Organizado e Pronto para Produção!**
