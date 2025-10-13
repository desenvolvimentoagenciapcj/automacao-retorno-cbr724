# 🏦 Sistema de Automação - Retorno Bancário

Sistema completo para automatizar o processamento de arquivos de retorno bancário (CNAB) integrado com Microsoft Access.

## 🚀 Características Principais

- **Monitoramento Automático**: Detecta automaticamente novos arquivos de retorno
- **Processamento CNAB**: Suporta formatos CNAB240 e CNAB400
- **Integração Access**: Conecta diretamente com bancos Microsoft Access
- **Notificações Email**: Alertas automáticos por email
- **Dashboard Web**: Interface web para monitoramento em tempo real
- **Backup Automático**: Backup do banco antes de cada processamento
- **Log Detalhado**: Sistema completo de logs para auditoria

## 📦 Instalação Rápida

### 1. Pré-requisitos
- Python 3.8 ou superior
- Microsoft Access Database Engine 2016 Redistributable
- Banco de dados Microsoft Access configurado

### 2. Instalação Automática
```bash
# Clone ou baixe os arquivos do sistema
cd AutomacaoRetorno

# Execute o instalador (vai instalar tudo automaticamente)
python instalar.py
```

### 3. Configuração
1. Edite o arquivo `config.yaml` com suas configurações:
   - Caminho do banco Access
   - Configurações de email
   - Pastas de processamento
   - Credenciais de acesso

2. Teste a configuração:
```bash
python monitor_arquivos.py --teste
```

## 🎮 Como Usar

### Execução Manual
```bash
# Iniciar monitoramento
python monitor_arquivos.py

# Iniciar dashboard web
python dashboard.py
```

### Execução Simplificada (Windows)
```bash
# Duplo clique nos arquivos:
iniciar_monitor.bat      # Para o monitor
iniciar_dashboard.bat    # Para o dashboard
```

### Como Serviço do Windows
```bash
# Instalar como serviço (executar como administrador)
nssm install RetornoBancario monitor_arquivos.py
nssm start RetornoBancario
```

## 📁 Estrutura do Sistema

```
AutomacaoRetorno/
├── config.yaml              # Configurações do sistema
├── monitor_arquivos.py       # Monitor principal
├── processador_cnab.py       # Processador de arquivos CNAB
├── integrador_access.py      # Integração com Access
├── notificador.py           # Sistema de notificações
├── dashboard.py             # Interface web
├── instalar.py              # Script de instalação
├── requirements.txt         # Dependências Python
├── iniciar_monitor.bat      # Script Windows - Monitor
├── iniciar_dashboard.bat    # Script Windows - Dashboard
└── logs/                    # Pasta de logs
```

## ⚙️ Configuração Detalhada

### Arquivo config.yaml
```yaml
# Diretórios de trabalho
diretorios:
  entrada: "D:\\Retornos\\Entrada"      # Onde chegam os arquivos
  processados: "D:\\Retornos\\Processados"
  erro: "D:\\Retornos\\Erro"
  backup: "D:\\Retornos\\Backup"

# Banco Access
banco:
  caminho: "D:\\SeuBanco\\Database.mdb"
  tabela_titulos: "Titulos"
  tabela_baixas: "Baixas"
  backup_antes_processo: true

# Email (Gmail exemplo)
email:
  servidor_smtp: "smtp.gmail.com"
  porta: 587
  usuario: "seu_email@gmail.com"
  senha: "sua_senha_app"  # Senha de aplicativo
  destinatarios:
    - "gerencia@empresa.com"
    - "financeiro@empresa.com"

# Interface Web
web:
  host: "localhost"
  porta: 5000
  senha_admin: "admin123"  # ALTERAR!
```

### Estrutura do Banco Access
O sistema espera as seguintes tabelas no Access:

**Tabela Titulos:**
- Id (Chave primária)
- NossoNumero (Texto)
- SeuNumero (Texto)
- ValorTitulo (Moeda)
- DataVencimento (Data)
- Status (Texto)
- DataPagamento (Data)
- ValorPago (Moeda)

**Tabela Baixas:**
- Id (Chave primária)
- TituloId (Número - FK)
- NossoNumero (Texto)
- DataBaixa (Data)
- ValorPago (Moeda)
- TipoBaixa (Texto)

**Tabela Ocorrencias:**
- Id (Chave primária)
- TituloId (Número - FK)
- CodigoOcorrencia (Texto)
- DescricaoOcorrencia (Texto)
- DataOcorrencia (Data)
- DataProcessamento (Data)

## 🌐 Dashboard Web

Acesse `http://localhost:5000` para:
- Monitorar status do sistema em tempo real
- Ver arquivos processados e com erro
- Acompanhar logs do sistema
- Processar arquivos manualmente
- Visualizar estatísticas

**Login padrão**: senha `admin123` (altere no config.yaml)

## 📧 Notificações

O sistema envia emails automáticos para:
- ✅ Processamento bem-sucedido
- ❌ Erros no processamento
- 📊 Relatório diário (18h)

## 🔧 Fluxo de Processamento

1. **Detecção**: Sistema detecta novo arquivo na pasta de entrada
2. **Validação**: Verifica se é um arquivo CNAB válido
3. **Backup**: Cria backup do banco Access
4. **Processamento**: Interpreta o arquivo CNAB
5. **Integração**: Atualiza dados no Access
6. **Movimentação**: Move arquivo para pasta apropriada
7. **Notificação**: Envia email com resultado

## 🐛 Resolução de Problemas

### Erro: "Driver Access não encontrado"
```bash
# Instalar Microsoft Access Database Engine 2016
https://www.microsoft.com/download/details.aspx?id=54920
```

### Erro: "Conexão com banco falhada"
- Verificar caminho do banco no config.yaml
- Verificar se o banco não está aberto no Access
- Verificar permissões da pasta

### Erro: "Não foi possível enviar email"
- Verificar configurações SMTP
- Para Gmail: usar senha de aplicativo
- Verificar firewall/antivírus

### Logs não aparecem
- Verificar permissões da pasta logs/
- Verificar se o diretório foi criado

## 📋 Manutenção

### Backup Automático
- Sistema faz backup antes de cada processamento
- Backups ficam na pasta configurada
- Recomenda-se limpeza periódica (manter últimos 30 dias)

### Limpeza de Logs
- Logs são rotacionados automaticamente
- Máximo 10MB por arquivo
- Manter últimos 5 arquivos

### Monitoramento
- Acompanhar dashboard web regularmente
- Verificar emails de notificação
- Revisar logs em caso de problemas

## 🆘 Suporte

### Arquivos de Log
```
logs/monitor_YYYYMMDD.log  # Log do monitor
logs/dashboard.log         # Log da interface web
```

### Teste de Componentes
```bash
# Testar processador CNAB
python -c "from processador_cnab import ProcessadorCNAB; print('OK')"

# Testar integração Access
python -c "from integrador_access import IntegradorAccess; print('OK')"

# Testar notificações
python -c "from notificador import Notificador; print('OK')"
```

### Contato
Para suporte técnico, verifique os logs e entre em contato com:
- 📧 Email: suporte@empresa.com
- 📱 WhatsApp: (11) 99999-9999

---

## 🔄 Histórico de Versões

### v1.0.0 - Versão Inicial
- Monitor automático de arquivos
- Processamento CNAB240/400
- Integração com Access
- Notificações por email
- Dashboard web
- Sistema de backup

---

**Sistema desenvolvido para automatizar completamente o processamento de arquivos de retorno bancário, eliminando a necessidade de intervenção manual diária.** 🎉

**⚡ Economize horas de trabalho todos os dias com este sistema!**