# ✅ Sistema de Recuperação Automática Implementado

## 🎯 Problema Resolvido

**Situação Anterior:**
- Quando servidor caía, sistema parava de funcionar
- Mesmo após servidor voltar, arquivos não eram processados
- Era necessário intervenção manual

**Solução Implementada:**
- ✅ Detecção automática de queda de servidor
- ✅ Verificação contínua de saúde (a cada 5 minutos)
- ✅ Recuperação automática quando servidor volta
- ✅ Processamento automático de arquivos pendentes
- ✅ Alertas por email durante todo o processo

---

## 🔄 Como Funciona

### 1. Monitoramento Contínuo
```
┌─────────────────────────────────────────────┐
│  Monitor de Retornos                         │
│                                              │
│  ✅ Processando arquivos...                 │
│  ✅ Verificando saúde do servidor (5min)    │
└─────────────────────────────────────────────┘
```

### 2. Detecção de Problema (até 5 min)
```
┌─────────────────────────────────────────────┐
│  ⚠️  SERVIDOR INACESSÍVEL DETECTADO         │
│                                              │
│  Ações Automáticas:                          │
│  • Log: "ALERTA: Servidor inacessível"      │
│  • Notificação Windows                       │
│  • Email enviado para backoffice            │
│  • Entrar em modo de espera                 │
└─────────────────────────────────────────────┘
```

### 3. Modo de Espera
```
┌─────────────────────────────────────────────┐
│  🔄 TENTANDO RECONECTAR...                  │
│                                              │
│  • Verificação a cada 5 minutos             │
│  • Sistema continua rodando                 │
│  • Arquivos acumulam na pasta               │
│  • Aguardando servidor voltar               │
└─────────────────────────────────────────────┘
```

### 4. Recuperação Automática (até 5 min após servidor voltar)
```
┌─────────────────────────────────────────────┐
│  ✅ SERVIDOR RECUPERADO!                    │
│                                              │
│  Ações Automáticas:                          │
│  • Log: "SERVIDOR RECUPERADO"               │
│  • Processar TODOS arquivos pendentes       │
│  • Notificação Windows                       │
│  • Email de confirmação                     │
│  • Voltar ao funcionamento normal           │
└─────────────────────────────────────────────┘
```

---

## 📧 Notificações por Email

### Email 1: Servidor Inacessível
```
Assunto: 🚨 SERVIDOR INACESSÍVEL - Monitor em Modo de Espera

Corpo:
- Pasta monitorada que ficou inacessível
- Horário da detecção
- Ações automáticas em andamento
- Instruções caso servidor demore a voltar
```

### Email 2: Servidor Recuperado
```
Assunto: ✅ SERVIDOR RECUPERADO - Sistema Operacional

Corpo:
- Confirmação de recuperação
- Horário da recuperação
- Quantidade de arquivos processados
- Confirmação que sistema está normal
```

---

## ⚙️ Configuração

### Arquivo: `config.ini`

```ini
[MONITORAMENTO_SERVIDOR]
# Habilitar verificação de saúde?
habilitado = true

# Intervalo de verificação (segundos)
# 300 = 5 minutos
# 180 = 3 minutos
# 600 = 10 minutos
intervalo_verificacao = 300

# Enviar emails de alerta?
alertar_por_email = true
```

### Ajustar Intervalo de Verificação

**Intervalo Menor (3 minutos):**
- ✅ Detecta problema mais rápido
- ✅ Recupera mais rápido
- ⚠️ Mais verificações = mais recursos

**Intervalo Maior (10 minutos):**
- ✅ Menos uso de recursos
- ⚠️ Demora mais para detectar/recuperar

**Recomendado:** 5 minutos (padrão)

---

## 🧪 Como Testar

### Teste Completo Automatizado
```batch
.\TESTAR_RECUPERACAO.bat
```

Este script testa todo o fluxo:
1. Verifica se monitor está rodando
2. Orienta como simular queda
3. Aguarda detecção (6 min)
4. Orienta como reconectar
5. Aguarda recuperação (6 min)
6. Verifica logs e resultados

### Teste Manual Rápido

1. **Simular Queda**
   ```
   - Desconectar unidade de rede mapeada, OU
   - Renomear pasta "Retorno" no servidor
   ```

2. **Aguardar Detecção** (até 5 minutos)
   - Verificar log: `logs\monitor_retornos.log`
   - Procurar linha: "ALERTA: Servidor ficou inacessível"
   - Verificar email recebido

3. **Reconectar Servidor**
   ```
   - Reconectar unidade de rede, OU
   - Voltar nome original da pasta
   ```

4. **Aguardar Recuperação** (até 5 minutos)
   - Verificar log: "SERVIDOR RECUPERADO"
   - Verificar email de confirmação
   - Confirmar que arquivos foram processados

---

## 📊 Logs do Sistema

### Durante Queda
```
2025-10-14 09:23:15 - WARNING - ============================================================
2025-10-14 09:23:15 - WARNING - ⚠️  ALERTA: Servidor ficou inacessível!
2025-10-14 09:23:15 - WARNING -    Pasta: \\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno
2025-10-14 09:23:15 - WARNING -    Tentando reconectar a cada 300s...
2025-10-14 09:23:15 - WARNING - ============================================================
2025-10-14 09:23:15 - INFO - 📧 Alerta por email enviado sobre servidor inacessível
```

### Durante Recuperação
```
2025-10-14 09:35:20 - INFO - ============================================================
2025-10-14 09:35:20 - INFO - ✅ SERVIDOR RECUPERADO!
2025-10-14 09:35:20 - INFO -    Processando arquivos pendentes...
2025-10-14 09:35:20 - INFO - ============================================================
2025-10-14 09:35:20 - INFO - 📁 Verificando arquivos existentes em: \\SERVIDOR1\...
2025-10-14 09:35:21 - INFO - 📦 Encontrados 3 arquivos .ret para processar
2025-10-14 09:35:21 - INFO - ✅ RETORNO_001.ret processado com sucesso
2025-10-14 09:35:22 - INFO - ✅ RETORNO_002.ret processado com sucesso
2025-10-14 09:35:23 - INFO - ✅ RETORNO_003.ret processado com sucesso
2025-10-14 09:35:23 - INFO - 📧 Email de recuperação enviado
```

---

## ❓ Perguntas Frequentes

### P: E se servidor demorar horas para voltar?
**R:** Sistema continuará tentando reconectar indefinidamente. Você receberá apenas 1 email avisando sobre queda. Quando servidor voltar (mesmo que seja no dia seguinte), sistema recuperará automaticamente.

### P: Preciso fazer algo manualmente?
**R:** **NÃO!** Sistema se recupera sozinho. Apenas se após 10 minutos do servidor voltar nada acontecer, execute `.\PROCESSAR.bat`

### P: Os arquivos adicionados durante queda serão perdidos?
**R:** **NÃO!** Todos os arquivos adicionados à pasta durante queda serão processados automaticamente quando servidor voltar.

### P: Como sei se funcionou?
**R:** Você receberá 2 emails:
1. Quando servidor cair: "🚨 SERVIDOR INACESSÍVEL"
2. Quando recuperar: "✅ SERVIDOR RECUPERADO"

### P: Posso desabilitar este recurso?
**R:** Sim, no `config.ini`:
```ini
[MONITORAMENTO_SERVIDOR]
habilitado = false
```
**Não recomendado!** Este recurso protege contra quedas de servidor.

### P: 5 minutos é muito tempo de espera?
**R:** Você pode reduzir para 3 minutos (180 segundos) ou até 1 minuto (60 segundos) em `config.ini`:
```ini
intervalo_verificacao = 180  # 3 minutos
```
Mas quanto menor o intervalo, mais verificações o sistema fará.

---

## 📝 Checklist de Implantação

- [x] Código atualizado em `monitor_retornos.py`
- [x] Configuração adicionada em `config.ini`
- [x] Classe `Config` atualizada
- [x] Emails de alerta configurados
- [x] Script de teste criado (`TESTAR_RECUPERACAO.bat`)
- [x] Documentação criada
- [ ] **TESTAR EM PRODUÇÃO** (executar `TESTAR_RECUPERACAO.bat`)
- [ ] Validar recebimento de emails
- [ ] Confirmar que arquivos são processados após recuperação

---

## 🎉 Benefícios

### Antes
- ❌ Intervenção manual necessária após queda
- ❌ Arquivos ficavam sem processar
- ❌ Necessário monitorar constantemente
- ❌ Colaborador tinha que avisar TI

### Agora
- ✅ Recuperação totalmente automática
- ✅ Todos os arquivos são processados
- ✅ Alertas automáticos por email
- ✅ Sistema se auto-recupera
- ✅ TI é notificado automaticamente

---

## 📞 Suporte

**Se precisar de ajuda:**
1. Verificar logs: `logs\monitor_retornos.log`
2. Executar: `.\STATUS.bat`
3. Em caso de dúvida, executar: `.\PROCESSAR.bat` (processa arquivos pendentes)
4. Contatar TI: backoffice@agencia.baciaspcj.org.br

---

**Versão:** 2.0 - Recuperação Automática  
**Data:** 14/10/2025  
**Status:** ✅ Implementado e Pronto para Produção
