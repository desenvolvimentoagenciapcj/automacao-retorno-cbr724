# 🎯 Verificação Inteligente - Agendador 8h30

## 📋 O Que É?

O agendador agora possui **verificação inteligente** que:
- Verifica servidor + monitor às **8h30** (segunda a sexta)
- Tenta recuperar automaticamente a cada **5 minutos** até **9h**
- Notifica por email se não conseguir até **9h**

---

## ⏰ Como Funciona (Timeline)

### 8h30 - Primeira Verificação
```
┌─────────────────────────────────────────────────────────────┐
│  VERIFICAÇÃO INICIAL                                         │
│                                                              │
│  ✓ Servidor está acessível?                                 │
│  ✓ Monitor está rodando?                                    │
└─────────────────────────────────────────────────────────────┘
```

**Cenário 1: Tudo OK ✅**
```
8h30 → Verifica → Servidor OK + Monitor OK
     → Log: "✅ Sistema OK - Monitor ativo e Servidor acessível"
     → Fim da verificação
     → Aguarda próximo dia útil
```

**Cenário 2: Problema Detectado ⚠️**
```
8h30 → Verifica → ⚠️ Servidor inacessível OU Monitor parado
     → Inicia processo de recuperação
     → Notificação Windows: "Sistema tentará recuperar a cada 5 min até 9h"
     → Agenda próxima tentativa: 8h35
```

---

### 8h30 - 9h00 - Tentativas de Recuperação (a cada 5 min)

```
┌─────────────────────────────────────────────────────────────┐
│  MODO RECUPERAÇÃO                                            │
│                                                              │
│  8h30 → Tentativa 1/6                                        │
│  8h35 → Tentativa 2/6                                        │
│  8h40 → Tentativa 3/6                                        │
│  8h45 → Tentativa 4/6                                        │
│  8h50 → Tentativa 5/6                                        │
│  8h55 → Tentativa 6/6                                        │
│  9h00 → Limite atingido                                      │
└─────────────────────────────────────────────────────────────┘
```

**A cada tentativa:**
1. Verifica servidor novamente
2. Tenta iniciar monitor (se servidor OK)
3. Se conseguir: ✅ Envia email de sucesso
4. Se falhar: Agenda próxima tentativa (+5 min)

---

### 9h00 - Resultado Final

**Se recuperou antes das 9h: ✅**
```
8h45 → Tentativa 4/6 → ✅ RECUPERADO!
     → Email: "✅ Sistema Recuperado com Sucesso"
     → Conteúdo:
        • Horário da recuperação: 8h45
        • Tentativas até recuperar: 4
        • Status: Monitor ativo + Servidor OK
     → Fim do processo de recuperação
```

**Se NÃO recuperou até 9h: 🚨**
```
9h00 → Esgotadas 6 tentativas → 🚨 FALHA CRÍTICA
     → Email: "🚨 FALHA CRÍTICA - [Servidor/Monitor] às 9h"
     → Conteúdo:
        • Problema detectado: Servidor inacessível OU Monitor não iniciou
        • Tentativas realizadas: 6
        • Horário limite: 9h00
        • Ações manuais necessárias (passo a passo)
     → Notificação Windows crítica
     → Log com destaque de erro
```

---

## 📧 Emails Enviados

### 1. Durante Recuperação (8h30-9h)

Você **NÃO** recebe emails a cada tentativa (para não encher caixa de entrada).

**Exceção:** Se recuperar com sucesso antes das 9h, recebe 1 email de confirmação.

### 2. Email de Sucesso (se recuperar antes 9h)
```
Assunto: ✅ Sistema Recuperado com Sucesso

Corpo:
Sistema voltou ao normal!

⏰ Horário: 8h45:32
🔄 Tentativas até recuperar: 4

✅ Monitor: Ativo (PID 12345)
✅ Servidor: Acessível

Sistema processando retornos normalmente.
```

### 3. Email de Falha Crítica (se não recuperar até 9h)

**Se problema for SERVIDOR:**
```
Assunto: 🚨 FALHA CRÍTICA - Servidor Inacessível às 9h

Corpo:
ATENÇÃO: Servidor continua inacessível!

⏰ Horário Limite: 9h00
🔄 Tentativas Realizadas: 6
📁 Servidor: \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno

❌ STATUS: Servidor NÃO está acessível

⚠️ AÇÃO URGENTE NECESSÁRIA:
1. Verificar se servidor \\SERVIDOR1 está ligado
2. Verificar conexão de rede
3. Testar acesso manual à pasta
4. Após correção, executar: .\PROCESSAR.bat

Arquivos de retorno NÃO estão sendo processados!
```

**Se problema for MONITOR:**
```
Assunto: 🚨 FALHA CRÍTICA - Monitor Não Iniciou às 9h

Corpo:
ATENÇÃO: Monitor não conseguiu iniciar!

⏰ Horário Limite: 9h00
🔄 Tentativas: 6

❌ STATUS: Monitor NÃO está rodando

⚠️ AÇÃO URGENTE:
1. Executar: .\STATUS.bat
2. Verificar logs em: logs\monitor_retornos.log
3. Tentar manualmente: .\INICIAR.bat
4. Processar pendentes: .\PROCESSAR.bat

Arquivos de retorno NÃO estão sendo processados!
```

---

## 🔧 Configuração

### Arquivo: `config.ini`

```ini
[VERIFICACAO_AGENDADA]
# Habilitar verificação agendada?
habilitado = true

# Horário inicial (30 minutos antes do prazo final)
horario = 08:30

# Dias da semana
dias_semana = segunda,terca,quarta,quinta,sexta
```

### Ajustar Horários

**Alterar horário inicial:**
```ini
horario = 08:00  # Começa às 8h, tenta até 8h30
horario = 09:00  # Começa às 9h, tenta até 9h30
```

**Prazo final:** Sempre 30 minutos após horário inicial
- Se `horario = 08:30` → Prazo final: 9h00
- Se `horario = 08:00` → Prazo final: 8h30
- Se `horario = 07:30` → Prazo final: 8h00

**Intervalo de tentativas:** Fixo em 5 minutos
- Total de 6 tentativas em 30 minutos

---

## 📊 Logs do Sistema

### Verificação Normal (Tudo OK)
```
2025-10-14 08:30:15 - INFO - ================================================================
2025-10-14 08:30:15 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 14/10/2025 às 08:30:15
2025-10-14 08:30:15 - INFO - ================================================================
2025-10-14 08:30:16 - INFO - ✅ Sistema OK - Monitor ativo (PID: 12345) e Servidor acessível
2025-10-14 08:30:16 - INFO - ================================================================
```

### Durante Recuperação
```
2025-10-14 08:30:15 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 14/10/2025 às 08:30:15
2025-10-14 08:30:15 - WARNING - ⚠️  SERVIDOR INACESSÍVEL!
2025-10-14 08:30:15 - WARNING - 🔄 Iniciando processo de recuperação...
2025-10-14 08:30:15 - INFO -    Tentativas a cada 5 minutos até 09:00
2025-10-14 08:30:15 - INFO -    Tentativa 1/6
2025-10-14 08:30:15 - INFO -    Próxima verificação em 5 minutos...

2025-10-14 08:35:10 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 14/10/2025 às 08:35:10
2025-10-14 08:35:10 - WARNING - ⚠️  SERVIDOR INACESSÍVEL!
2025-10-14 08:35:10 - INFO -    Tentativa 2/6
2025-10-14 08:35:10 - INFO -    Próxima verificação em 5 minutos...

2025-10-14 08:40:12 - INFO - 🔍 VERIFICAÇÃO AGENDADA - 14/10/2025 às 08:40:12
2025-10-14 08:40:13 - INFO - ✅ RECUPERAÇÃO BEM-SUCEDIDA!
2025-10-14 08:40:13 - INFO -    Recuperado após 3 tentativa(s)
2025-10-14 08:40:13 - INFO - 📧 Email de confirmação enviado
```

### Falha Crítica (Não recuperou)
```
2025-10-14 09:00:05 - ERROR - ================================================================
2025-10-14 09:00:05 - ERROR - ❌ FALHA CRÍTICA - Servidor continua inacessível
2025-10-14 09:00:05 - ERROR -    Tentativas: 6
2025-10-14 09:00:05 - ERROR -    Horário atual: 09:00
2025-10-14 09:00:05 - ERROR -    AÇÃO MANUAL URGENTE NECESSÁRIA!
2025-10-14 09:00:05 - ERROR - ================================================================
2025-10-14 09:00:06 - INFO - 📧 Email de falha crítica enviado
```

---

## 🧪 Como Testar

### Teste 1: Simular Servidor Inacessível às 8h30

1. **Antes das 8h30:**
   - Desconectar unidade de rede OU renomear pasta no servidor

2. **Às 8h30:**
   - Sistema detecta problema
   - Inicia tentativas de recuperação

3. **8h40 (exemplo):**
   - Reconectar servidor
   - Aguardar até próxima verificação (8h45)
   - Sistema deve detectar e enviar email de sucesso

### Teste 2: Simular Falha Total (Não recupera até 9h)

1. **Antes das 8h30:**
   - Desconectar servidor

2. **Deixar desconectado até 9h05**

3. **Verificar:**
   - Email de falha crítica deve chegar às 9h
   - Log deve mostrar 6 tentativas falhadas
   - Notificação Windows de erro crítico

### Teste 3: Monitor Parado (Servidor OK)

1. **Antes das 8h30:**
   - Executar `.\PARAR.bat`

2. **Às 8h30:**
   - Sistema detecta monitor parado
   - Tenta reiniciar automaticamente

3. **Resultado esperado:**
   - Monitor reinicia na primeira tentativa (8h30)
   - Email de confirmação (se configurado)

---

## ❓ Perguntas Frequentes

### P: Por que 8h30 e não 8h?
**R:** 8h30 dá uma margem de 30 minutos para recuperação antes do horário crítico de 9h, quando os colaboradores começam a adicionar arquivos.

### P: Posso mudar para começar às 8h?
**R:** Sim! Altere `horario = 08:00` no config.ini. O prazo final será automaticamente 8h30.

### P: Vou receber 6 emails (um por tentativa)?
**R:** **NÃO!** Você só recebe email:
- Se recuperar com sucesso antes das 9h (1 email)
- Se falhar até 9h (1 email de falha crítica)

### P: O que acontece se servidor voltar às 8h50?
**R:** Sistema detecta na próxima verificação (8h55 ou antes), processa arquivos pendentes e envia email de sucesso.

### P: E se problema for às 10h (fora do horário 8h30)?
**R:** O sistema de monitoramento contínuo (a cada 5 minutos, 24/7) cuida disso. Ele detecta e tenta recuperar independente do agendador das 8h30.

### P: Posso desabilitar essa verificação?
**R:** Sim, no config.ini:
```ini
[VERIFICACAO_AGENDADA]
habilitado = false
```
**Não recomendado!** Este recurso garante que sistema esteja funcionando no início do expediente.

---

## 🎯 Vantagens

### Antes
- ❌ Verificava só uma vez às 8h
- ❌ Se falhasse, não tentava novamente
- ❌ Colaborador podia adicionar arquivo sem monitor ativo
- ❌ Problema só detectado quando TI chegasse

### Agora
- ✅ Verifica às 8h30
- ✅ Tenta recuperar até 9h (6 tentativas)
- ✅ Email automático se falhar
- ✅ Margem de 30 min para resolver automaticamente
- ✅ TI notificado às 9h se não resolver

---

## 📞 Ações em Caso de Email de Falha Crítica

### 1. Verificar Servidor
```batch
# Tentar acessar pasta manualmente no Explorer
\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno

# Se não conseguir: servidor está offline ou rede com problema
```

### 2. Verificar Monitor
```batch
# Na pasta do projeto
.\STATUS.bat
```

### 3. Tentar Iniciar Manualmente
```batch
.\INICIAR.bat
```

### 4. Processar Arquivos Pendentes
```batch
.\PROCESSAR.bat
```

### 5. Verificar Logs
```
logs\monitor_retornos.log
logs\agendador.log
```

---

**Versão:** 2.1 - Verificação Inteligente  
**Data:** 14/10/2025  
**Status:** ✅ Implementado
