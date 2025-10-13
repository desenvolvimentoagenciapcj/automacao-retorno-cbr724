# 🧹 Guia de Limpeza para Produção

## Arquivos que DEVEM PERMANECER (Essenciais)

### 📌 Núcleo do Sistema
- ✅ `processador_cbr724.py` - Processa arquivos CBR724
- ✅ `processador_cnab.py` - Processa arquivos CNAB240
- ✅ `integrador_access.py` - Integra com banco Access
- ✅ `processar_todos_arquivos.py` - Processamento em lote
- ✅ `monitor_arquivos_simples.py` - Monitor automático
- ✅ `config.yaml` - Configurações do sistema
- ✅ `requirements.txt` - Dependências Python

### 📌 Documentação
- ✅ `README.md` ou `README_SISTEMA.md` - Manual do sistema
- ✅ `COMO_USAR.md` - Instruções de uso

### 📌 Utilitários
- ✅ `verificar_sistema.py` - Verificação automática (NOVO)
- ✅ `notificador.py` - Notificações de processamento (se usado)
- ✅ `relatorio_processamento.py` - Relatórios (se usado)

---

## ❌ Arquivos que PODEM SER APAGADOS (Testes/Debug)

### 🗑️ Scripts de Teste
```
analisar_cbr724_real.py
analisar_layout_real.py
analisar_todas_linhas.py
analise_manual_cbr724.py
buscar_id_880.py
buscar_nosso_880.py
buscar_por_id_pcj.py
buscar_titulos_1227.py
buscar_titulos_cbr724.py
consultar_titulos.py
debug_arquivo.py
debug_parser.py
descobrir_vba_layout.py
diagnostico_manual_vs_automatico.py
explicar_cd_sac.py
explicar_cd_sac_simples.py
investigar_2500003711.py
layout_cbr724_correto.py
listar_titulos.py
testar.py
testar_arquivo_unico.py
testar_extracao_vba.py
testar_processamento_880.py
testar_simples.py
teste_apagar_iedcbr.py
teste_conexao.py
verificar_880_simples.py
verificar_atualizacao_880.py
verificar_banco_detalhado.py
verificar_datas_banco.py
verificar_estrutura_bancos.py
verificar_importacao.py
verificar_tipo_documento.py
verificar_titulos_1227_final.py
verificar_titulos_posicao11_21.py
verificar_titulos_processados.py
verificar_titulo_880.py
verificar_vinculo_bancos.py
```

### 🗑️ Arquivos de Desenvolvimento/Backup
```
corrigir_integrador.py
corrigir_links_access.py
criar_integrador_vba.py
extrair_vba.py
extrair_vba_correto.py
integrador_access.py.backup
integrador_access_broken.py
integrador_access_OLD.py
integrador_access_temp.py
integrador_vba_logic.py
processar_um_arquivo.py
resumo_correcao_vba.py
vba_novo_importa_arquivo_retorno.vb
```

### 🗑️ Instaladores/Setup (já instalado)
```
instalar.py
instalar_simples.py
desabilitar_startup.vbs
```

### 🗑️ Dashboards/Relatórios Experimentais
```
dashboard.py (a menos que esteja usando)
relatorio_final.py (a menos que esteja usando)
```

---

## 📁 Estrutura Final para Produção

```
D:\Teste_Cobrança_Acess\
│
├── dbBaixa2025.accdb          ← Banco principal
├── Cobranca2019.accdb         ← Banco secundário (se usado)
│
├── Retorno\                   ← Pasta de entrada
│   ├── Processados\           ← Arquivos processados
│   └── Erro\                  ← Arquivos com erro
│
├── Backup\                    ← Backups automáticos
│
└── AutomacaoRetorno\          ← Sistema
    ├── processador_cbr724.py
    ├── processador_cnab.py
    ├── integrador_access.py
    ├── processar_todos_arquivos.py
    ├── monitor_arquivos_simples.py
    ├── verificar_sistema.py    ← NOVO
    ├── config.yaml
    ├── requirements.txt
    ├── README.md
    ├── COMO_USAR.md
    └── logs\                  ← Logs do sistema
```

---

## 🚀 Script de Limpeza Automática

Execute este comando no PowerShell para limpar automaticamente:

```powershell
# Ir para pasta do sistema
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"

# Criar pasta temporária para arquivos removidos (segurança)
New-Item -ItemType Directory -Path "..\Arquivos_Removidos" -Force

# Mover arquivos de teste/debug
$arquivos_remover = @(
    "analisar_*.py",
    "buscar_*.py",
    "consultar_*.py",
    "debug_*.py",
    "descobrir_*.py",
    "diagnostico_*.py",
    "explicar_*.py",
    "investigar_*.py",
    "layout_*.py",
    "listar_*.py",
    "testar*.py",
    "teste_*.py",
    "verificar_*.py",
    "corrigir_*.py",
    "criar_*.py",
    "extrair_*.py",
    "*_backup.py",
    "*_broken.py",
    "*_OLD.py",
    "*_temp.py",
    "processar_um_arquivo.py",
    "resumo_*.py",
    "instalar*.py",
    "*.vb",
    "*.vbs"
)

foreach ($pattern in $arquivos_remover) {
    Get-ChildItem -Path . -Filter $pattern | Move-Item -Destination "..\Arquivos_Removidos\" -Force
}

Write-Host "`n✅ Limpeza concluída! Arquivos movidos para pasta 'Arquivos_Removidos'" -ForegroundColor Green
Write-Host "   Se tudo funcionar bem, você pode apagar essa pasta depois.`n" -ForegroundColor Yellow
```

---

## ✅ Checklist Pós-Limpeza

Após limpar, execute a verificação automática:

```powershell
python verificar_sistema.py
```

O sistema vai verificar:
- ✓ Estrutura de pastas
- ✓ Arquivos essenciais
- ✓ Bancos Access
- ✓ Configurações
- ✓ Dependências Python
- ✓ Sistema de backup

---

## 🔄 Verificação Periódica (Recomendado)

### Criar tarefa agendada para verificar o sistema toda segunda-feira:

```powershell
# Criar script de verificação agendada
$script = @"
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
python verificar_sistema.py > "..\logs\verificacao_sistema.log"
"@

$script | Out-File "D:\Teste_Cobrança_Acess\verificar_automatico.bat" -Encoding ASCII

# Criar tarefa agendada (executar como Administrador)
$action = New-ScheduledTaskAction -Execute "D:\Teste_Cobrança_Acess\verificar_automatico.bat"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8am
Register-ScheduledTask -TaskName "Verificação Sistema Cobrança" -Action $action -Trigger $trigger
```

---

## 📞 Suporte

Em caso de dúvidas sobre o que apagar:
1. Execute `verificar_sistema.py` ANTES de apagar
2. Mova para pasta temporária (não apague diretamente)
3. Teste por 1 semana
4. Se tudo OK, apague a pasta temporária

**⚠️ IMPORTANTE:** Sempre faça backup do banco Access antes de qualquer mudança!
