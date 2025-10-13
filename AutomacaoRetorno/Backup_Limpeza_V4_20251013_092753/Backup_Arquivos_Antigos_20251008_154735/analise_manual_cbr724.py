#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise do formato CBR724 baseado no arquivo real
"""

# Linha real do arquivo processado:
# ' 7 24778829000008952 000008952    411 - IOCHPE-MAXION S/A      31102025       0216 RG            13.299,07'

print("=== ANÁLISE DE LAYOUT CBR724 ===\n")
print("Linha exemplo (160 caracteres):")
linha = ' 7 24778829000008952 000008952    411 - IOCHPE-MAXION S/A      31102025       0216 RG            13.299,07                         5,19*           0,00'

print(f"Tamanho: {len(linha)} caracteres\n")

# Análise de posições
print("Análise de campos:")
print(f"[0:3]   Tipo registro: '{linha[0:3]}' = ' 7'")
print(f"[3:20]  Código/CNPJ:   '{linha[3:20]}' = '24778829000008952'")
print(f"[21:31] Nosso Número:  '{linha[21:31]}' = '000008952 '")
print(f"[31:64] Nome/Dados:    '{linha[31:64]}' = '   411 - IOCHPE-MAXION S/A      3'")
print(f"[64:73] Data:          '{linha[64:73]}' = '1102025  '")

print("\n=== HIPÓTESE ===")
print("O código [3:20] parece ser: CNPJ (8 dígitos) + Nosso Número (9 dígitos)")
print("CNPJ: '24778829'")
print("Nosso Número completo: '000008952'")

print("\n=== PROBLEMA IDENTIFICADO ===")
print("O Nosso Número no arquivo: '000008952'")
print("Precisa encontrar no banco como: '9900088952' ou similar")
print("\nO arquivo tem apenas os ÚLTIMOS 9 dígitos do Nosso Número!")
print("O banco tem o número COMPLETO com prefixo (ex: 99...)")

print("\n=== SOLUÇÃO PROPOSTA ===")
print("1. Extrair Nosso Número da posição [21:31] = '000008952'")
print("2. Remover zeros à esquerda = '8952'")
print("3. Buscar no banco com LIKE '%8952' ou RIGHT(NR_NNR_TIT, 4) = '8952'")
print("4. Ou buscar padrões conhecidos: '99%8952' ou similar")
