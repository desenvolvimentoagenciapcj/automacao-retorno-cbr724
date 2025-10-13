# 🤖 Monitor Automático de Retornos Bancários CBR724

## ✅ Sistema Totalmente Funcional e Testado

Este sistema processa automaticamente arquivos de retorno bancário CBR724, integrando com Microsoft Access.

---

## 📋 Funcionalidades

✅ **Monitoramento automático** da pasta `D:\Teste_Cobrança_Acess\Retorno`  
✅ **Processamento CBR724** - Lê arquivo, extrai data correta, processa registros  
✅ **Integração Access** - Atualiza banco `dbBaixa2025.accdb` automaticamente  
✅ **Backup automático** - Cria backup antes de qualquer alteração  
✅ **Arquivos IED** - Apaga automaticamente arquivos IEDCBR*  
✅ **Sufixo "-processado"** - Renomeia arquivos após processar  
✅ **3 modos de execução** - Visível, Minimizado ou Oculto  
✅ **Logs detalhados** - Registro completo em `monitor_retornos.log`  

---

## 🚀 Como Usar

### **Opção 1: Modo Oculto (Recomendado para produção)**

```batch
INICIAR_MONITOR_OCULTO.bat
```

- Monitor roda **totalmente invisível** em segundo plano
- Não aparece nenhuma janela
- Ideal para rodar 24/7

### **Opção 2: Modo Minimizado**

```batch
INICIAR_MONITOR_MINIMIZADO.bat
```

- Janela minimizada na barra de tarefas
- Clique para expandir e ver o progresso
- Bom para debug

### **Opção 3: Modo Interativo (Escolhe ao iniciar)**

```batch
INICIAR_MONITOR.bat
```

- Pergunta qual modo você prefere (1=Visível, 2=Minimizado, 3=Oculto)
- Flexível para diferentes situações

---

## 📊 Verificar Status

```batch
STATUS_MONITOR.bat
```

**Mostra:**
- ✅ STATUS: RODANDO ou ⭕ PARADO
- 🆔 PID do processo (se rodando)
- 📝 Última atividade registrada
- 📊 Últimos arquivos processados

---

## 🛑 Parar o Monitor

```batch
PARAR_MONITOR.bat
```

- Pede confirmação antes de parar
- Encerra o processo graciosamente
- Mostra mensagem de sucesso

---

## 📁 Estrutura de Pastas

```
D:\Teste_Cobrança_Acess\
├── Retorno\                    ← Coloque arquivos .ret aqui
│   ├── Processados\            ← Arquivos processados com sucesso
│   └── Erro\                   ← Arquivos com erro
├── Backup\                     ← Backups automáticos dos bancos
└── AutomacaoRetorno\
    ├── monitor_retornos.py     ← Monitor principal
    ├── integrador_access.py    ← Integração com Access
    ├── processador_cbr724.py   ← Processador de arquivos
    ├── INICIAR_*.bat           ← Scripts de inicialização
    ├── STATUS_MONITOR.bat      ← Verificar status
    ├── PARAR_MONITOR.bat       ← Parar monitor
    └── monitor_retornos.log    ← Log de atividades
```

---

## 🔧 Funcionamento

1. **Monitor detecta** arquivo .ret na pasta Retorno
2. **Identifica tipo:**
   - `IEDCBR*` → Apaga automaticamente
   - `CBR724*` → Processa normalmente
3. **Cria backup** dos bancos Access
4. **Extrai data** do arquivo (linha 28, posições 115-122)
5. **Processa registros:**
   - Tipo 01: Liquidação (LQ) - Baixa título
   - Tipo 02: Baixa manual (BX) - Baixa título
   - Tipo 06: Cancelamento (CC) - Cancela título
6. **Executa queries** de atualização (Alexandre Passos 1, 2 e 3)
7. **Move arquivo** para Processados com sufixo "-processado"
8. **Aguarda próximo** arquivo...

---

## 📝 Logs

**Localização:** `monitor_retornos.log`

**Conteúdo:**
- Data/hora de cada operação
- Arquivos detectados
- Títulos processados (número, valor, juros, data)
- Baixas, cancelamentos, criações
- Erros (se houver)
- Resultado final (estatísticas)

**Exemplo:**
```
2025-10-09 09:50:57 - INFO - 📄 Novo arquivo detectado: CBR724_TESTE.ret
2025-10-09 09:50:57 - INFO - ✓ Título PAGO: 2500004810 - Valor: R$ 847.48
2025-10-09 09:50:59 - INFO - ✅ Processamento concluído com sucesso!
2025-10-09 09:50:59 - INFO -    • Processados: 4
2025-10-09 09:50:59 - INFO -    • Baixas: 3
```

---

## ⚙️ Configuração Avançada

### Alterar Pasta Monitorada

Edite `monitor_retornos.py` linha ~35:

```python
PASTA_RETORNO = r"D:\Teste_Cobrança_Acess\Retorno"
```

### Alterar Bancos Access

Edite `integrador_access.py` linhas ~35-39:

```python
DB_BAIXA = r"D:\Teste_Cobrança_Acess\dbBaixa2025.accdb"
DB_COBRANCA = r"D:\Teste_Cobrança_Acess\Cobranca2019.accdb"
```

---

## 🐛 Solução de Problemas

### Monitor não inicia

1. Verifique se Python está instalado: `python --version`
2. Instale dependências: `pip install watchdog pywin32`
3. Tente modo visível primeiro: `INICIAR_MONITOR.bat` → opção 1

### Monitor não detecta arquivos

1. Verifique o log: `monitor_retornos.log`
2. Confirme que a pasta existe: `D:\Teste_Cobrança_Acess\Retorno`
3. Verifique STATUS: `STATUS_MONITOR.bat`

### Erro ao processar arquivo

1. Verifique o log para detalhes do erro
2. Arquivo vai para pasta `Retorno\Erro`
3. Verifique se bancos Access estão acessíveis
4. Confirme que Access não está aberto bloqueando os bancos

### STATUS mostra PARADO mas está rodando

- Execute `PARAR_MONITOR.bat` e reinicie
- Ou mate o processo Python manualmente

---

## 📦 Repositório GitHub

🔒 **Repositório Privado:** `Cha-Oliveira/automacao-retorno-cbr724`

**Commits recentes:**
- `fbc7697` - FIX: PARAR_MONITOR.bat detecta processo corretamente
- `cbc01f7` - FIX: Modo oculto funcionando com VBScript
- `a96bd7d` - FIX: Caminhos absolutos para modo minimizado
- `ad30a34` - FIX: 3 problemas (IED, backup, sufixo)

---

## 📞 Suporte

- Verifique os logs em `monitor_retornos.log`
- Todos os commits estão no GitHub
- Sistema testado e aprovado ✅

---

## ⚡ Início Rápido

```batch
# 1. Iniciar monitor em segundo plano
INICIAR_MONITOR_OCULTO.bat

# 2. Verificar se está rodando
STATUS_MONITOR.bat

# 3. Copiar arquivo .ret para D:\Teste_Cobrança_Acess\Retorno

# 4. Ver log (opcional)
notepad monitor_retornos.log

# 5. Parar quando necessário
PARAR_MONITOR.bat
```

🎉 **Sistema 100% funcional e testado!**
