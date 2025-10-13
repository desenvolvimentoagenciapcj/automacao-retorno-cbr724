# 🧹 PLANO DE LIMPEZA - VERSÃO ENXUTA

## ❌ ARQUIVOS QUE SERÃO REMOVIDOS (podem ser deletados):

### Arquivos de Teste/Desenvolvimento (não usados em produção):
- `analise_manual_cbr724.py` - análise manual antiga
- `checar_datas.py` - verificação antiga
- `teste_data_arquivo.py` - teste de desenvolvimento
- `verificar_datas_banco.py` - verificação antiga
- `verificar_sistema.py` - verificação antiga
- `monitor_arquivos.py` - versão antiga do monitor
- `monitor_arquivos_simples.py` - versão de teste

### Arquivos Duplicados/Backup:
- `integrador_access.py.backup` - backup desnecessário
- `integrador_vba_logic.py` - versão antiga do integrador

### Processadores Não Utilizados:
- `processador_cnab.py` - formato não usado (só usamos CBR724)
- `processar_todos_arquivos.py` - substituído pelo monitor automático

### Documentação Redundante:
- `COMO_USAR.md` - substituído pelo GUIA_RAPIDO.txt
- `README.md` - substituído pelo README_AUTOMACAO.md
- `README_SISTEMA.md` - informações já no README_AUTOMACAO.md
- `LIMPEZA_PRODUCAO.md` - documento histórico, não necessário

### Configuração Não Usada:
- `config.yaml` - não está sendo usado pelo sistema

### Serviço Windows (opcional - só se NÃO for usar):
- `servico_monitor.py` - só necessário se instalar como serviço
- `INSTALAR_SERVICO.bat` - só necessário se instalar como serviço

---

## ✅ ARQUIVOS ESSENCIAIS (manter obrigatoriamente):

### 🎯 Core do Sistema (3 arquivos Python):
1. **`processador_cbr724.py`** - Processa arquivo CBR724
2. **`integrador_access.py`** - Integra com banco Access
3. **`monitor_retornos.py`** - Monitor automático principal

### 🚀 Execução (1 arquivo):
4. **`INICIAR_MONITOR.bat`** - Inicia o monitor

### 📖 Documentação (1 arquivo):
5. **`GUIA_RAPIDO.txt`** - Guia visual de uso

### 📦 Dependências (1 arquivo):
6. **`requirements.txt`** - Lista de bibliotecas necessárias

---

## 📊 RESUMO DA LIMPEZA:

| Tipo | Antes | Depois | Removidos |
|------|-------|--------|-----------|
| Arquivos Python | 16 | 3 | 13 |
| Documentação | 5 | 1 | 4 |
| Scripts .bat | 3 | 1 | 2 |
| Configuração | 1 | 1 | 0 |
| **TOTAL** | **25** | **6** | **19** |

---

## 🎯 ESTRUTURA FINAL (ENXUTA):

```
AutomacaoRetorno/
│
├── 📄 processador_cbr724.py        # Processa CBR724
├── 📄 integrador_access.py         # Integra com Access
├── 📄 monitor_retornos.py          # Monitor automático
│
├── 🚀 INICIAR_MONITOR.bat          # Inicia o sistema
│
├── 📖 GUIA_RAPIDO.txt              # Como usar
├── 📦 requirements.txt             # Dependências
│
└── 📁 logs/                        # Logs (gerado automaticamente)
    └── monitor_retornos.log
```

**De 25 arquivos para apenas 6 arquivos essenciais!** 🎉

---

## ⚠️ ANTES DE LIMPAR:

1. ✅ Confirme que o monitor está funcionando
2. ✅ Teste com pelo menos 1 arquivo .ret
3. ✅ Verifique que os dados estão corretos no Access
4. ✅ Faça backup se tiver dúvida

---

## 🔥 EXECUTAR LIMPEZA:

Posso criar um script automático que:
1. Move arquivos desnecessários para pasta "Arquivos_Antigos"
2. Mantém apenas os 6 arquivos essenciais
3. Cria backup antes de limpar

**Quer que eu execute a limpeza agora?**
