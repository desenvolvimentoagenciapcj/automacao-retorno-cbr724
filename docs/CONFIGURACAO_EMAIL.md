# 📧 Guia de Configuração de E-mail

## Visão Geral

O sistema agora suporta notificações por e-mail quando:
- ✅ Arquivos são processados com sucesso
- ❌ Ocorrem erros no processamento
- 🚀 O monitor é iniciado
- 📊 Relatórios diários (opcional)

---

## 🔧 Passo 1: Gerar Senha de App do Google Workspace

**IMPORTANTE:** Não use sua senha normal do e-mail! Use uma "Senha de App" específica.

### Como criar a Senha de App:

1. **Acesse sua conta Google:**
   - Vá para: https://myaccount.google.com/security
   - Faça login com: `charles.oliveira@agencia.baciaspcj.org.br`

2. **Ative a Verificação em Duas Etapas** (se ainda não estiver ativa):
   - Procure por "Verificação em duas etapas"
   - Clique em "Ativar"
   - Siga as instruções

3. **Gere uma Senha de App:**
   - Ainda em https://myaccount.google.com/security
   - Procure por "Senhas de app" (ou "App passwords")
   - Clique em "Senhas de app"
   - Selecione aplicativo: **"Outro (nome personalizado)"**
   - Digite o nome: **"Monitor Retornos CBR724"**
   - Clique em "Gerar"

4. **Copie a senha gerada:**
   - O Google exibirá uma senha de 16 caracteres
   - Exemplo: `abcd efgh ijkl mnop`
   - **Copie essa senha** (você não poderá vê-la novamente)

---

## ⚙️ Passo 2: Configurar o config.ini

Edite o arquivo: `config/config.ini`

Encontre a seção `[EMAIL]` e configure:

```ini
[EMAIL]
# Enviar notificações por e-mail? (true/false)
habilitado = true

# Servidor SMTP (Gmail: smtp.gmail.com, Outlook: smtp-mail.outlook.com)
smtp_servidor = smtp.gmail.com

# Porta SMTP (587 para TLS, 465 para SSL)
smtp_porta = 587

# E-mail remetente (Google Workspace da Agência PCJ)
remetente = charles.oliveira@agencia.baciaspcj.org.br

# Senha de App gerada no passo anterior
# COLE A SENHA SEM ESPAÇOS: abcdefghijklmnop
senha = sua_senha_de_app_aqui

# E-mails que receberão as notificações (separados por vírgula)
destinatarios = charles.oliveira@agencia.baciaspcj.org.br, outro@agencia.baciaspcj.org.br
```

### Exemplo de configuração preenchida:

```ini
[EMAIL]
habilitado = true
smtp_servidor = smtp.gmail.com
smtp_porta = 587
remetente = charles.oliveira@agencia.baciaspcj.org.br
senha = abcdefghijklmnop
destinatarios = charles.oliveira@agencia.baciaspcj.org.br, ti@agencia.baciaspcj.org.br
```

---

## 🧪 Passo 3: Testar a Configuração

### Método 1 - Usando o atalho (RECOMENDADO):

1. Na pasta raiz do projeto, execute: **`TESTAR_EMAIL.bat`**
2. Escolha a opção **"1 - Enviar e-mail de teste"**
3. Verifique sua caixa de entrada

### Método 2 - Linha de comando:

```powershell
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
python scripts\python\notificador_email.py
```

---

## 📨 Tipos de Notificações

### 1. E-mail de Sucesso
Enviado quando um arquivo é processado com sucesso:
- Nome do arquivo
- Data/hora do processamento
- Número de registros processados

### 2. E-mail de Erro
Enviado quando ocorre erro:
- Nome do arquivo
- Data/hora do erro
- Descrição do erro
- Ações necessárias

### 3. E-mail de Início
Enviado quando o monitor é iniciado:
- Pasta sendo monitorada
- Data/hora de início

### 4. Relatório Diário (opcional)
Resumo diário com estatísticas:
- Total de arquivos processados
- Total de erros
- Lista detalhada de sucessos e erros
- Taxa de sucesso

---

## ⚠️ Solução de Problemas

### Erro: "Autenticação SMTP falhou"

**Causa:** Senha incorreta ou senha normal em vez de senha de app.

**Solução:**
1. Gere uma nova Senha de App (Passo 1)
2. Copie a senha **SEM ESPAÇOS**
3. Cole no `config.ini`
4. Teste novamente

### Erro: "Conexão recusada" ou "Timeout"

**Causa:** Firewall bloqueando conexão SMTP.

**Solução:**
1. Verifique se está na rede da Agência PCJ
2. Teste conexão:
   ```powershell
   Test-NetConnection smtp.gmail.com -Port 587
   ```
3. Se bloqueado, contate o TI para liberar porta 587

### E-mails não chegam

**Possíveis causas:**
1. **Caixa de spam:** Verifique a pasta de spam/lixo eletrônico
2. **Destinatário errado:** Verifique o campo `destinatarios` no config.ini
3. **Notificações desabilitadas:** Verifique se `habilitado = true`

---

## 🔒 Segurança

### Boas práticas:

1. ✅ **Use Senha de App**, não a senha real do e-mail
2. ✅ Mantenha o `config.ini` **privado** (não compartilhe)
3. ✅ Se comprometida, **revogue** a senha de app e gere nova
4. ✅ Não versione o `config.ini` com senha no GitHub (já está no .gitignore)

### Como revogar uma Senha de App:

1. Acesse: https://myaccount.google.com/security
2. Vá em "Senhas de app"
3. Clique em "Remover" ao lado da senha comprometida
4. Gere uma nova senha

---

## 📋 Configurações Avançadas

### Usar outro servidor SMTP (Outlook):

```ini
smtp_servidor = smtp-mail.outlook.com
smtp_porta = 587
remetente = seu.email@outlook.com
```

### Desabilitar temporariamente:

```ini
habilitado = false
```

### Múltiplos destinatários:

```ini
destinatarios = email1@agencia.baciaspcj.org.br, email2@agencia.baciaspcj.org.br, email3@agencia.baciaspcj.org.br
```

---

## 🎯 Testando Diferentes Cenários

Execute: `TESTAR_EMAIL.bat`

Opções disponíveis:
1. **Teste de configuração** - Verifica se o e-mail está configurado
2. **Simular sucesso** - Envia e-mail como se arquivo fosse processado
3. **Simular erro** - Envia e-mail como se houvesse erro
4. **Simular relatório** - Envia relatório diário de exemplo

---

## 📞 Suporte

Se tiver problemas:

1. Verifique o log: `logs/monitor_retornos.log`
2. Execute o teste: `TESTAR_EMAIL.bat`
3. Revise este guia
4. Contate o TI se necessário

---

## ✅ Checklist Final

Antes de usar em produção:

- [ ] Senha de App gerada no Google Workspace
- [ ] `config.ini` configurado corretamente
- [ ] Teste executado com sucesso (`TESTAR_EMAIL.bat`)
- [ ] E-mail de teste recebido
- [ ] Destinatários corretos configurados
- [ ] `habilitado = true` no config.ini

---

**Última atualização:** 13/10/2025  
**Sistema:** Automação de Retornos CBR724  
**Agência das Bacias PCJ**
