# ⚠️ COMPORTAMENTO DO MONITOR - IMPORTANTE

**Data:** 13/10/2025  
**Versão:** 2.1

---

## 🎯 COMPORTAMENTO PADRÃO

O monitor utiliza a biblioteca **watchdog** do Python, que funciona assim:

### ✅ O que o monitor FAZ:
- ✅ Detecta arquivos **NOVOS** criados/copiados **APÓS** ele iniciar
- ✅ Processa automaticamente esses novos arquivos
- ✅ Deleta automaticamente arquivos IEDCBR novos
- ✅ Move arquivos processados para `Retorno\Processados\`

### ❌ O que o monitor NÃO FAZ:
- ❌ **NÃO** detecta arquivos que **JÁ ESTAVAM** na pasta antes dele iniciar
- ❌ **NÃO** faz varredura inicial da pasta
- ❌ **NÃO** processa arquivos antigos automaticamente

---

## 🔍 CENÁRIO PROBLEMA

### Situação:
1. Você **para** o monitor (PARAR_MONITOR.bat)
2. Enquanto parado, **chegam** 3 arquivos .ret na pasta
3. Você **inicia** o monitor novamente (INICIAR_MONITOR_OCULTO.bat)
4. O monitor **ignora** os 3 arquivos que já estavam lá! ❌

### Por quê?
O watchdog só "vê" arquivos criados **depois** que ele começa a monitorar.

---

## ✅ SOLUÇÃO

### Para processar arquivos existentes:

Execute o script:
```batch
PROCESSAR_EXISTENTES.bat
```

**O que ele faz:**
1. 🗑️ **Deleta** todos os arquivos IEDCBR da pasta
2. 📋 **Lista** todos os arquivos CBR724
3. 🔄 **Move temporariamente** para outra pasta
4. ⏱️ **Aguarda** 3 segundos
5. 🔙 **Move de volta** para a pasta original
6. ✨ O monitor detecta como "novos" e processa!

---

## 📋 QUANDO USAR

### ✅ Use `PROCESSAR_EXISTENTES.bat` quando:

1. **Reiniciar o monitor**
   - Parou e iniciou novamente
   - Arquivos ficaram na pasta durante o downtime

2. **Após manutenção**
   - Atualizou o sistema
   - Fez alterações nos scripts

3. **Monitor travou/caiu**
   - Sistema foi reiniciado
   - Houve queda de energia

4. **Dúvida se há arquivos pendentes**
   - Execute e confirme que tudo foi processado

### ❌ NÃO precisa usar quando:

- Monitor está rodando normalmente 24/7
- Nenhuma interrupção ocorreu
- Arquivos chegam em tempo real

---

## 🚀 WORKFLOW RECOMENDADO

### Cenário 1: Início do Dia
```batch
1. INICIAR_MONITOR_OCULTO.bat
2. PROCESSAR_EXISTENTES.bat    ← Processa pendências
3. STATUS_MONITOR.bat           ← Confirma que está OK
```

### Cenário 2: Após Manutenção
```batch
1. PARAR_MONITOR.bat
2. [Fazer alterações necessárias]
3. INICIAR_MONITOR_OCULTO.bat
4. PROCESSAR_EXISTENTES.bat    ← Importante!
5. STATUS_MONITOR.bat
```

### Cenário 3: Operação Normal
```batch
# Monitor roda 24/7, sem interrupções
# Arquivos são processados automaticamente
# Nada a fazer! ✅
```

---

## 📊 EXEMPLO REAL (13/10/2025)

### Situação detectada:
```
Pasta Retorno:
  - CBR72462641010202521737_id.ret (aguardando)
  - IEDCBR62631010202520834.ret (aguardando)
  - IEDCBR7441010202521006.ret (aguardando)

Monitor: ✅ Rodando (PID 47188)
Problema: Arquivos ignorados
```

### Solução aplicada:
```powershell
PS> .\PROCESSAR_EXISTENTES.bat

Resultado:
  ✅ Deletados: 2 arquivos IEDCBR
  ✅ Processado: 1 arquivo CBR724
  ✅ Pasta Retorno: VAZIA
```

---

## 🔧 ALTERNATIVA TÉCNICA

Se preferir fazer manualmente:

### PowerShell:
```powershell
# 1. Deletar IEDCBRs
Remove-Item "\\SERVIDOR1\CobrancaPCJ\Retorno\IEDCBR*.ret" -Force

# 2. Mover CBR724 temporariamente
$temp = "\\SERVIDOR1\CobrancaPCJ\RetornoTemp"
Move-Item "\\SERVIDOR1\CobrancaPCJ\Retorno\CBR*.ret" -Destination $temp

# 3. Aguardar
Start-Sleep -Seconds 3

# 4. Mover de volta (monitor detecta como novo)
Move-Item "$temp\CBR*.ret" -Destination "\\SERVIDOR1\CobrancaPCJ\Retorno"
```

---

## ⚙️ OPÇÕES FUTURAS

### Se quiser que o monitor processe arquivos existentes:

Seria necessário modificar `monitor_retornos.py` para:
1. Fazer varredura inicial da pasta ao iniciar
2. Processar arquivos encontrados
3. Depois começar a monitorar novos

**Prós:** Processamento automático  
**Contras:** Pode reprocessar arquivos indesejados

**Decisão atual:** Manter comportamento atual (mais seguro) e usar `PROCESSAR_EXISTENTES.bat` quando necessário.

---

## 📚 SCRIPTS RELACIONADOS

| Script | Função |
|--------|--------|
| `INICIAR_MONITOR_OCULTO.bat` | Inicia monitor em segundo plano |
| `PARAR_MONITOR.bat` | Para todos os monitores |
| `STATUS_MONITOR.bat` | Verifica status do monitor |
| `PROCESSAR_EXISTENTES.bat` | **Processa arquivos existentes** ⭐ |

---

## 💡 DICAS

### Como saber se há arquivos pendentes?

Execute:
```powershell
Get-ChildItem "\\SERVIDOR1\CobrancaPCJ\Retorno\*.ret"
```

Se retornar arquivos, execute `PROCESSAR_EXISTENTES.bat`.

### Como garantir que tudo foi processado?

1. Execute `PROCESSAR_EXISTENTES.bat`
2. Aguarde 30 segundos
3. Verifique novamente:
   ```powershell
   Get-ChildItem "\\SERVIDOR1\CobrancaPCJ\Retorno\*.ret"
   ```
4. Deve estar vazio! ✅

---

## 🆘 TROUBLESHOOTING

### Problema: PROCESSAR_EXISTENTES não funciona

**Verificar:**
1. Monitor está rodando? (`STATUS_MONITOR.bat`)
2. Acesso à rede OK? (testar caminho `\\SERVIDOR1`)
3. Permissões de escrita na pasta?

### Problema: Arquivos continuam na pasta

**Possíveis causas:**
1. Monitor travou (reinicie com PARAR + INICIAR)
2. Erro no processamento (verifique `monitor_retornos.log`)
3. Arquivo corrompido (mova manualmente para pasta Erro)

---

**✅ Lembre-se: `PROCESSAR_EXISTENTES.bat` é seu amigo após reiniciar o monitor!**

---

**Criado por:** GitHub Copilot  
**Data:** 13/10/2025  
**Versão do Sistema:** 2.1
