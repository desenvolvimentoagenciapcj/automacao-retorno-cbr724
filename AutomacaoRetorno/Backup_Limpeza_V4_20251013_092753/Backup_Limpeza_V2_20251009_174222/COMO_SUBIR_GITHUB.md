# 🚀 GUIA: Como Subir o Projeto no GitHub

## 📋 Pré-requisitos

1. **Conta no GitHub** - https://github.com/signup
2. **Git instalado** - https://git-scm.com/download/win

## 🔧 Passo a Passo

### 1️⃣ Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `automacao-retorno-cbr724` (ou o nome que preferir)
   - **Description**: "Sistema automático de processamento de retornos bancários CBR724"
   - **Visibilidade**: 
     - ✅ **Private** (RECOMENDADO - código financeiro sensível)
     - ⚠️ Public (apenas se for compartilhar publicamente)
   - **NÃO marque** "Add a README file" (já temos um)
3. Clique em **"Create repository"**

### 2️⃣ Configurar Git Local

Abra o PowerShell nesta pasta e execute:

```powershell
# Navegar para a pasta do projeto
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"

# Inicializar repositório Git
git init

# Configurar seu nome e email (primeira vez apenas)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Adicionar todos os arquivos
git add .

# Verificar o que será commitado
git status

# Fazer o primeiro commit
git commit -m "Initial commit - Sistema de automação CBR724"
```

### 3️⃣ Conectar com GitHub

```powershell
# Adicionar o repositório remoto (SUBSTITUA 'seu-usuario' pelo seu usuário do GitHub)
git remote add origin https://github.com/seu-usuario/automacao-retorno-cbr724.git

# Verificar se foi adicionado
git remote -v

# Enviar para o GitHub
git branch -M main
git push -u origin main
```

### 4️⃣ Autenticação

Se pedir login:

**Opção 1 - Personal Access Token (RECOMENDADO)**
1. Acesse: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Marque: `repo` (Full control of private repositories)
4. Copie o token gerado
5. Use como senha quando o Git pedir

**Opção 2 - GitHub CLI**
```powershell
# Instalar GitHub CLI
winget install GitHub.cli

# Fazer login
gh auth login
```

### 5️⃣ Verificar

Acesse seu repositório no GitHub e confirme que os arquivos foram enviados!

## 📁 O que vai ser enviado?

✅ **SIM:**
- `monitor_retornos.py`
- `processador_cbr724.py`
- `integrador_access.py`
- `INICIAR_MONITOR.bat`
- `requirements.txt`
- `README.md`
- `GUIA_RAPIDO.txt`
- `LEIA-ME.txt`

❌ **NÃO** (protegido pelo .gitignore):
- Bancos Access (`.accdb`)
- Arquivos de retorno (`.ret`)
- Logs (`*.log`)
- Backups
- Dados sensíveis

## 🔄 Comandos Úteis (Para Futuras Atualizações)

```powershell
# Ver status das mudanças
git status

# Adicionar arquivos modificados
git add .

# Fazer commit das mudanças
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push

# Baixar mudanças do GitHub
git pull

# Ver histórico
git log --oneline
```

## 🔒 Segurança

⚠️ **IMPORTANTE - Antes de enviar, VERIFIQUE:**

```powershell
# Ver o que será enviado
git status

# Se algo sensível aparecer, adicione ao .gitignore:
echo "arquivo_sensivel.accdb" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

## 🆘 Problemas Comuns

### "fatal: not a git repository"
```powershell
# Certifique-se de estar na pasta correta
cd "D:\Teste_Cobrança_Acess\AutomacaoRetorno"
git init
```

### "Permission denied"
```powershell
# Use Personal Access Token como senha
# Ou configure SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### "rejected (non-fast-forward)"
```powershell
# Se o repositório remoto tem conteúdo que você não tem localmente:
git pull origin main --allow-unrelated-histories
git push
```

### Remover arquivo sensível já commitado
```powershell
# CUIDADO - reescreve histórico
git rm --cached arquivo_sensivel.accdb
git commit -m "Remove arquivo sensível"
git push --force
```

## 📚 Recursos

- **Documentação Git**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **GitHub Desktop** (interface gráfica): https://desktop.github.com/

---

**Pronto! Seu projeto estará no GitHub! 🎉**
