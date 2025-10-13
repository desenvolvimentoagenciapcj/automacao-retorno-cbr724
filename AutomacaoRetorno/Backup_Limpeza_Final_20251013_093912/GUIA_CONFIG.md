# 📋 GUIA DO CONFIG.INI

**Data:** 10/10/2025
**Versão:** 2.1 com todas as configurações centralizadas

---

## 🎯 O QUE É?

O `config.ini` é o **arquivo de configuração centralizada** do sistema. 

**Vantagens:**
- ✅ **Manutenção fácil** - Muda só 1 arquivo para ajustar tudo
- ✅ **Sem recompilar** - Não precisa mexer em código Python
- ✅ **Portabilidade** - Copia para outra máquina e ajusta só o config.ini
- ✅ **Documentação clara** - Todas as configurações em um só lugar
- ✅ **Backup simples** - Fácil versionar e restaurar configurações
- ✅ **Zero hardcode** - Nenhum caminho fixo nos códigos

---

## 📂 ESTRUTURA DO CONFIG.INI

### `[DIRETORIOS]` - Diretórios de Trabalho ⭐ NOVO

```ini
[DIRETORIOS]
# Diretório raiz de trabalho local (onde ficam os scripts Python)
dir_trabalho = D:\Teste_Cobrança_Acess\AutomacaoRetorno

# Diretório de produção no servidor (para implantação)
dir_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno
```

**Quando ajustar:**
- Mudar de máquina
- Reimplantar em outro ambiente
- Mover pasta de trabalho

**Usado por:**
- Todos os scripts BAT
- BACKUP_ONEDRIVE.ps1
- PROCESSAR_EXISTENTES.ps1

---

### `[CAMINHOS]` - Pastas do Sistema

```ini
[CAMINHOS]
# Pasta monitorada (onde ficam os arquivos .ret para processar)
pasta_retorno = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno

# Pasta para arquivos processados com sucesso
pasta_processados = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Processados

# Pasta para arquivos com erro
pasta_erro = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Erro

# Pasta para backups dos bancos Access
pasta_backup = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup
```

**Quando ajustar:**
- Mudar para outro servidor
- Mudar estrutura de pastas
- Testar em ambiente local antes de produção

---

### `[BANCOS_ACCESS]` - Bancos de Dados

```ini
[BANCOS_ACCESS]
# Banco de baixas (principal - onde importa retornos)
db_baixa = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb

# Banco de cobrança (opcional)
db_cobranca = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb

# Usar banco de cobrança? (true/false)
usar_cobranca = false
```

**Quando ajustar:**
- Novo banco de dados
- Mudar versão do banco (ex: dbBaixa2026.accdb)
- Ativar/desativar banco de cobrança
- Testar com banco local

**Nota:** `usar_cobranca = false` desativa o banco de cobrança mesmo que o caminho esteja configurado.

---

### `[PYTHON]` - Executável Python

```ini
[PYTHON]
# Caminho do executável Python (usado pelos scripts BAT)
executavel = C:\Users\charles.oliveira.AGENCIAPCJ\AppData\Local\Programs\Python\Python313\python.exe
```

**Quando ajustar:**
- Instalou Python em outro local
- Mudou de usuário Windows
- Instalou nova versão do Python
- Rodando em outra máquina

**Como descobrir seu caminho:**
```powershell
where.exe python
```

---

### `[LOGS]` - Configuração de Logs

```ini
[LOGS]
# Nome do arquivo de log
arquivo_log = monitor_retornos.log

# Nível de log (DEBUG, INFO, WARNING, ERROR)
nivel_log = INFO
```

**Níveis disponíveis:**
- `DEBUG` - Tudo (muito detalhado, para desenvolvimento)
- `INFO` - Normal (recomendado para produção)
- `WARNING` - Apenas avisos e erros
- `ERROR` - Apenas erros

**Quando ajustar:**
- `DEBUG` → Para investigar problemas
- `INFO` → Uso normal
- `WARNING` → Reduzir tamanho do log

---

### `[PROCESSAMENTO]` - Comportamento do Sistema

```ini
[PROCESSAMENTO]
# Tempo de espera (segundos) para garantir que arquivo foi copiado completamente
tempo_espera_arquivo = 1

# Fazer backup automático antes de processar? (true/false)
fazer_backup = true

# Excluir automaticamente arquivos IEDCBR? (true/false)
excluir_ied = true
```

**Opções:**

| Configuração | O que faz | Valores | Recomendado |
|--------------|-----------|---------|-------------|
| `tempo_espera_arquivo` | Aguarda antes de processar | 1 a 5 segundos | `1` |
| `fazer_backup` | Cria backup antes de processar | true/false | `true` |
| `excluir_ied` | Apaga arquivos IEDCBR | true/false | `true` |

**Quando ajustar:**
- `tempo_espera_arquivo = 2` → Se arquivos grandes estão sendo cortados
- `fazer_backup = false` → Para testes rápidos (não recomendado em produção!)
- `excluir_ied = false` → Se quiser manter arquivos IED para análise

---

## 🔧 EXEMPLOS DE USO

### Exemplo 1: Mudou de Servidor

**Antes:**
```ini
pasta_retorno = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno
db_baixa = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb
```

**Depois:**
```ini
pasta_retorno = \\SERVIDOR2\Cobranca\Retorno
db_baixa = \\SERVIDOR2\Cobranca\dbBaixa2025.accdb
```

✅ **Não precisa mexer em código Python!**

---

### Exemplo 2: Testar Localmente

**config.ini para testes locais:**
```ini
[CAMINHOS]
pasta_retorno = D:\Teste\Retorno
pasta_processados = D:\Teste\Retorno\Processados
pasta_erro = D:\Teste\Retorno\Erro
pasta_backup = D:\Teste\Backup

[BANCOS_ACCESS]
db_baixa = D:\Teste\dbBaixa2025.accdb
db_cobranca = D:\Teste\Cobranca2019.accdb
usar_cobranca = false

[PROCESSAMENTO]
fazer_backup = false   # Sem backup em testes
excluir_ied = false    # Mantém IED para análise
```

---

### Exemplo 3: Debug de Problemas

**Para investigar erros:**
```ini
[LOGS]
nivel_log = DEBUG   # Ativa logs detalhados

[PROCESSAMENTO]
tempo_espera_arquivo = 3   # Aguarda mais tempo
```

---

## ⚠️ IMPORTANTE

### ❌ NÃO FAÇA:
- Não use barras simples `\` - sempre use duplas `\\`
- Não apague seções inteiras
- Não use caracteres especiais nos valores

### ✅ FAÇA:
- Use `\\` para caminhos Windows: `\\SERVIDOR1\pasta`
- Mantenha backup do config.ini antes de alterar
- Teste alterações primeiro em modo DEBUG
- Documente mudanças (adicione comentários com `#`)

---

## 🧪 COMO TESTAR CONFIGURAÇÃO

### Teste 1: Validar config.ini
```powershell
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
python config_manager.py
```

Deve mostrar todas as configurações carregadas. Se der erro, há problema no config.ini.

### Teste 2: Teste rápido do monitor
```powershell
# Inicie e pare em 5 segundos
.\INICIAR_MONITOR.bat
# Aguarde 5 segundos
# Ctrl+C para parar

# Verifique o log
Get-Content monitor_retornos.log -Tail 20
```

Deve mostrar caminhos corretos no log.

---

## 🔄 MIGRAÇÃO ENTRE AMBIENTES

### De Desenvolvimento para Produção:

1. **Copie os arquivos Python** para a pasta de produção
2. **Copie o config.ini**
3. **Edite APENAS o config.ini** com caminhos de produção
4. **Teste:**
   ```powershell
   python config_manager.py
   ```
5. **Inicie o monitor**

### De uma Máquina para Outra:

1. Copie toda a pasta `AutomacaoRetorno`
2. Ajuste no `config.ini`:
   - `[PYTHON] executavel` → Caminho do Python na nova máquina
   - Se os caminhos de rede mudaram, ajuste `[CAMINHOS]`
3. Teste e rode

---

## 📝 TEMPLATE COMPLETO

```ini
[DIRETORIOS]
dir_trabalho = D:\Teste_Cobrança_Acess\AutomacaoRetorno
dir_producao = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno

[CAMINHOS]
pasta_retorno = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno
pasta_processados = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Processados
pasta_erro = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Erro
pasta_backup = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup

[BANCOS_ACCESS]
db_baixa = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb
db_cobranca = \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb
usar_cobranca = false

[PYTHON]
executavel = C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python313\python.exe

[LOGS]
arquivo_log = monitor_retornos.log
nivel_log = INFO

[PROCESSAMENTO]
tempo_espera_arquivo = 1
fazer_backup = true
excluir_ied = true

[NOTIFICACOES]
habilitado = true

[ONEDRIVE]
caminho_backup = F:\OneDrive - Fundacao Agencia das Bacias PCJ\Repositorio_TI\Manuais\SCPCJ\AutomaçãoDbBaixa

[EMAIL]
habilitado = false
smtp_servidor = smtp.gmail.com
smtp_porta = 587
remetente = seu_email@exemplo.com
senha = sua_senha_de_app_aqui
destinatarios = destinatario1@exemplo.com, destinatario2@exemplo.com
```

---

## 🆘 TROUBLESHOOTING

### Erro: "Arquivo de configuração não encontrado"
**Solução:** Certifique-se de que `config.ini` está em:
```
D:\Teste_Cobrança_Acess\AutomacaoRetorno\config.ini
```

### Erro: "Seções faltando no config.ini"
**Solução:** Compare seu config.ini com o template acima. Todas as seções `[NOME]` devem existir.

### Monitor não encontra pasta
**Solução:** Verifique os caminhos no config.ini:
```powershell
Test-Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno"
```

### Logs muito grandes
**Solução:** Mude `nivel_log` de `DEBUG` para `INFO` ou `WARNING`

---

**🎉 Com config.ini, manutenção é muito mais fácil!**

*Criado em: 09/10/2025*
