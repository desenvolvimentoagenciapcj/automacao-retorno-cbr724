# 🚀 PLANO DE IMPLANTAÇÃO - PRODUÇÃO

**Servidor:** \\\\SERVIDOR1\\CobrancaPCJ\\CobrancaPCJ  
**Data:** 09/10/2025

---

## 📋 CHECKLIST PRÉ-IMPLANTAÇÃO

- [x] ✅ Acesso ao servidor verificado
- [x] ✅ Bancos Access localizados:
  - Cobranca2019.accdb (48.16 MB)
  - dbBaixa2025.accdb (53.47 MB)
- [x] ✅ Pasta Retorno existe
- [x] ✅ Pasta backup existe
- [ ] ⏳ Criar pasta AutomacaoRetorno
- [ ] ⏳ Copiar arquivos Python
- [ ] ⏳ Copiar scripts BAT
- [ ] ⏳ Criar pastas necessárias
- [ ] ⏳ Ajustar caminhos nos scripts
- [ ] ⏳ Testar em produção

---

## 📂 ESTRUTURA A SER CRIADA

```
\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\
├── Retorno\                       ← JÁ EXISTE
│   ├── Processados\               ← CRIAR
│   ├── Erro\                      ← CRIAR
│   └── ied\                       ← VERIFICAR/CRIAR
├── backup\                        ← JÁ EXISTE
├── AutomacaoRetorno\              ← CRIAR (nova pasta)
│   ├── monitor_retornos.py
│   ├── integrador_access.py
│   ├── processador_cbr724.py
│   ├── INICIAR_MONITOR.bat
│   ├── INICIAR_MONITOR_OCULTO.bat
│   ├── INICIAR_MONITOR_MINIMIZADO.bat
│   ├── STATUS_MONITOR.bat
│   ├── PARAR_MONITOR.bat
│   ├── _run_hidden.vbs
│   ├── _start_monitor.bat
│   ├── _check_monitor.ps1
│   ├── COMO_USAR.md
│   └── APROVADO.md
├── Cobranca2019.accdb             ← JÁ EXISTE
└── dbBaixa2025.accdb              ← JÁ EXISTE
```

---

## 🔧 AJUSTES NECESSÁRIOS

### 1. Caminhos nos Scripts Python

**Arquivos a ajustar:**
- `monitor_retornos.py` (linhas ~35-40)
- `integrador_access.py` (linhas ~35-42)

**DE (desenvolvimento):**
```python
PASTA_RETORNO = r"D:\Teste_Cobrança_Acess\Retorno"
DB_BAIXA = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"
DB_COBRANCA = r"D:\Teste_Cobrança_Acess\Cobranca2019.accdb"
PASTA_BACKUP = r"D:\Teste_Cobrança_Acess\Backup"
```

**PARA (produção):**
```python
PASTA_RETORNO = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno"
DB_BAIXA = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb"
DB_COBRANCA = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb"
PASTA_BACKUP = r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup"
```

### 2. Arquivo _start_monitor.bat

**DE:**
```bat
cd /d "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
```

**PARA:**
```bat
cd /d "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno"
```

### 3. Scripts BAT de Controle

Todos os scripts que usam `cd /d` precisam ser ajustados:
- INICIAR_MONITOR_OCULTO.bat
- INICIAR_MONITOR_MINIMIZADO.bat
- STATUS_MONITOR.bat
- PARAR_MONITOR.bat

---

## 📝 PASSOS DE IMPLANTAÇÃO

### Passo 1: Criar Estrutura de Pastas
```powershell
New-Item -ItemType Directory -Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno" -Force
New-Item -ItemType Directory -Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Processados" -Force
New-Item -ItemType Directory -Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Erro" -Force
```

### Passo 2: Copiar Arquivos Python (com ajustes)
- Criar versões ajustadas dos arquivos .py
- Copiar para \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno

### Passo 3: Copiar Scripts BAT (com ajustes)
- Criar versões ajustadas dos .bat
- Copiar para \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno

### Passo 4: Copiar Arquivos Auxiliares
- _run_hidden.vbs
- _start_monitor.bat (ajustado)
- _check_monitor.ps1
- Documentação (COMO_USAR.md, APROVADO.md)

### Passo 5: Testar
- Executar INICIAR_MONITOR.bat (modo visível)
- Copiar arquivo de teste
- Verificar processamento
- Testar STATUS e PARAR

### Passo 6: Produção
- Executar INICIAR_MONITOR_OCULTO.bat
- Verificar STATUS
- Monitorar logs

---

## ⚠️ CONSIDERAÇÕES IMPORTANTES

### 1. Permissões
- ✅ Verificar permissões de leitura/escrita no servidor
- ✅ Garantir acesso aos bancos Access
- ✅ Verificar se Python está instalado no servidor

### 2. Python no Servidor
- Verificar se Python está instalado
- Se não, instalar ou usar Python portable
- Ajustar caminho do Python no _start_monitor.bat

### 3. Backup
- Sistema já faz backup automático
- Mas fazer backup manual dos bancos antes da primeira execução

### 4. Testes
- **CRÍTICO:** Testar primeiro em modo visível
- Verificar logs detalhadamente
- Só depois usar modo oculto

---

## 🎯 COMANDOS RÁPIDOS

### Criar estrutura:
```powershell
# Criar pastas
$base = "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ"
New-Item -ItemType Directory -Path "$base\AutomacaoRetorno" -Force
New-Item -ItemType Directory -Path "$base\Retorno\Processados" -Force
New-Item -ItemType Directory -Path "$base\Retorno\Erro" -Force
```

### Copiar arquivos:
```powershell
# Copiar sistema completo (após ajustes)
Copy-Item "D:\Teste_Cobrança_Acess\AutomacaoRetorno\*" `
  -Destination "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\AutomacaoRetorno" `
  -Recurse -Force
```

---

## 📊 VALIDAÇÃO PÓS-IMPLANTAÇÃO

- [ ] Monitor inicia sem erros
- [ ] Detecta arquivo .ret automaticamente
- [ ] Processa corretamente
- [ ] Cria backup
- [ ] Move arquivo para Processados
- [ ] Adiciona sufixo "-processado"
- [ ] STATUS detecta monitor
- [ ] PARAR funciona corretamente
- [ ] Logs são gerados corretamente

---

## 🔄 ROLLBACK (se necessário)

1. Parar monitor: `PARAR_MONITOR.bat`
2. Restaurar backup dos bancos (se necessário)
3. Remover pasta AutomacaoRetorno
4. Processo manual volta ao normal

---

**Próximo passo:** Criar versões ajustadas dos arquivos para produção
