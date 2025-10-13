# 🔄 Sistema Watchdog - Monitor do Monitor

> **Criado:** 2025-01-23  
> **Sistema:** Automação de Retornos CBR724  
> **Versão:** 1.0

---

## 📌 O Que é o Watchdog?

O **Watchdog** é um "**monitor do monitor**" - um sistema que:

- 🔍 Verifica se o `monitor_retornos.py` está rodando
- 🔄 **Reinicia automaticamente** se detectar que caiu
- 📧 Envia **alertas por e-mail** quando houver problemas
- 📊 Mantém **logs detalhados** de toda a atividade
- ⚡ Garante **máxima disponibilidade** do sistema

---

## 🎯 Por Que Usar o Watchdog?

### Problemas que o Watchdog Resolve:

❌ **Sem Watchdog:**
- Monitor pode cair à noite e ninguém percebe
- Arquivos não são processados por horas/dias
- Precisa verificar manualmente se está rodando
- Reinício manual toda vez que cai

✅ **Com Watchdog:**
- Monitor caiu? Reinicia **automaticamente** em 60 segundos
- Você é **notificado por e-mail** na hora
- Sistema se **auto-recupera** sem intervenção
- **Zero downtime** - máxima disponibilidade

---

## ⚙️ Como Funciona

### Ciclo de Verificação:

```
1. Watchdog verifica se monitor está rodando (a cada 60 segundos)
   ↓
2. Monitor está OK?
   ├─ SIM → Aguarda 60 segundos e verifica novamente
   └─ NÃO → Envia alerta e tenta reiniciar
              ↓
3. Tentativa de Reinício:
   ├─ Executa INICIAR_MONITOR_OCULTO.bat
   ├─ Aguarda 5 segundos
   └─ Verifica se reiniciou com sucesso
      ├─ SIM → Envia notificação de sucesso
      └─ NÃO → Tenta novamente (máximo 3 vezes)
                ↓
4. Após 3 Falhas:
   ├─ Envia alerta CRÍTICO por e-mail
   ├─ Aguarda 5 minutos
   └─ Reseta o contador e tenta novamente
```

---

## 🚀 Iniciar o Watchdog

### Método 1: Script BAT (Recomendado)

Dê um duplo clique em:
```
INICIAR_WATCHDOG.bat
```

O watchdog será iniciado **em segundo plano** (oculto).

---

### Método 2: Linha de Comando

```cmd
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
python watchdog_monitor.py
```

---

### Método 3: Iniciar com o Windows (Automático)

Para o watchdog iniciar automaticamente quando o Windows ligar:

1. **Pressione:** `Win + R`
2. **Digite:** `shell:startup`
3. **Copie:** Um atalho de `INICIAR_WATCHDOG.bat` para essa pasta

Pronto! O watchdog inicia automaticamente com o Windows.

---

## ⏹️ Parar o Watchdog

### Método 1: Script BAT (Recomendado)

Dê um duplo clique em:
```
PARAR_WATCHDOG.bat
```

---

### Método 2: Gerenciador de Tarefas

1. Abra o **Gerenciador de Tarefas** (Ctrl + Shift + Esc)
2. Vá na aba **Detalhes**
3. Procure por processos `python.exe`
4. Identifique o que tem `watchdog_monitor.py` na linha de comando
5. Clique com botão direito → **Finalizar Tarefa**

---

## 📊 Logs do Watchdog

### Arquivo de Log:
```
watchdog.log
```

### Conteúdo do Log:

```
[2025-01-23 08:00:00] Watchdog iniciado
[2025-01-23 08:00:00] Monitor está rodando (PID: 12345)
[2025-01-23 08:10:00] Verificação a cada 10 minutos - Monitor OK (PID: 12345)
[2025-01-23 14:30:00] ⚠️ ALERTA: Monitor não está rodando!
[2025-01-23 14:30:05] Tentativa de reinício 1/3...
[2025-01-23 14:30:10] ✅ Monitor reiniciado com sucesso! (PID: 23456)
```

### Características:

- ✅ Mantém apenas as **últimas 1000 linhas**
- ✅ Logs mais recentes no **topo do arquivo**
- ✅ Registra **todas as tentativas** de reinício
- ✅ Mostra **PIDs dos processos**

---

## 🔔 Notificações por E-mail

### E-mails que o Watchdog Envia:

#### 1. Monitor Caiu 🔴
```
Assunto: 🔴 ALERTA CRÍTICO - Monitor Caiu!

O monitor de retornos parou de funcionar!
O sistema tentará reiniciar automaticamente.

Data: 23/01/2025 14:30:00
```

#### 2. Monitor Reiniciado ✅
```
Assunto: ✅ Monitor Reiniciado

O monitor foi reiniciado com sucesso!
PID: 23456

Data: 23/01/2025 14:30:10
```

#### 3. Falha ao Reiniciar (após 3 tentativas) ❌
```
Assunto: ❌ FALHA AO REINICIAR MONITOR

Foram feitas 3 tentativas de reinício sem sucesso.
AÇÃO NECESSÁRIA: Verificar manualmente o sistema.

Verifique os logs para mais detalhes.
Data: 23/01/2025 14:32:00
```

**OBS:** Para receber e-mails, configure a seção `[EMAIL]` no `config.ini` (veja `SISTEMA_NOTIFICACOES.md`)

---

## ⚙️ Configurações Avançadas

### Alterar Intervalo de Verificação:

No arquivo `watchdog_monitor.py`, linha ~30:
```python
self.intervalo_verificacao = 60  # Altere para o número de segundos desejado
```

**Sugestões:**
- **30 segundos:** Verificação mais frequente (mais rápido para detectar problemas)
- **60 segundos:** Padrão (bom equilíbrio)
- **120 segundos:** Menos verificações (menor uso de recursos)

---

### Alterar Máximo de Tentativas:

No arquivo `watchdog_monitor.py`, linha ~31:
```python
self.max_tentativas_restart = 3  # Altere para quantas tentativas quiser
```

---

### Desativar E-mails:

No `config.ini`:
```ini
[EMAIL]
habilitado = false
```

O watchdog continuará funcionando, mas sem enviar e-mails.

---

## 🛠️ Solução de Problemas

### Watchdog Não Detecta o Monitor

**Sintoma:** Watchdog diz que monitor não está rodando, mas ele está.

**Solução:**
- Verifique se o monitor foi iniciado com `INICIAR_MONITOR_OCULTO.bat`
- O watchdog procura por processos Python executando `monitor_retornos.py`
- Confirme que o nome do arquivo está correto

---

### Watchdog Não Reinicia o Monitor

**Sintoma:** Watchdog detecta que monitor caiu, mas não consegue reiniciar.

**Possíveis causas:**

1. **Arquivo `INICIAR_MONITOR_OCULTO.bat` não encontrado:**
   - Confirme que o arquivo existe na mesma pasta
   - Verifique o caminho no log

2. **Permissões insuficientes:**
   - Execute como Administrador

3. **Python não encontrado:**
   - Verifique o `config.ini`, seção `[PYTHON]`, campo `executavel`

---

### Watchdog Está Reiniciando Infinitamente

**Sintoma:** Monitor reinicia, mas cai logo em seguida (loop infinito).

**Solução:**
- O watchdog tem proteção: após 3 falhas, aguarda 5 minutos
- Verifique os logs do monitor (`monitor_retornos.log`) para ver por que está caindo
- Possíveis causas:
  - Erro no código Python
  - Banco de dados inacessível
  - Pasta monitorada sem permissão

---

### Como Saber se o Watchdog Está Rodando?

**Método 1: Gerenciador de Tarefas**
- Procure por processos `python.exe`
- Verifique se há um com `watchdog_monitor.py` na linha de comando

**Método 2: Verificar Log**
- Abra `watchdog.log`
- Se há registros recentes (últimos 10 minutos), está rodando

**Método 3: Criar Script de Status** (TODO: implementar `STATUS_WATCHDOG.bat`)

---

## 📈 Estatísticas e Monitoramento

### Com o Watchdog Ativo:

- ✅ **Disponibilidade:** ~99.9% (máximo 1 minuto de downtime por queda)
- ✅ **Recuperação:** Automática em ~10 segundos
- ✅ **Visibilidade:** E-mails + logs completos
- ✅ **Confiabilidade:** Sistema se auto-recupera

---

## 🔐 Segurança

### Recomendações:

1. ✅ **Rode com usuário apropriado** (não administrador desnecessariamente)
2. ✅ **Proteja os logs** (podem conter informações sensíveis)
3. ✅ **Configure e-mails corporativos** (não pessoais)
4. ✅ **Monitore os e-mails de alerta** (não ignore)

---

## 💡 Boas Práticas

### Deploy em Produção:

1. ✅ Teste em ambiente de desenvolvimento primeiro
2. ✅ Configure notificações por e-mail
3. ✅ Verifique se está recebendo alertas
4. ✅ Teste o auto-restart (mate o monitor manualmente)
5. ✅ Configure para iniciar com o Windows
6. ✅ Monitore os logs nos primeiros dias

---

### Manutenção:

- 🔍 Revise `watchdog.log` semanalmente
- 📧 Verifique se está recebendo e-mails de alerta
- 📊 Analise quantas vezes o monitor caiu (se muito frequente, investigue a causa)

---

## 📚 Arquivos Relacionados

- **watchdog_monitor.py:** Código do watchdog
- **INICIAR_WATCHDOG.bat:** Inicia o watchdog
- **PARAR_WATCHDOG.bat:** Para o watchdog
- **watchdog.log:** Logs do watchdog
- **notificador_email.py:** Sistema de e-mails (usado pelo watchdog)
- **config.ini:** Configurações gerais

---

## 🎯 Checklist de Implementação

Antes de colocar em produção:

- [ ] Configurar `config.ini` seção `[EMAIL]`
- [ ] Testar notificações por e-mail
- [ ] Executar `INICIAR_WATCHDOG.bat`
- [ ] Verificar se watchdog iniciou (ver `watchdog.log`)
- [ ] Testar auto-restart (matar monitor manualmente)
- [ ] Confirmar que recebeu e-mail de alerta
- [ ] Confirmar que monitor foi reiniciado
- [ ] Configurar para iniciar com Windows (opcional)
- [ ] Documentar procedimentos para equipe

---

## 🚀 Exemplo de Fluxo Completo

### Cenário: Monitor cai às 3h da manhã

```
03:00:00 - Monitor trava por erro desconhecido
03:01:00 - Watchdog detecta que monitor não está rodando
03:01:00 - 📧 E-mail enviado: "Monitor Caiu!"
03:01:05 - Watchdog executa INICIAR_MONITOR_OCULTO.bat
03:01:10 - Monitor reinicia com sucesso (PID: 45678)
03:01:10 - 📧 E-mail enviado: "Monitor Reiniciado"
03:01:10 - Sistema volta a funcionar normalmente
```

**Resultado:**
- ✅ Downtime total: **~1 minuto**
- ✅ Intervenção manual: **zero**
- ✅ Você foi notificado: **sim**
- ✅ Sistema se recuperou: **automaticamente**

---

**Sistema autônomo = Sem preocupações = Mais tempo para focar no que importa! 🚀**
