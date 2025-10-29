# 📦 Backup OneDrive - Guia de Uso

**Data:** 29 de outubro de 2025  
**Versão:** 2.1  
**Objetivo:** Fazer backup de toda a automação com as últimas alterações

---

## 🎯 Resumo

O script `BACKUP_ONEDRIVE.bat` copia todos os arquivos importantes da automação para o OneDrive.

---

## 📍 Caminhos Configurados

### OneDrive
```
F:\OneDrive - Fundacao Agencia das Bacias PCJ\Repositorio_TI\Manuais\SCPCJ\AutomaçãoDbBaixa
```

### Pasta Local de Trabalho
```
D:\Teste_Cobrança_Acess\AutomaçãoDbBaixa
```

---

## 🚀 Como Usar

### Opção 1: Executar o BAT (Recomendado)
```batch
BACKUP_ONEDRIVE.bat
```

Isto vai:
- Criar pasta com timestamp (ex: `Backup_20251029_0906`)
- Copiar todos os scripts Python
- Copiar todos os scripts BAT
- Copiar scripts PowerShell
- Copiar configurações
- Copiar documentação
- Criar arquivo ZIP automático
- Exibir resumo

### Opção 2: Automático (ao salvar)
O sistema pode ser configurado para fazer backup automático.

---

## 📋 O que é Copiado

| Item | Localização | Arquivos |
|------|-----------|----------|
| Scripts Python | `Scripts/python/` | 7 arquivos (.py) |
| Scripts BAT | `Scripts/bat/` | ~10 arquivos |
| PowerShell | `Scripts/powershell/` | ~5 arquivos |
| Configuração | `config/` | 2 arquivos |
| Documentação | `docs/` e raiz | 15+ arquivos (.md e .txt) |
| Atalhos | Raiz | *.bat principais |

---

## 📝 Estrutura do Backup

```
Backup_20251029_0906/
├── Scripts/
│   ├── python/          ← Código Python
│   ├── bat/             ← Scripts em lote
│   └── powershell/      ← PowerShell
├── config/
│   ├── config.ini.backup
│   └── requirements.txt
├── docs/                ← Documentação
├── *.bat                ← Atalhos principais
├── README.md
└── INFO_BACKUP.md       ← Informações do backup
```

---

## 🔍 Verificação da Integridade

Após o backup, verificar:

✅ Pasta criada no OneDrive  
✅ Arquivos copiados  
✅ ZIP gerado  
✅ INFO_BACKUP.md criado  

---

## 🌳 Git (Se Aplicável)

Para versionamento com Git:

```powershell
# Ver status
git status

# Adicionar tudo
git add .

# Fazer commit
git commit -m "v2.1: Notificacao de arquivo faltante para Aline e Lilian"

# Push
git push origin main
```

---

## 📊 Versão Atual

```
Versão: 2.1
Data: 29/10/2025
Alterações:
  - ✅ Notificação de arquivo faltante
  - ✅ Emails adicionais (Aline + Lilian)
  - ✅ Correcção RFC 5322
  - ✅ Melhoria em _criar_mensagem()
```

---

## ⚠️ Importante

- ✅ Backup NÃO sobrescreve (cria pasta com timestamp)
- ✅ Arquivo ZIP é automático
- ✅ INFO_BACKUP.md documentar alterações
- ⚠️ Verificar espaço em disco antes

---

## 🆘 Solução de Problemas

**Problema:** Caminho OneDrive não encontrado
- **Solução:** O script pedirá novo caminho

**Problema:** Erro ao criar ZIP
- **Solução:** Requer PowerShell 5.0+ ou WinRAR

**Problema:** Permissão negada
- **Solução:** Executar como administrador

---

## ✅ Checklist Pós-Backup

- [ ] Pasta criada no OneDrive
- [ ] ZIP gerado com sucesso
- [ ] INFO_BACKUP.md preenchido
- [ ] Todos os scripts copiados
- [ ] Config.ini.backup criado
- [ ] Documentação completa

---

**Backup está pronto para usar!** 🎉

