# 🕐 Agendador de Verificação Automática

## 📋 O que é?

Um sistema que **verifica automaticamente** se o monitor está rodando em horários programados.

**Por padrão:** Segunda a Sexta às **8h da manhã**

## 🎯 Para que serve?

**Problema:** O monitor pode cair (erro, Windows reiniciar, etc.) e você não perceber.

**Solução:** O agendador verifica periodicamente se o monitor está ativo:
- ✅ Se estiver rodando → Tudo OK, não faz nada
- ❌ Se NÃO estiver rodando → **Reinicia automaticamente** e notifica você

---

## 🚀 Como Usar

### Opção 1: Executar Manualmente (quando precisar)

Na raiz do projeto, execute:
```
AGENDADOR.bat
```

Ou:
```
scripts\bat\INICIAR_AGENDADOR.bat
```

O agendador ficará rodando e verificará nos horários programados.

### Opção 2: Iniciar com o Windows (RECOMENDADO para produção)

Veja seção "Iniciar Automaticamente com Windows" abaixo.

---

## ⚙️ Configuração

Edite: `config/config.ini`

```ini
[VERIFICACAO_AGENDADA]
# Habilitar verificação agendada?
habilitado = true

# Horário da verificação (formato 24h)
horario = 08:00

# Dias da semana
dias_semana = segunda,terca,quarta,quinta,sexta
```

### Exemplos de Configuração:

**1. Verificar todos os dias às 8h:**
```ini
horario = 08:00
dias_semana = segunda,terca,quarta,quinta,sexta,sabado,domingo
```

**2. Verificar 2x por dia (requer múltiplos agendadores):**
```ini
horario = 08:00
dias_semana = segunda,terca,quarta,quinta,sexta
```
E iniciar outro agendador configurado para 14:00.

**3. Desabilitar temporariamente:**
```ini
habilitado = false
```

---

## 🔍 Como Funciona

### Fluxo de Verificação:

```
⏰ Horário programado chega (ex: 8h)
    ↓
🔍 Verifica: monitor está rodando?
    ↓
✅ SIM - Monitor ativo
    ├─→ Log: "Monitor está ativo - PID: xxxx"
    └─→ Não faz nada
    
❌ NÃO - Monitor caído
    ├─→ 📢 Notificação Windows: "Monitor caiu, reiniciando..."
    ├─→ 🔄 Tenta reiniciar automaticamente
    ├─→ ⏳ Aguarda 3 segundos
    └─→ Verifica novamente:
         ├─→ ✅ Sucesso: Notifica "Reiniciado com sucesso"
         └─→ ❌ Falha: Notifica ERRO CRÍTICO por Windows + E-mail
```

---

## 🧪 Testar a Verificação

### Teste Imediato (sem esperar horário agendado):

Execute:
```
scripts\bat\TESTAR_VERIFICACAO.bat
```

Ou:
```powershell
python scripts\python\agendador_verificacao.py --testar
```

**O que acontece:**
- Executa verificação imediatamente
- Mostra status do monitor
- Se caído, tenta reiniciar

---

## 📝 Comandos Disponíveis

### Iniciar Agendador:
```
AGENDADOR.bat
```
ou
```
scripts\bat\INICIAR_AGENDADOR.bat
```

### Parar Agendador:
```
scripts\bat\PARAR_AGENDADOR.bat
```

### Testar Verificação:
```
scripts\bat\TESTAR_VERIFICACAO.bat
```

---

## 🔄 Iniciar Automaticamente com Windows

### Método 1: Agendador de Tarefas do Windows (RECOMENDADO)

1. **Abra o Agendador de Tarefas:**
   - Pressione `Win + R`
   - Digite: `taskschd.msc`
   - Enter

2. **Criar Nova Tarefa:**
   - Clique em "Criar Tarefa Básica..."
   - Nome: `Monitor - Agendador Verificação`
   - Descrição: `Verifica se monitor de retornos está ativo`

3. **Disparador:**
   - Quando: `Quando o computador iniciar`
   - Adiar tarefa por: `1 minuto`

4. **Ação:**
   - Ação: `Iniciar um programa`
   - Programa: `D:\Teste_Cobrança_Acess\AutomacaoRetorno\AGENDADOR.bat`

5. **Configurações Avançadas:**
   - ✅ Executar independente de o usuário estar conectado
   - ✅ Executar com privilégios mais altos
   - ✅ Se a tarefa já estiver em execução, não iniciar nova instância

6. **Salvar e Testar:**
   - Clique com botão direito na tarefa
   - "Executar"
   - Verifique se iniciou

### Método 2: Pasta de Inicialização

1. **Abra a pasta de inicialização:**
   - Pressione `Win + R`
   - Digite: `shell:startup`
   - Enter

2. **Crie um atalho:**
   - Botão direito → Novo → Atalho
   - Local: `D:\Teste_Cobrança_Acess\AutomacaoRetorno\AGENDADOR.bat`
   - Nome: `Agendador Verificação Monitor`

3. **Reinicie o PC para testar**

---

## 📊 Logs

Os logs são salvos em: `logs/agendador.log`

### Exemplo de log normal:

```
2025-10-13 08:00:00 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 13/10/2025 às 08:00:00
2025-10-13 08:00:01 - INFO - ✅ Monitor está ativo - PID: 12345
```

### Exemplo de log com reinício:

```
2025-10-13 08:00:00 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 13/10/2025 às 08:00:00
2025-10-13 08:00:01 - WARNING - ⚠️  MONITOR NÃO ESTÁ RODANDO!
2025-10-13 08:00:01 - INFO - 🔄 Tentando reiniciar automaticamente...
2025-10-13 08:00:01 - INFO - 🚀 Iniciando monitor automaticamente...
2025-10-13 08:00:05 - INFO - ✅ Monitor reiniciado com sucesso! PID: 67890
```

### Exemplo de log com falha:

```
2025-10-13 08:00:00 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 13/10/2025 às 08:00:00
2025-10-13 08:00:01 - WARNING - ⚠️  MONITOR NÃO ESTÁ RODANDO!
2025-10-13 08:00:01 - INFO - 🔄 Tentando reiniciar automaticamente...
2025-10-13 08:00:01 - ERROR - ❌ FALHA ao reiniciar monitor!
2025-10-13 08:00:01 - ERROR - ⚠️  AÇÃO MANUAL NECESSÁRIA!
```

---

## 📧 Notificações

### Notificações do Windows:

1. **Monitor Ativo (não notifica)** - Só loga
2. **Monitor Caído:**
   - 🔸 "Monitor Caiu - Tentando reiniciar..."
3. **Reinício Sucesso:**
   - 🔹 "Monitor Reiniciado - Monitor reiniciado com sucesso!"
4. **Reinício Falhou:**
   - 🔴 "CRÍTICO: Falha ao Reiniciar - Ação manual necessária!"

### E-mails:

Apenas em caso de **FALHA CRÍTICA** (não conseguiu reiniciar):
- Assunto: `❌ ERRO - MONITOR CAIU`
- Conteúdo: Detalhes do erro + orientação para ação manual

---

## ❓ Perguntas Frequentes

### P: O agendador precisa ficar rodando sempre?

**R:** Sim. Ele roda em background e só age nos horários programados. Consome pouquíssimos recursos.

### P: Posso ter múltiplas verificações por dia?

**R:** Sim! Você pode:
1. Iniciar múltiplas instâncias com horários diferentes
2. Ou usar Agendador de Tarefas do Windows com múltiplos disparadores

### P: O agendador reinicia o computador?

**R:** Não! Ele só reinicia o **monitor** (processo Python), nunca o Windows.

### P: E se o Windows reiniciar?

**R:** Se configurou para iniciar com Windows (Método 1 ou 2 acima), o agendador inicia automaticamente após reiniciar.

### P: O agendador consome muita memória?

**R:** Não. Usa ~10-20 MB de RAM e 0% de CPU (fica dormindo até horário programado).

### P: Posso desabilitar sem desinstalar?

**R:** Sim! No `config.ini`:
```ini
[VERIFICACAO_AGENDADA]
habilitado = false
```

### P: Como sei se o agendador está rodando?

**R:** Execute:
```
scripts\bat\STATUS_MONITOR.bat
```

Ou verifique o Gerenciador de Tarefas:
- Processos Python rodando `agendador_verificacao.py`

---

## 🎯 Cenários de Uso

### Cenário 1: Uso Normal Diário

**Setup:**
```ini
habilitado = true
horario = 08:00
dias_semana = segunda,terca,quarta,quinta,sexta
```

**Comportamento:**
- Todo dia útil às 8h verifica
- Se monitor caiu durante a noite, reinicia automaticamente
- Você chega no trabalho com tudo funcionando

### Cenário 2: Monitoramento 24/7

**Setup:**
```ini
habilitado = true
horario = 08:00  # Criar múltiplas instâncias para vários horários
dias_semana = segunda,terca,quarta,quinta,sexta,sabado,domingo
```

**Comportamento:**
- Verifica todos os dias (inclusive fim de semana)
- Garante disponibilidade contínua

### Cenário 3: Apenas Verificação (sem reinício automático)

**Não é possível nativamente**, mas você pode:
1. Desabilitar notificações de e-mail
2. Só ver os logs
3. Receber notificação Windows mas agir manualmente

---

## ✅ Checklist de Implementação

- [x] Script `agendador_verificacao.py` criado
- [x] Configuração `[VERIFICACAO_AGENDADA]` adicionada ao config.ini
- [x] Scripts BAT criados (INICIAR, PARAR, TESTAR)
- [x] Atalho raiz `AGENDADOR.bat` criado
- [x] Biblioteca `schedule` instalada
- [x] Notificações Windows integradas
- [x] Notificações E-mail integradas
- [x] Logs implementados
- [x] Documentação completa

---

## 🚀 Quick Start

**1. Testar agora:**
```
scripts\bat\TESTAR_VERIFICACAO.bat
```

**2. Iniciar agendador:**
```
AGENDADOR.bat
```

**3. Configurar iniciar com Windows:**
- Seguir "Método 1: Agendador de Tarefas do Windows"

**Pronto!** O sistema agora se auto-monitora! 🎉

---

**Data:** 13/10/2025  
**Sistema:** Automação de Retornos CBR724  
**Agência das Bacias PCJ**
