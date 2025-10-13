#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o integrador_access_broken.py
Remove duplicatas e código quebrado, mantém apenas o que funciona
"""

# Ler arquivo broken
with open('integrador_access_broken.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📄 Arquivo original: {len(lines)} linhas")

# Estratégia:
# 1. Manter linhas 1-336 (até antes do _buscar_titulo quebrado)
# 2. Pular linhas 337-433 (métodos quebrados/duplicados)
# 3. Manter linhas 434-fim (métodos bons: _buscar_titulo, _processar_cancelamento, _processar_baixa, etc)

parte1 = lines[0:336]  # Início até antes do quebrado
parte2 = lines[433:]   # Do _buscar_titulo bom até o fim

novo_arquivo = parte1 + parte2

print(f"✂️  Removidas {len(lines) - len(novo_arquivo)} linhas (código duplicado/quebrado)")
print(f"✅ Novo arquivo: {len(novo_arquivo)} linhas")

# Salvar
with open('integrador_access.py', 'w', encoding='utf-8') as f:
    f.writelines(novo_arquivo)

print("\n✓ Arquivo integrador_access.py corrigido!")
print("\n📋 Métodos mantidos:")
for i, line in enumerate(novo_arquivo):
    if line.strip().startswith('def _'):
        print(f"  {line.strip()}")
