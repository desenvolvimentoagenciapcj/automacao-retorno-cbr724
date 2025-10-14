# 🚨 PLANO DE CONTINGÊNCIA - Queda de Servidor

## 📋 O QUE ACONTECEU

~~Quando o servidor cai:~~
~~1. ❌ Monitor perde conexão com `\\SERVIDOR1\...`~~
~~2. ❌ Watchdog não detecta arquivos adicionados durante queda~~
~~3. ❌ Sistema **NÃO processa automaticamente** após servidor voltar~~
~~4. ❌ Arquivos ficam "presos" na pasta esperando processamento~~

### ✅ PROBLEMA RESOLVIDO (Versão Atualizada)

**O sistema agora:**
1. ✅ Detecta automaticamente quando servidor fica inacessível
2. ✅ Verifica a cada 5 minutos se servidor voltou
3. ✅ Processa automaticamente todos os arquivos pendentes ao recuperar
4. ✅ Envia alertas por email durante queda e recuperação

## 🆕 COMO FUNCIONA A RECUPERAÇÃO AUTOMÁTICA

### Durante Funcionamento Normal
- Monitor verifica saúde do servidor a cada 5 minutos
- Tudo funciona normalmente

### Quando Servidor Cai
1. **Detecção Automática** (em até 5 minutos)
   - Log registra: `⚠️ ALERTA: Servidor ficou inacessível!`
   - Notificação Windows: "Servidor Desconectado"
   - Email enviado: "🚨 SERVIDOR INACESSÍVEL - Monitor em Modo de Espera"

2. **Modo de Espera**
   - Sistema continua rodando
   - Tenta reconectar a cada 5 minutos
   - Arquivos adicionados durante queda ficam aguardando

3. **Recuperação Automática** (quando servidor volta)
   - Log registra: `✅ SERVIDOR RECUPERADO!`
   - Processa automaticamente TODOS os arquivos pendentes
   - Notificação Windows: "Servidor Reconectado"
   - Email enviado: "✅ SERVIDOR RECUPERADO - Sistema Operacional"

### ⚙️ Configuração (config.ini)
```ini
[MONITORAMENTO_SERVIDOR]
habilitado = true                    # Habilitar monitoramento de saúde
intervalo_verificacao = 300          # Verificar a cada 5 minutos
alertar_por_email = true             # Enviar emails de alerta
```

---

## 🎯 AÇÕES MANUAIS (Apenas se Necessário)

### ⚡ Solução Rápida - Processar Arquivos Agora

**Quando usar:** Apenas se após 10 minutos do servidor voltar, arquivos ainda não foram processados.

```powershell
.\PROCESSAR.bat
```

**O que faz:**
- ✅ Processa TODOS os arquivos `.ret` que estão na pasta
- ✅ Funciona mesmo com servidor instável
- ✅ Não depende do watchdog
- ✅ Envia notificações

### Opção 2: Reiniciar Monitor Completamente
```powershell
# 1. Parar monitor atual
.\PARAR.bat

# 2. Aguardar 5 segundos

# 3. Iniciar novamente
.\INICIAR.bat
```

**O que faz:**
- ✅ Reinicia conexão com servidor
- ✅ Processa arquivos existentes (se `processar_existentes_ao_iniciar = true`)
- ✅ Recomeça monitoramento

## 🔧 MELHORIAS IMPLEMENTADAS

### 1️⃣ **Detecção Automática de Queda de Servidor**

O sistema agora detecta quando:
- Servidor fica inacessível
- Pasta de rede desconecta
- Watchdog para de responder

### 2️⃣ **Reconexão Automática**

Quando servidor volta:
- ✅ Reconecta automaticamente
- ✅ Processa arquivos pendentes
- ✅ Envia notificação de recuperação

### 3️⃣ **Monitoramento de Saúde**

A cada 5 minutos verifica:
- Conexão com servidor está ativa?
- Pasta de rede está acessível?
- Watchdog está respondendo?

### 4️⃣ **Modo Fallback**

Se servidor estiver inacessível por muito tempo:
- ⚠️ Alerta via email
- 📝 Log detalhado do problema
- 🔄 Tenta reconectar a cada 2 minutos

## 📊 CHECKLIST PÓS-QUEDA

Execute esta checklist **sempre** que servidor voltar:

### ✅ **Passo 1: Verificar Status do Monitor**
```powershell
.\STATUS.bat
```

**Resultado esperado:**
- ✅ Monitor está rodando
- ✅ PID ativo
- ✅ Tempo de execução

**Se não estiver rodando:**
```powershell
.\INICIAR.bat
```

### ✅ **Passo 2: Verificar Arquivos Pendentes**
```powershell
# Ver arquivos na pasta de entrada
cd "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno"
Get-ChildItem *.ret
```

**Se houver arquivos:**
```powershell
# Voltar para raiz do projeto
cd "d:\Teste_Cobrança_Acess"

# Processar arquivos pendentes
.\PROCESSAR.bat
```

### ✅ **Passo 3: Verificar Logs**
```powershell
# Ver últimos logs
Get-Content "AutomacaoRetorno\logs\monitor.log" -Tail 20
```

**Procure por:**
- ✅ "Arquivo processado com sucesso"
- ⚠️ "Erro ao acessar pasta"
- ❌ "Servidor inacessível"

### ✅ **Passo 4: Testar Conexão**
```powershell
# Testar acesso ao servidor
Test-Path "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno"
```

**Resultado esperado:**
```
True
```

### ✅ **Passo 5: Verificar Email**

Checar se recebeu notificações:
- 📧 "Monitor Caiu" (durante queda)
- 📧 "Arquivos Processados" (após recuperação)

## 🔄 ROTINA PREVENTIVA

### Diariamente (Manhã)
```powershell
# Verificar status
.\STATUS.bat

# Ver se há arquivos pendentes
.\PROCESSAR.bat
```

### Semanalmente (Segunda-feira)
```powershell
# Verificar logs da semana anterior
Get-Content "AutomacaoRetorno\logs\monitor.log" -Tail 100
```

### Mensalmente
```powershell
# Verificar espaço em disco no servidor
Get-ChildItem "\\SERVIDOR1\CobrancaPCJ\CobrancaPCJ\Retorno" -Recurse | 
    Measure-Object -Property Length -Sum
```

## 🚨 ALERTAS CONFIGURADOS

### Email Automático em Caso de:

1. **Servidor Inacessível** (>5 minutos)
   - 📧 Para: backoffice@agencia.baciaspcj.org.br
   - ⚠️ Assunto: "ALERTA: Servidor Inacessível"

2. **Monitor Parou**
   - 📧 Verificação agendada (8h segunda a sexta)
   - 🔄 Reinicia automaticamente

3. **Erro no Processamento**
   - 📧 Email imediato com detalhes
   - 📝 Log completo do erro

4. **Arquivos Pendentes** (>10 arquivos)
   - 📧 Alerta diário
   - 📊 Lista de arquivos não processados

## 📞 CONTATOS DE EMERGÊNCIA

### Problema com Servidor
- **TI Infraestrutura**: [inserir contato]
- **Responsável Servidor**: [inserir contato]

### Problema com Sistema
- **Desenvolvedor**: charles.oliveira@agencia.baciaspcj.org.br
- **Backup Office**: backoffice@agencia.baciaspcj.org.br

## 📝 REGISTRO DE INCIDENTES

### Modelo de Registro:

```
DATA: 14/10/2025
HORA INÍCIO: [horário que servidor caiu]
HORA FIM: [horário que servidor voltou]
DURAÇÃO: [tempo total]

IMPACTO:
- [X] arquivos não processados
- Monitor [parou/continuou rodando]
- Notificações [enviadas/não enviadas]

AÇÃO TOMADA:
1. [o que foi feito]
2. [resultado]

ARQUIVOS PROCESSADOS MANUALMENTE:
- [lista de arquivos]

RESPONSÁVEL: [nome]
```

## 🎯 PREVENÇÃO FUTURA

### Já Implementado:
- ✅ Detecção automática de queda
- ✅ Reconexão automática
- ✅ Processamento de arquivos existentes
- ✅ Monitoramento de saúde
- ✅ Alertas via email

### Próximas Melhorias:
- ⏳ Fila de processamento persistente
- ⏳ Retry automático em caso de falha
- ⏳ Dashboard web de monitoramento
- ⏳ Backup local temporário

## 📚 DOCUMENTOS RELACIONADOS

- `DOCUMENTACAO_SISTEMA.md` - Manual completo
- `AGENDADOR_VERIFICACAO.md` - Sistema de verificação agendada
- `NOTIFICACOES_EMAIL.md` - Configuração de alertas

---

**IMPORTANTE:** Após queda de servidor, **SEMPRE** execute:
```powershell
.\PROCESSAR.bat
```

Isso garante que nenhum arquivo fique sem processar!
