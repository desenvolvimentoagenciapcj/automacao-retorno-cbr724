# 🚀 GUIA DE USO - SISTEMA DE AUTOMAÇÃO DE RETORNO BANCÁRIO CBR724

## ✅ SIM! O SISTEMA RECONHECE ARQUIVOS AUTOMATICAMENTE

O monitor funciona em **tempo real** - você não precisa fazer nada manualmente!

---

## 📋 COMO FUNCIONA

### 1️⃣ INICIAR O MONITOR (Uma única vez)

```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
python monitor_arquivos_simples.py
```

**O sistema vai mostrar:**
```
============================================================
🏦 SISTEMA DE AUTOMAÇÃO - RETORNO BANCÁRIO CBR724
============================================================
📁 Monitorando: D:\Teste_Cobrança_Acess\Retorno
💾 Banco Baixa: D:/Teste_Cobrança_Acess/dbBaixa2025.accdb
💾 Banco Cobrança: D:/Teste_Cobrança_Acess/Cobranca2019.accdb
📝 Logs: logs
============================================================

✅ Monitor iniciado e aguardando novos arquivos...
⏹️  Pressione Ctrl+C para parar.
```

### 2️⃣ O QUE ACONTECE AUTOMATICAMENTE

Quando um arquivo **CBR724*.ret** chega em **D:\Teste_Cobrança_Acess\Retorno**:

1. 🔍 **Detecção Automática** - Sistema detecta o arquivo imediatamente
2. 📦 **Backup Automático** - Cria backup de dbBaixa2025 e Cobranca2019
3. 📄 **Processamento CBR724** - Lê arquivo de 160 caracteres por linha
4. 💾 **Atualização Access** - Atualiza pcjTITULOS com as baixas
5. 📊 **Relatório** - Mostra quantas baixas foram feitas
6. ✅ **Finalização** - Move arquivo para D:\Teste_Cobrança_Acess\Retorno\Processados
7. 🔄 **Continua** - Volta a aguardar o próximo arquivo

### 3️⃣ EXEMPLO DE PROCESSAMENTO AUTOMÁTICO

```
============================================================
🔄 PROCESSANDO: CBR7246250110202521616_id.ret
============================================================
📦 Criando backup dos bancos...
✓ Backup dbBaixa2025: D:\Teste_Cobrança_Acess\Backup\backup_20251007_094640_dbBaixa2025.accdb
✓ Backup Cobranca2019: D:\Teste_Cobrança_Acess\Backup\backup_20251007_094640_Cobranca2019.accdb

📄 Processando arquivo CBR724 (160 caracteres)...
✅ 10 registros encontrados

💾 Integrando com banco Access...
✓ Conectado ao dbBaixa2025.accdb
✓ Conectado ao Cobranca2019.accdb
✓ Baixa processada: 0000008952 - Valor: R$ 150.00
✓ Baixa processada: 0000008953 - Valor: R$ 200.00
✓ Transação commitada. Processados: 10, Baixas: 2

============================================================
✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!
============================================================
📊 Registros processados: 10
💰 Baixas realizadas: 2
🔄 Atualizações: 0
============================================================

✅ Monitor iniciado e aguardando novos arquivos...
```

---

## 🎯 USO NO DIA A DIA

### VOCÊ SÓ PRECISA:

1. ✅ **Deixar o monitor rodando** (pode minimizar a janela)
2. ✅ **Colocar arquivos CBR724*.ret** em `D:\Teste_Cobrança_Acess\Retorno`
3. ✅ **Pronto!** O resto é automático

### NÃO PRECISA:

- ❌ Clicar em nada
- ❌ Executar comandos manualmente
- ❌ Abrir o Access
- ❌ Importar manualmente

---

## 📁 ESTRUTURA DE PASTAS

```
D:\Teste_Cobrança_Acess\
├── Retorno\              ← COLOQUE OS ARQUIVOS CBR724*.ret AQUI (monitorada)
│   ├── Processados\      ← Arquivos já processados vão para cá
│   └── Erro\             ← Arquivos com erro vão para cá
├── Backup\               ← Backups dos bancos Access ficam aqui
└── AutomacaoRetorno\
    └── logs\             ← Logs detalhados do sistema
```

---

## 🔧 BANCOS DE DADOS UTILIZADOS

- **dbBaixa2025.accdb** - Onde os retornos são importados
  - Tabela: **pcjTITULOS** (253.649 registros)
  - Campos atualizados: DT_PGTO_TIT, VL_PGTO_TIT, DT_LIB_CRED, CodMovimento
  
- **Cobranca2019.accdb** - Dados de cobrança (referência)
  - Tabela: **pcjCOBRANCA** (5.409 registros)

## 📄 FORMATO CBR724

- **160 caracteres por linha**
- Tipo 7 = Registros de títulos
- Nosso Número nas posições 21-30
- Sistema processa automaticamente CBR724 e CNAB240

---

## 📊 LOGS

Todos os processamentos são registrados em:
- **Arquivo de log**: `D:\Teste_Cobrança_Acess\AutomacaoRetorno\logs\retorno_AAAAMMDD.log`
- **Console**: Você vê tudo acontecendo em tempo real na tela

---

## ⚙️ CONFIGURAÇÃO

O arquivo `config.yaml` controla todas as configurações:
- Pastas monitoradas
- Caminhos dos bancos Access
- Nível de log (INFO, DEBUG, etc.)

---

## ❓ DÚVIDAS FREQUENTES

### O monitor precisa ficar rodando o tempo todo?
**SIM!** Enquanto o monitor estiver ativo, ele detecta arquivos automaticamente.
Se você fechar, precisa iniciar novamente.

### E se eu fechar o terminal?
O monitor para. Para usar no dia a dia, deixe o terminal minimizado.

### Posso processar vários arquivos de uma vez?
**SIM!** Copie quantos quiser para `D:\Teste_Cobrança_Acess\Retorno` que o sistema
processa todos, um por vez.

### E se der erro?
- Arquivo com erro vai para `D:\Teste_Cobrança_Acess\Retorno\Erro`
- Veja os detalhes no log
- O monitor continua funcionando

### Preciso fazer backup manual?
**NÃO!** O sistema cria backup automático dos 2 bancos Access antes de cada
processamento em `D:\Teste_Cobrança_Acess\Backup`.

---

## 🆘 SUPORTE

**Problema**: Monitor não inicia
**Solução**: Verifique se está no diretório correto:
```powershell
cd D:\Teste_Cobrança_Acess\AutomacaoRetorno
python monitor_arquivos_simples.py
```

**Problema**: Arquivo não é processado
**Solução**: 
1. Verifique se o monitor está rodando
2. Verifique se o arquivo começa com CBR724 (ex: CBR7246250110202521616_id.ret)
3. Verifique se o arquivo está em `D:\Teste_Cobrança_Acess\Retorno`
4. Veja o log em `logs/` para detalhes

---

## 🎉 RESUMO

**TUDO QUE VOCÊ FAZ:**
1. Inicia o monitor uma vez
2. Coloca arquivos CBR724*.ret na pasta Retorno

**TUDO QUE O SISTEMA FAZ AUTOMATICAMENTE:**
1. Detecta arquivos CBR724
2. Faz backup dos 2 bancos Access
3. Processa formato CBR724 (160 chars)
4. Atualiza pcjTITULOS no dbBaixa2025
5. Move para Processados
6. Aguarda próximo arquivo

**É ISSO! SIMPLES E AUTOMÁTICO! 🚀**
