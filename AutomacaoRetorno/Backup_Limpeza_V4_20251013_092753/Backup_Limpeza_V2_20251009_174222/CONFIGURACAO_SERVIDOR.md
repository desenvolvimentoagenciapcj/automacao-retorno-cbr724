# ✅ CONFIGURAÇÃO: MONITORAMENTO REMOTO

**Data:** 09/10/2025
**Modo:** Monitor LOCAL → Servidor REMOTO

---

## 🎯 COMO FUNCIONA

### ✅ Arquivos Python e BAT ficam:
```
D:\Teste_Cobrança_Acess\AutomacaoRetorno\
```
**(Na sua máquina local)**

### ✅ Python roda:
```
Na sua máquina (localhost)
```

### ✅ Mas monitora e processa:
```
\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\
```
**(Tudo acontece no servidor via rede)**

---

## 📂 MAPEAMENTO DE PASTAS

| O QUE | ONDE ESTÁ |
|-------|-----------|
| **Scripts Python** | `D:\Teste_Cobrança_Acess\AutomacaoRetorno\` (local) |
| **Scripts BAT** | `D:\Teste_Cobrança_Acess\AutomacaoRetorno\` (local) |
| **Logs** | `D:\Teste_Cobrança_Acess\AutomacaoRetorno\monitor_retornos.log` (local) |
| | |
| **Pasta Monitorada** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\` |
| **Banco dbBaixa2025** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb` |
| **Banco Cobranca2019** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb` |
| **Pasta Backup** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup\` |
| **Processados** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Processados\` |
| **Erros** | `\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Erro\` |

---

## 🚀 COMO USAR

### 1. Iniciar Monitor (da sua máquina)
```powershell
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
.\INICIAR_MONITOR_OCULTO.bat
```

### 2. Verificar Status
```powershell
.\STATUS_MONITOR.bat
```

### 3. Ver Log Local
```powershell
Get-Content monitor_retornos.log -Tail 20
```

### 4. Parar Monitor
```powershell
.\PARAR_MONITOR.bat
```

---

## 📋 FLUXO DE PROCESSAMENTO

```
1. Alguém coloca arquivo .ret em:
   \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\

2. Monitor (rodando na sua máquina) detecta via watchdog

3. Python processa o arquivo:
   ✓ Lê o arquivo do servidor
   ✓ Faz backup no servidor
   ✓ Atualiza banco Access no servidor
   ✓ Move arquivo para Processados no servidor

4. Log fica na sua máquina:
   D:\Teste_Cobrança_Acess\AutomacaoRetorno\monitor_retornos.log
```

---

## ✅ VANTAGENS DESSA CONFIGURAÇÃO

1. **Controle Total da Sua Máquina**
   - Você inicia/para quando quiser
   - Logs ficam acessíveis localmente
   - Não precisa acessar servidor via Remote Desktop

2. **Processamento Centralizado**
   - Todos os arquivos ficam no servidor
   - Bancos Access no servidor (evita problemas de rede)
   - Backups no servidor

3. **Flexibilidade**
   - Pode executar de qualquer máquina com acesso ao servidor
   - Scripts BAT usam `%~dp0` (caminho relativo)
   - Fácil mover para outro local se necessário

4. **Segurança**
   - Apenas sua máquina acessa os bancos
   - Servidor recebe apenas arquivos processados
   - Log de tudo que acontece

---

## 🔧 AJUSTES FEITOS

### Em `monitor_retornos.py`:
```python
# Antes (local):
pasta_entrada = Path(r"D:\Teste_Cobrança_Acess\Retorno")

# Agora (servidor):
pasta_entrada = Path(r"\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno")
```

### Em `monitor_retornos.py` (config):
```python
config = {
    'bancos': {
        'baixa': {
            'caminho': r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb'
        },
        'cobranca': {
            'ativo': False,
            'caminho': r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Cobranca2019.accdb'
        }
    },
    'diretorios': {
        'backup': r'\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\backup'
    }
}
```

### Em TODOS os arquivos .bat:
```bat
# Antes:
cd /d "D:\Teste_Cobrança_Acess\AutomacaoRetorno"

# Agora (dinâmico):
cd /d "%~dp0"
```

O `%~dp0` significa "pasta onde está este BAT", então funciona em qualquer local!

---

## 🧪 TESTE RÁPIDO

```powershell
# 1. Acesse a pasta local
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"

# 2. Inicie em modo visível (para ver o que acontece)
.\INICIAR_MONITOR.bat

# 3. Em outra janela, copie um arquivo de teste para o servidor:
Copy-Item "D:\algum_arquivo_teste.ret" -Destination "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\"

# 4. Observe o processamento no monitor

# 5. Verifique o resultado no servidor:
Get-ChildItem "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno\Processados"
```

---

## ⚠️ REQUISITOS

- ✅ Acesso de rede ao servidor: `\\SERVIDOR1\CobrancaPCJ\`
- ✅ Permissão de leitura/escrita nas pastas do servidor
- ✅ Driver ODBC Access instalado na sua máquina
- ✅ Python 3.13 com pacotes: `watchdog`, `pyodbc`
- ✅ Sua máquina precisa estar ligada para monitor funcionar

---

## 📞 TROUBLESHOOTING

### Monitor não detecta arquivos?
```powershell
# Teste se consegue acessar o servidor:
Test-Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno"

# Deve retornar: True
```

### Erro de acesso ao banco?
```powershell
# Verifique permissões:
Test-Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\dbBaixa2025.accdb"

# Tente abrir manualmente o Access
```

### Monitor não inicia?
```powershell
# Veja o erro no log:
Get-Content "D:\Teste_Cobrança_Acess\AutomacaoRetorno\monitor_retornos.log" -Tail 50
```

---

**🎉 Sistema configurado para monitoramento remoto!**

*Atualizado em: 09/10/2025*
