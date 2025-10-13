# 🤖 Automação de Retornos CBR724

Sistema automatizado para processamento de arquivos de retorno bancário CBR724 (CNAB240/CNAB400) com integração ao Microsoft Access.

## 📋 Descrição

Este sistema monitora automaticamente uma pasta de entrada, processa arquivos de retorno bancário e integra os dados com bancos Access, gerando PDFs de comprovantes quando necessário.

## ✨ Funcionalidades

### 🎯 Principais
- **Monitoramento automático** de pasta para novos arquivos `.ret`
- **Processamento CBR724** (CNAB240 e CNAB400)
- **Integração com Access** via ODBC
- **Geração automática de PDFs** de comprovantes
- **Notificações** (Windows + Email)
- **Verificação agendada** do sistema (segunda a sexta, 8h)
- **Auto-reinicialização** em caso de falha

### 🛡️ Proteções
1. **Camada 1**: Monitor watchdog para novos arquivos
2. **Camada 2**: Processamento de arquivos existentes ao iniciar
3. **Camada 3**: Notificações duplas (Windows + Email)
4. **Camada 4**: Verificação agendada + auto-restart

## 📁 Estrutura do Projeto

```
Teste_Cobrança_Acess/
├── scripts/
│   ├── python/          # Scripts Python
│   │   ├── monitor_retornos.py
│   │   ├── processador_cbr724.py
│   │   ├── integrador_access.py
│   │   ├── agendador_verificacao.py
│   │   ├── notificador_email.py
│   │   └── ...
│   ├── powershell/      # Scripts PowerShell
│   └── bat/             # Scripts Batch
├── config/
│   ├── config.ini       # Configurações centralizadas
│   └── requirements.txt # Dependências Python
├── docs/                # Documentação completa
├── logs/                # Logs do sistema
├── Retorno/             # Pasta monitorada
├── PDFs/                # PDFs gerados
└── Quick Access:        # Atalhos raiz
    ├── INICIAR.bat
    ├── PARAR.bat
    ├── STATUS.bat
    ├── PROCESSAR.bat
    └── AGENDADOR.bat
```

## 🚀 Início Rápido

### Requisitos
- Python 3.8+
- Microsoft Access (ODBC Driver)
- Windows 10/11

### Instalação

1. **Clone o repositório**
```powershell
git clone <url-do-repositorio>
cd Teste_Cobrança_Acess
```

2. **Instale as dependências**
```powershell
pip install -r config\requirements.txt
```

3. **Configure o arquivo config.ini**
```powershell
notepad config\config.ini
```

### Uso Básico

#### Iniciar o Monitor
```powershell
.\INICIAR.bat
```

#### Verificar Status
```powershell
.\STATUS.bat
```

#### Parar o Monitor
```powershell
.\PARAR.bat
```

#### Processar Arquivos Existentes
```powershell
.\PROCESSAR.bat
```

#### Iniciar Verificação Agendada
```powershell
.\AGENDADOR.bat
```

## 📧 Notificações por Email

O sistema envia emails automáticos para:
- ✅ Arquivos processados com sucesso
- ❌ Erros de processamento
- 🚀 Monitor iniciado
- 📊 Relatório diário (final do dia)

Configure em `config/config.ini` seção `[EMAIL]`.

## ⏰ Verificação Agendada

O agendador verifica automaticamente se o monitor está rodando:
- **Horário padrão**: 8h da manhã
- **Dias**: Segunda a sexta
- **Ação**: Reinicia automaticamente se detectar que caiu

Configure em `config/config.ini` seção `[VERIFICACAO_AGENDADA]`.

## 📖 Documentação Completa

Acesse a pasta `docs/` para documentação detalhada:

- **DOCUMENTACAO_SISTEMA.md** - Manual completo do sistema
- **CONFIGURACAO_EMAIL.md** - Guia de configuração de emails
- **NOTIFICACOES_EMAIL.md** - Referência rápida de notificações
- **AGENDADOR_VERIFICACAO.md** - Guia do agendador

## 🔧 Configuração

Todas as configurações estão centralizadas em `config/config.ini`:

```ini
[DIRETORIOS]
pasta_retorno = D:\Teste_Cobrança_Acess\Retorno
pasta_processados = D:\Teste_Cobrança_Acess\Retorno\Processados
pasta_erro = D:\Teste_Cobrança_Acess\Retorno\Erro
pasta_backup = D:\Teste_Cobrança_Acess\Backup
pasta_pdfs = D:\Teste_Cobrança_Acess\PDFs

[EMAIL]
smtp_servidor = smtp.gmail.com
smtp_porta = 587
remetente = seu-email@dominio.com
senha = sua-senha-app
destinatarios = destinatario1@dominio.com, destinatario2@dominio.com

[VERIFICACAO_AGENDADA]
habilitado = true
horario = 08:00
dias_semana = segunda,terca,quarta,quinta,sexta
```

## 🛠️ Solução de Problemas

### Monitor não reconhece arquivos existentes
Execute `.\PROCESSAR.bat` para processar arquivos que já estavam na pasta.

### Emails não estão sendo enviados
1. Verifique as configurações em `[EMAIL]`
2. Use senha de app do Google (não a senha normal)
3. Execute `scripts\bat\TESTAR_EMAIL.bat`

### Monitor caiu e não reiniciou
1. Verifique se o agendador está rodando
2. Execute `.\AGENDADOR.bat` para iniciar
3. Configure Windows Task Scheduler (veja documentação)

## 📊 Logs

Todos os logs ficam em `logs/`:
- `monitor.log` - Log principal do monitor
- `agendador.log` - Log do agendador de verificação
- `processamento.log` - Detalhes de processamento

## 🤝 Contribuindo

Este é um projeto interno. Para sugestões ou problemas, contate o administrador do sistema.

## 📝 Licença

Uso interno - Fundação Agência das Bacias PCJ

## 📧 Contato

Para suporte técnico, consulte a documentação em `docs/` ou contate o TI.

---

**Última atualização**: 13/10/2025
**Versão**: 2.0 (Sistema Completo com Verificação Agendada)
