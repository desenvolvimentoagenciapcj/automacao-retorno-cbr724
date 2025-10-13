# 📋 Centralização de Configurações no config.ini

## 🎯 Objetivo

Todos os caminhos e diretórios fixos foram removidos dos códigos e centralizados no arquivo `config.ini`. Isso torna o sistema:

- ✅ **Mais fácil de reimplantar** (só precisa editar config.ini)
- ✅ **Mais flexível** (suporta diferentes ambientes)
- ✅ **Mais profissional** (separação de código e configuração)
- ✅ **Menos propenso a erros** (um único lugar para configurar tudo)

---

## 📁 Novas Seções no config.ini

### **[DIRETORIOS]**
Caminhos dos diretórios de trabalho

```ini
[DIRETORIOS]
# Diretório raiz de trabalho local (onde ficam os scripts Python)
dir_trabalho = D:\Teste_Cobrança_Acess\AutomacaoRetorno

# Diretório de produção no servidor (para implantação)
dir_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno
```

### **[ONEDRIVE]**
Caminho para backup no OneDrive

```ini
[ONEDRIVE]
# Caminho do backup no OneDrive
caminho_backup = F:\OneDrive - Fundacao Agencia das Bacias PCJ\Repositorio_TI\Manuais\SCPCJ\AutomaçãoDbBaixa
```

---

## 🔧 Arquivos Atualizados

### **Python**

#### `config_manager.py`
- ✅ Adicionado suporte para seção `[DIRETORIOS]`
- ✅ Adicionado suporte para seção `[ONEDRIVE]`
- ✅ Adicionado suporte completo para `[NOTIFICACOES]`
- ✅ Adicionado suporte completo para `[EMAIL]`
- ✅ Novos métodos:
  - `dir_trabalho` - Diretório de trabalho local
  - `dir_producao` - Diretório de produção
  - `onedrive_backup` - Caminho do backup OneDrive
  - `notificacoes_habilitadas` - Flag de notificações Windows
  - `email_habilitado`, `email_smtp_servidor`, `email_smtp_porta`, etc.

### **PowerShell**

#### `_read_config.ps1` (NOVO)
Script auxiliar para ler valores do config.ini em scripts BAT/PS1

**Uso:**
```powershell
powershell -File "_read_config.ps1" -Secao "CAMINHOS" -Chave "pasta_retorno"
```

#### `BACKUP_ONEDRIVE.ps1`
- ✅ Agora lê `dir_trabalho` e `onedrive_backup` do config.ini
- ❌ Removido caminho fixo: `D:\Teste_Cobrança_Acess\AutomacaoRetorno`
- ❌ Removido caminho fixo: `F:\OneDrive - Fundacao...`

#### `PROCESSAR_EXISTENTES.ps1`
- ✅ Agora lê `pasta_retorno` do config.ini
- ❌ Removido caminho fixo: `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno`

### **Batch Scripts**

#### `INICIAR_MONITOR_OCULTO.bat`
- ✅ Agora lê `dir_trabalho` do config.ini usando `_read_config.ps1`
- ❌ Removido caminho fixo: `D:\Teste_Cobrança_Acess\AutomacaoRetorno`

#### `STATUS_MONITOR.bat`
- ✅ Agora lê `pasta_retorno` e `pasta_processados` do config.ini
- ❌ Removido caminho fixo: `D:\Teste_Cobrança_Acess\Retorno`
- ❌ Removido caminho fixo: `D:\Teste_Cobrança_Acess\Retorno\Processados`

---

## 🚀 Como Reimplantar em Outro Ambiente

Agora ficou MUITO mais fácil reimplantar o sistema:

### **1. Copie todos os arquivos**
```
- Python/
- Scripts/
- Configuracao/
- Documentacao/
```

### **2. Edite APENAS o config.ini**

Altere as seções `[DIRETORIOS]`, `[CAMINHOS]`, `[BANCOS_ACCESS]`, `[PYTHON]` e `[ONEDRIVE]` conforme o novo ambiente:

```ini
[DIRETORIOS]
dir_trabalho = C:\MeuNovoCaminho\AutomacaoRetorno
dir_producao = \\SERVIDOR2\Pasta\AutomacaoRetorno

[CAMINHOS]
pasta_retorno = \\SERVIDOR2\Pasta\Retorno
pasta_processados = \\SERVIDOR2\Pasta\Retorno\Processados
pasta_erro = \\SERVIDOR2\Pasta\Retorno\Erro
pasta_backup = \\SERVIDOR2\Pasta\backup

[BANCOS_ACCESS]
db_baixa = \\SERVIDOR2\Pasta\dbBaixa2025.accdb
db_cobranca = \\SERVIDOR2\Pasta\Cobranca2019.accdb

[PYTHON]
executavel = C:\Python\python.exe

[ONEDRIVE]
caminho_backup = D:\OneDrive\MeuBackup
```

### **3. Pronto!**
Todos os scripts vão usar automaticamente os novos caminhos. **Não precisa editar nenhum código!**

---

## ✅ Benefícios

| Antes | Depois |
|-------|--------|
| Caminhos espalhados em 10+ arquivos | Um único arquivo (config.ini) |
| Reimplantar = editar vários arquivos | Reimplantar = editar config.ini |
| Difícil de manter | Fácil de manter |
| Código misturado com config | Código separado de config |

---

## 🧪 Testar Configuração

Execute:
```bash
python config_manager.py
```

Vai exibir todas as configurações carregadas. Verifique se está tudo correto!

---

## 📌 Importante

- ⚠️ **Sempre use `\\` (barras duplas)** para caminhos de rede no Windows
- ⚠️ **Não use aspas** nos valores do config.ini
- ⚠️ **Caminhos locais usam `\`** (barra invertida simples)
- ✅ **Comentários começam com `#`**

**Exemplo correto:**
```ini
pasta_retorno = \\SERVIDOR1\CobrancaPCJ\Retorno
dir_trabalho = D:\Teste\AutomacaoRetorno
```

**Exemplo ERRADO:**
```ini
pasta_retorno = "\\SERVIDOR1\CobrancaPCJ\Retorno"  ❌ (não use aspas)
dir_trabalho = D:/Teste/AutomacaoRetorno           ❌ (use \ não /)
```

---

## 📚 Arquivos Relacionados

- `config.ini` - Arquivo de configuração principal
- `config_manager.py` - Gerenciador de configurações Python
- `_read_config.ps1` - Leitor de configurações PowerShell
- `GUIA_CONFIG.md` - Guia completo do config.ini
