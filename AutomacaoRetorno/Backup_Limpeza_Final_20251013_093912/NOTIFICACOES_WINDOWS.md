# 🔔 Notificações do Windows - Guia Rápido

> **Sistema:** Automação de Retornos CBR724  
> **Versão:** 1.0 - Notificações Nativas do Windows

---

## 📌 O Que São as Notificações?

Notificações **visuais** que aparecem no canto da tela do Windows (como as do Outlook, Teams, etc).

**Exemplo:**
```
┌─────────────────────────────────┐
│ ✅ Monitor Iniciado             │
│                                 │
│ Monitorando:                    │
│ \\SERVIDOR1\...\Retorno         │
└─────────────────────────────────┘
```

---

## ✅ Vantagens

- 🚀 **Zero configuração** - Sem senhas, sem contas
- 👀 **Visual e imediato** - Aparece na hora
- 🔊 **Som de alerta** - Chama atenção
- 💻 **Funciona offline** - Não precisa de internet
- 🎨 **Colorido** - Fácil de identificar o tipo

---

## 📦 Instalação

### **Passo 1: Instalar a Biblioteca**

Abra o PowerShell na pasta do projeto e execute:

```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
pip install plyer
```

**OU** instale todas as dependências:

```powershell
pip install -r requirements.txt
```

### **Passo 2: Testar**

```powershell
python notificador_windows.py
```

Se aparecer uma notificação no canto da tela, está funcionando! ✅

---

## 🔔 Tipos de Notificações

### 1. 🟢 **Monitor Iniciado**
```
ℹ️ Monitor Iniciado

Monitorando:
\\SERVIDOR1\CobrancaPCJ\...\Retorno
```

### 2. 📄 **Novo Arquivo Detectado**
```
ℹ️ Novo Arquivo Detectado

Processando:
CBR724001.ret
```

### 3. ✅ **Processamento Sucesso**
```
✅ Arquivo Processado

Arquivo: CBR724001.ret
✅ Criados: 45
💰 Pagos: 23
❌ Cancelados: 2
```

### 4. ❌ **Erro no Processamento**
```
❌ Erro no Processamento

Arquivo: CBR724002.ret
Erro: Banco de dados inacessível
```

### 5. 🗑️ **IEDCBR Excluído**
```
⚠️ IEDCBR Excluído

Arquivo IEDCBR excluído:
IEDCBR739310202514856.ret
```

### 6. 🔴 **Monitor Caiu (Watchdog)**
```
❌ ALERTA: Monitor Caiu

O monitor parou de funcionar!
Tentando reiniciar automaticamente...
```

### 7. ✅ **Monitor Reiniciado**
```
✅ Monitor Reiniciado

Monitor reiniciado com sucesso!
PID: 12345
```

---

## ⚙️ Configuração (Opcional)

No arquivo `config.ini`:

```ini
[NOTIFICACOES]
# Exibir notificações do Windows? (true/false)
habilitado = true
```

**Para desativar:**
```ini
habilitado = false
```

O sistema continuará funcionando normalmente, mas sem notificações.

---

## 🧪 Como Testar

### **Teste 1: Notificação Básica**
```powershell
python notificador_windows.py
```
✅ Deve aparecer uma notificação de teste

### **Teste 2: Com o Monitor Rodando**

1. Inicie o monitor:
   ```cmd
   INICIAR_MONITOR_OCULTO.bat
   ```

2. Copie um arquivo CBR para a pasta monitorada

3. Você verá notificações para:
   - 📄 Arquivo detectado
   - ✅ Processamento concluído

### **Teste 3: Arquivo IEDCBR**

1. Copie um arquivo IEDCBR para a pasta monitorada

2. Você verá:
   - 🗑️ Notificação de exclusão

---

## 📊 Exemplo de Uso Real

**Cenário:** Você está trabalhando em outra coisa, mas quer saber quando arquivos são processados.

**Resultado:**
1. Arquivo chega no servidor às 14:30
2. 🔔 Notificação aparece: "Novo Arquivo Detectado"
3. Sistema processa automaticamente
4. 🔔 Notificação aparece: "Arquivo Processado - 45 títulos criados"

**Você nem precisou abrir o sistema!** 🎉

---

## 🛠️ Solução de Problemas

### ❌ Erro: "módulo 'plyer' não encontrado"

**Solução:**
```powershell
pip install plyer
```

---

### ❌ Notificações não aparecem

**Verificar:**

1. **Biblioteca instalada?**
   ```powershell
   pip list | Select-String plyer
   ```

2. **Notificações habilitadas no Windows?**
   - Abra: Configurações → Sistema → Notificações
   - Verifique se notificações estão ativas

3. **Focus Assist ativo?**
   - Se estiver no modo "Concentrar-se", notificações podem estar silenciadas
   - Desative temporariamente para testar

---

### ℹ️ Notificações aparecem mas desaparecem rápido

Isso é normal! As notificações ficam visíveis por alguns segundos e depois vão para a Central de Ações.

**Para ver notificações antigas:**
- Clique no ícone de notificações no canto inferior direito
- Todas as notificações ficam salvas lá

---

## 💡 Dicas

### **1. Não Incomoda**
- Notificações aparecem e somem automaticamente
- Não interrompem seu trabalho
- Som discreto

### **2. Histórico**
- Todas ficam salvas na Central de Ações do Windows
- Você pode revisar depois

### **3. Foco no que Importa**
- Recebe alerta só quando algo acontece
- Não precisa ficar verificando logs

### **4. Combinação com Logs**
- Notificações = Alerta rápido
- Logs = Detalhes completos

---

## 🎯 Checklist de Implementação

- [x] Biblioteca `plyer` instalada
- [x] `notificador_windows.py` criado
- [x] `config.ini` atualizado com seção `[NOTIFICACOES]`
- [x] Monitor integrado com notificações
- [x] Watchdog integrado com notificações
- [ ] Testar notificação básica
- [ ] Testar com arquivo real
- [ ] Verificar se notificações aparecem

---

## 📚 Arquivos Relacionados

- **notificador_windows.py** - Sistema de notificações
- **monitor_retornos.py** - Monitor (integrado com notificações)
- **watchdog_monitor.py** - Watchdog (integrado com notificações)
- **config.ini** - Seção `[NOTIFICACOES]`
- **requirements.txt** - Biblioteca `plyer`

---

## 🚀 Comparação: E-mail vs Windows

| Recurso | E-mail | Windows |
|---------|--------|---------|
| Configuração | 😓 Complexa (senha de app) | ✅ Zero |
| Velocidade | ⏱️ Alguns segundos | ⚡ Instantâneo |
| Precisa internet | ✅ Sim | ❌ Não |
| Recebe fora do PC | ✅ Sim (celular) | ❌ Não |
| Visual | 📧 E-mail | 🔔 Notificação |
| Histórico | ✅ Inbox completo | ⏱️ Central de Ações |

**Conclusão:** Notificações do Windows são **muito mais fáceis** para uso local! 🎉

---

## ✨ Próximos Passos

1. ✅ Instale: `pip install plyer`
2. ✅ Teste: `python notificador_windows.py`
3. ✅ Inicie o monitor e veja as notificações aparecerem!

---

**Sistema funcionando + Notificações ativas = Você sempre informado! 🚀**
