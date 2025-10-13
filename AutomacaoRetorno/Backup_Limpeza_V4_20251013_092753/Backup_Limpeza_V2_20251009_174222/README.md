# 🤖 Sistema de Automação de Retornos Bancários CBR724

Sistema automático para processar arquivos de retorno bancário no formato CBR724 e integrar com banco de dados Microsoft Access.

## 📋 Funcionalidades

✅ **Monitoramento Automático** - Detecta novos arquivos .ret na pasta configurada  
✅ **Processamento CBR724** - Extrai dados de pagamentos, cancelamentos e registros  
✅ **Integração Access** - Atualiza automaticamente o banco de dados  
✅ **Lógica VBA Replicada** - Implementa exatamente a mesma lógica do sistema legado  
✅ **Extração de Datas** - Pega a data correta do arquivo (não usa data atual)  
✅ **Organização Automática** - Move arquivos para pastas Processados/ ou Erro/  
✅ **Log Detalhado** - Registra todas as operações para auditoria  

## 🚀 Como Usar

### 1️⃣ Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Configuração

Edite o arquivo `monitor_retornos.py` e ajuste os caminhos:

```python
config = {
    'bancos': {
        'baixa': {
            'caminho': r'D:\SeuCaminho\dbBaixa2025.accdb'  # ← Seu banco principal
        },
        'cobranca': {
            'caminho': r'D:\SeuCaminho\Cobranca2019.accdb',  # ← Seu banco secundário
            'ativo': True  # False para desabilitar
        }
    }
}
```

### 3️⃣ Executar

**Modo Manual:**
```bash
# Duplo clique no arquivo ou execute:
INICIAR_MONITOR.bat
```

O monitor ficará rodando e processará automaticamente qualquer arquivo `.ret` que aparecer na pasta `Retorno/`.

### 4️⃣ Parar o Monitor

Pressione `Ctrl+C` no terminal para encerrar.

## 📁 Estrutura de Pastas

```
Retorno/
├── arquivo.ret           ← Coloque arquivos aqui
├── Processados/          ← Arquivos processados com sucesso
│   └── arquivo-processado.ret
├── Erro/                 ← Arquivos com erro
│   └── arquivo-erro_20241008_123456.ret
└── monitor_retornos.log  ← Log de todas operações
```

## 📊 Formato CBR724

O sistema processa arquivos no formato CBR724 com:

- **Tipo 28**: Header com data do arquivo (posições 115-122, formato DDMMAAAA)
- **Tipo 7**: Registros de baixa/pagamento (operações LQ, BX, RG, etc.)
- **Tipo 37**: Registros complementares

### Operações Suportadas

| Código | Operação | Ação |
|--------|----------|------|
| **LQ** | Liquidação | Marca título como PAGO |
| **BX** | Baixa | Marca título como CANCELADO |
| **RG** | Registro | Cria novo título (se não existir) |
| **VC** | Vencimento | Operação ignorada (warning) |

## 🔧 Arquivos do Sistema

| Arquivo | Descrição |
|---------|-----------|
| `monitor_retornos.py` | Monitor principal (watchdog) |
| `processador_cbr724.py` | Parser de arquivos CBR724 |
| `integrador_access.py` | Integração com Access (pyodbc) |
| `INICIAR_MONITOR.bat` | Script para iniciar monitor |
| `requirements.txt` | Dependências Python |

## 📝 Logs

Todas as operações são registradas em `monitor_retornos.log`:

```
2025-10-08 16:38:19 - INFO - 🆕 NOVO ARQUIVO DETECTADO: arquivo.ret
2025-10-08 16:38:20 - INFO - 📋 Tipo detectado: CBR724
2025-10-08 16:38:21 - INFO - 📅 Data do arquivo extraída: 01/10/2025
2025-10-08 16:38:22 - INFO - ✓ 10 registros encontrados
2025-10-08 16:38:25 - INFO - ✅ Processamento concluído com sucesso!
2025-10-08 16:38:25 - INFO -    • Processados: 10
2025-10-08 16:38:25 - INFO -    • Baixas: 7
2025-10-08 16:38:31 - INFO - 📦 Movido para: arquivo-processado.ret
```

## ⚙️ Requisitos

- **Python 3.8+**
- **Microsoft Access** (instalado na máquina)
- **Windows** (Access Driver for ODBC)
- **Dependências Python**:
  - `pyodbc` - Conexão com Access
  - `watchdog` - Monitoramento de arquivos
  - `python-dateutil` - Manipulação de datas

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Arquivos `.accdb` (bancos Access) **NÃO** são versionados
- Arquivos `.ret` (retornos bancários) **NÃO** são versionados
- Logs com dados sensíveis **NÃO** são versionados
- Configure seu `.gitignore` adequadamente

## 💡 Dicas

1. **Backup**: Configure backup automático dos bancos Access antes de usar
2. **Teste**: Teste primeiro com cópias dos bancos, não os originais
3. **Monitoramento**: Deixe a janela do monitor aberta para ver o processamento em tempo real
4. **Performance**: O monitor usa ~0% de CPU quando ocioso (sistema de eventos)

## 🐛 Solução de Problemas

### Erro: "Microsoft Access Driver não encontrado"
```bash
# Instale o Access Database Engine 2016:
# https://www.microsoft.com/en-us/download/details.aspx?id=54920
```

### Erro: "Banco de dados está bloqueado"
```bash
# Feche o Microsoft Access antes de processar
# Ou desabilite o banco secundário se estiver em rede
```

### Arquivos vão para pasta Erro/
```bash
# Verifique o log: monitor_retornos.log
# Causas comuns:
# - Formato de arquivo inválido
# - Banco de dados inacessível
# - Permissões insuficientes
```

## 📈 Estatísticas

- ✅ **100%** de processamento (antes era 70%)
- ✅ Datas **corretas** do arquivo (antes usava data atual)
- ✅ **Automático** (antes era manual)
- ✅ **0%** CPU ociosa (sistema de eventos)

## 📄 Licença

Este projeto foi desenvolvido para uso interno. Consulte a licença antes de redistribuir.

## 👨‍💻 Autor

Desenvolvido para automatizar o processamento de retornos bancários CBR724.

---

**⚡ Processamento Automático | 📊 Logs Detalhados | 🔒 Seguro**
