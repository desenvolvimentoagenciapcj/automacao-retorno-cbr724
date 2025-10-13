# 📧 Sistema de Notificações por E-mail

> **Criado:** 2025-01-23  
> **Sistema:** Automação de Retornos CBR724  
> **Versão:** 1.0

---

## 📌 Visão Geral

O sistema de notificações permite que você seja **alertado por e-mail** sobre todos os eventos importantes do sistema:

- ✅ **Processamento bem-sucedido** (com estatísticas detalhadas)
- ❌ **Erros no processamento** (com detalhes do erro)
- 🟢 **Monitor iniciado**
- 🟡 **Monitor parado manualmente**
- 🔴 **Monitor caiu** (alerta crítico)

---

## ⚙️ Configuração

### 1. Habilitar Notificações

No arquivo `config.ini`, configure a seção `[EMAIL]`:

```ini
[EMAIL]
# Enviar notificações? (true para ativar, false para desativar)
habilitado = true

# Servidor SMTP
smtp_servidor = smtp.gmail.com

# Porta SMTP (587 para TLS)
smtp_porta = 587

# E-mail remetente
remetente = seuemail@gmail.com

# Senha de App (veja como criar abaixo)
senha = xxxx xxxx xxxx xxxx

# E-mails que receberão as notificações (separados por vírgula)
destinatarios = email1@example.com, email2@example.com
```

---

### 2. Criar Senha de App no Gmail

O Gmail não aceita senha normal por questões de segurança. Você precisa criar uma **Senha de App**:

#### Passo a Passo:

1. **Acesse:** [https://myaccount.google.com/security](https://myaccount.google.com/security)

2. **Ative a Verificação em Duas Etapas:**
   - Vá em "Verificação em duas etapas"
   - Clique em "Começar"
   - Siga as instruções

3. **Crie a Senha de App:**
   - Volte em [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Procure por "Senhas de app"
   - Clique em "Senhas de app"
   - Em "Selecionar app", escolha "Outro (nome personalizado)"
   - Digite: "Monitor Retornos CBR724"
   - Clique em "Gerar"

4. **Copie a Senha:**
   - Uma senha de 16 caracteres será gerada (ex: `xxxx xxxx xxxx xxxx`)
   - Copie e cole no `config.ini` no campo `senha`
   - **IMPORTANTE:** Não adicione espaços entre os blocos, copie exatamente como mostrado

---

### 3. Configurar Outros Provedores de E-mail

#### Outlook/Hotmail:
```ini
smtp_servidor = smtp-mail.outlook.com
smtp_porta = 587
remetente = seuemail@outlook.com
```

#### Yahoo Mail:
```ini
smtp_servidor = smtp.mail.yahoo.com
smtp_porta = 587
remetente = seuemail@yahoo.com
```

#### Gmail Corporativo (Google Workspace):
```ini
smtp_servidor = smtp.gmail.com
smtp_porta = 587
remetente = seuemail@suaempresa.com.br
```

---

## 📨 Tipos de Notificações

### 1. Processamento Bem-Sucedido ✅
**Quando:** Arquivo CBR724 processado com sucesso  
**Cor:** Verde  
**Conteúdo:**
- Nome do arquivo processado
- Total de títulos criados
- Total de títulos pagos
- Total de títulos cancelados
- Data e hora do processamento

**Exemplo de E-mail:**
```
Assunto: ✅ Processamento Concluído - CBR724001.ret

Arquivo: CBR724001.ret processado com sucesso!

Títulos Criados: 45
Títulos Pagos: 23
Títulos Cancelados: 2

Processado em: 23/01/2025 14:30:45
```

---

### 2. Erro no Processamento ❌
**Quando:** Erro ao processar arquivo  
**Cor:** Vermelho  
**Conteúdo:**
- Nome do arquivo que deu erro
- Descrição do erro
- Data e hora

**Exemplo de E-mail:**
```
Assunto: ❌ Erro no Processamento - CBR724002.ret

Arquivo: CBR724002.ret

ERRO: Não foi possível conectar ao banco de dados.

Data: 23/01/2025 14:35:12
```

---

### 3. Monitor Iniciado 🟢
**Quando:** Monitor de retornos é iniciado  
**Cor:** Azul  
**Conteúdo:**
- Confirmação de início
- Pasta monitorada
- Data e hora

---

### 4. Monitor Parado 🟡
**Quando:** Monitor é parado manualmente  
**Cor:** Amarelo  
**Conteúdo:**
- Motivo da parada
- Data e hora

---

### 5. Monitor Caiu 🔴
**Quando:** Watchdog detecta que o monitor parou de funcionar  
**Cor:** Vermelho (Alerta Crítico)  
**Conteúdo:**
- Alerta de que o monitor caiu
- Informação sobre tentativa de reinício
- Data e hora

**Exemplo de E-mail:**
```
Assunto: 🔴 ALERTA CRÍTICO - Monitor Caiu!

ATENÇÃO: O monitor de retornos parou de funcionar!

O sistema tentará reiniciar automaticamente.
Se o problema persistir, verifique os logs.

Data: 23/01/2025 03:15:45
```

---

## 🧪 Testar Notificações

Para testar se as notificações estão funcionando:

1. **Configure o `config.ini`** com suas credenciais de e-mail

2. **Execute o teste:**
   ```cmd
   python notificador_email.py
   ```

3. **Resultado esperado:**
   - Mensagem no console: "E-mail de teste enviado com sucesso!"
   - E-mail recebido em poucos segundos

---

## 🛠️ Integração com o Monitor

O sistema já está integrado automaticamente:

- **monitor_retornos.py:** Envia notificações ao processar arquivos
- **watchdog_monitor.py:** Envia alertas quando monitor cai/reinicia

Não é necessário fazer nada manualmente!

---

## ⚠️ Solução de Problemas

### Erro: "Falha ao enviar e-mail"

**Possíveis causas:**

1. **Senha incorreta:**
   - Verifique se está usando **Senha de App**, não a senha normal
   - Confirme que copiou a senha corretamente (sem espaços extras)

2. **Verificação em duas etapas não ativada:**
   - A senha de app só funciona se você ativou a verificação em 2 etapas

3. **Gmail bloqueando:**
   - Acesse: [https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps)
   - Ative "Permitir aplicativos menos seguros" (se disponível)

4. **Firewall/Antivírus:**
   - Verifique se o firewall não está bloqueando a porta 587

---

### Erro: "Connection timed out"

**Solução:**
- Verifique sua conexão com a internet
- Confirme que a porta 587 não está bloqueada
- Tente usar a porta 465 (SSL):
  ```ini
  smtp_porta = 465
  ```

---

### Erro: "Invalid credentials"

**Solução:**
- Confirme que o e-mail remetente está correto
- Recrie a senha de app do Gmail
- Verifique se não há espaços extras na senha

---

## 📊 Estatísticas

Com as notificações ativas, você terá:

- **Visibilidade total** do que está acontecendo
- **Auditoria completa** de todos os processamentos
- **Alertas imediatos** em caso de problemas
- **Histórico** de eventos no seu e-mail

---

## 🔐 Segurança

### Recomendações:

1. **Nunca compartilhe sua senha de app**
2. **Use e-mails corporativos** para produção
3. **Configure destinatários específicos** (não use e-mails pessoais)
4. **Revogue senhas antigas** se não estiverem mais em uso
5. **Mantenha o `config.ini` protegido** (não compartilhe o arquivo)

---

## 💡 Dicas

### Desativar temporariamente:
```ini
habilitado = false
```

### Múltiplos destinatários:
```ini
destinatarios = ti@empresa.com, gerente@empresa.com, suporte@empresa.com
```

### Testar sem enviar:
- Deixe `habilitado = false`
- O sistema funcionará normalmente, mas sem enviar e-mails

---

## 📚 Arquivos Relacionados

- **notificador_email.py:** Código do sistema de notificações
- **watchdog_monitor.py:** Usa notificações para alertas
- **monitor_retornos.py:** Envia notificações ao processar
- **config.ini:** Configuração de e-mail na seção `[EMAIL]`

---

## 🎯 Próximos Passos

Após configurar as notificações:

1. ✅ Configure o `config.ini`
2. ✅ Teste com `python notificador_email.py`
3. ✅ Reinicie o monitor
4. ✅ Aguarde a primeira notificação
5. ✅ Verifique se está recebendo e-mails

---

**Sistema funcionando = E-mails sendo enviados = Você informado! 🚀**
