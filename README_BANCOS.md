# 💾 Bancos de Dados Access - Localização e Backup

## ❓ Por que os bancos não estão no Git?

Os arquivos de banco de dados Access (`.accdb`) foram **intencionalmente excluídos** do repositório Git por serem:

1. **Muito grandes** (alguns com mais de 50 MB)
2. **Arquivos binários** (não se beneficiam do controle de versão)
3. **Históricos/backup** (não são usados pelo sistema de automação)

## 🎯 Onde o Sistema Busca os Bancos?

O sistema de automação **NÃO usa os bancos locais**. Ele acessa diretamente os bancos no servidor:

```ini
[BANCOS_ACCESS]
# Banco principal (usado pelo sistema)
db_baixa = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb

# Banco secundário (opcional)
db_cobranca = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb
```

**Resultado:** O sistema funciona 100% mesmo sem os bancos históricos locais!

## 📂 Onde Estão os Bancos Históricos?

### 1️⃣ **Backup OneDrive** (Recomendado)
```
F:\OneDrive - Fundacao Agencia das Bacias PCJ\
└── Backup_AutomacaoRetorno\
    └── 2025-10-13_152805\
        └── Teste_Cobrança_Acess\
            └── SISTEMA COBRANÇA\  ← Todos os bancos 2007-2024
```

**Tamanho total:** 9.8 GB  
**Status:** ✅ Backup completo e seguro

### 2️⃣ **Máquina Local** (Se você fez clone original)
```
d:\Teste_Cobrança_Acess\
├── SISTEMA COBRANÇA\           ← Bancos históricos (2007-2024)
│   ├── 2007\
│   ├── 2008\
│   ├── ...
│   └── 2024\
└── dbBaixa2025.accdb           ← Banco atual (cópia local)
```

**Nota:** Esses arquivos existem apenas na máquina onde foi feito o backup original.

### 3️⃣ **Servidor de Produção** (Bancos ativos)
```
\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\
├── dbBaixa2025.accdb           ← Usado pelo sistema
└── Cobranca2019.accdb          ← Usado pelo sistema
```

**Status:** ✅ Estes são os bancos que o sistema realmente usa!

## 🚀 Após Clonar o Repositório

Quando você clonar o repositório em outra máquina:

### ✅ **O que você TEM:**
- ✅ Todo o código Python (scripts/)
- ✅ Configurações (config/)
- ✅ Documentação (docs/)
- ✅ Scripts BAT e PowerShell
- ✅ Sistema 100% funcional

### ❌ **O que você NÃO tem:**
- ❌ Pasta `SISTEMA COBRANÇA/` (bancos históricos 2007-2024)
- ❌ `dbBaixa2025.accdb` local (cópia de backup)
- ❌ Bancos antigos de teste

### 🎯 **Precisa funcionar?**
**SIM!** O sistema funciona perfeitamente porque:
1. Acessa os bancos no servidor (`\\SERVIDOR1\...`)
2. Não depende de bancos locais
3. Os bancos históricos são apenas para consulta/backup

## 📋 Quando Você Precisa dos Bancos Históricos?

### Cenário 1: Análise de Dados Antigos
**Solução:** Baixe do backup OneDrive
```
Acesse: F:\OneDrive - Fundacao Agencia das Bacias PCJ\
        Backup_AutomacaoRetorno\2025-10-13_152805\
```

### Cenário 2: Restaurar Sistema Completo
**Solução:** 
1. Clone o repositório (código)
2. Copie bancos do backup OneDrive (dados)

### Cenário 3: Desenvolvimento/Teste Local
**Solução:**
1. Sistema usa bancos do servidor (não precisa de cópias locais)
2. Para testes offline, copie apenas o banco necessário do OneDrive

## 📊 Estrutura dos Arquivos Ignorados

Arquivos no `.gitignore`:
```gitignore
# Bancos Access históricos (grandes - mantidos apenas no backup OneDrive)
SISTEMA COBRANÇA/
dbBaixa*.accdb
Cobranca*.accdb
```

**Benefícios:**
- ✅ Repositório Git leve e rápido
- ✅ Clone em segundos (não em horas)
- ✅ Sem alertas do GitHub sobre arquivos grandes
- ✅ Backup seguro no OneDrive

## 🔍 Verificar Bancos Disponíveis

### Verificar bancos no servidor:
```powershell
# Ver bancos em produção
Get-ChildItem "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\*.accdb"
```

### Verificar backup OneDrive:
```powershell
# Ver todos os backups
Get-ChildItem "F:\OneDrive - Fundacao Agencia das Bacias PCJ\Backup_AutomacaoRetorno\" -Recurse -Filter "*.accdb"
```

## ❓ Perguntas Frequentes

### 1. O sistema vai funcionar após clonar?
**Sim!** 100%. O sistema usa bancos do servidor, não locais.

### 2. Preciso baixar os bancos históricos?
**Não**, a menos que precise consultar dados antigos (2007-2024).

### 3. Onde estão os bancos de produção?
No servidor: `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\`

### 4. Como restaurar um banco antigo?
Baixe do backup OneDrive: `Backup_AutomacaoRetorno\2025-10-13_152805\`

### 5. Posso adicionar os bancos ao Git?
**Não recomendado**. São muito grandes (>50MB) e causam problemas:
- ⚠️ Clone extremamente lento
- ⚠️ Alertas do GitHub
- ⚠️ Git não é ideal para binários grandes
- ✅ Melhor: Manter no OneDrive

## 📞 Suporte

Se precisar dos bancos históricos ou tiver dúvidas:
1. Acesse o backup OneDrive
2. Consulte `docs/DOCUMENTACAO_SISTEMA.md`
3. Contate o TI: backoffice@agencia.baciaspcj.org.br

---

**Última atualização:** 13/10/2025  
**Versão do sistema:** 2.0  
**Tamanho do backup OneDrive:** 9.8 GB  
**Bancos históricos:** 2007-2024 (70 arquivos)
