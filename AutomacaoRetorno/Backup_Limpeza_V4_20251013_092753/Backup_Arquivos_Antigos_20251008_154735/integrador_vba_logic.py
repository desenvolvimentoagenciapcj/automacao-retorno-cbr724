#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LÓGICA VBA COMPLETA - Para ser integrada no integrador_access.py

Este arquivo contém APENAS os métodos novos que implementam a lógica do VBA.
Depois de testar, estes métodos serão copiados para o integrador_access.py

VBA LOGIC:
1. Busca título (Seek)
2. Se NÃO achou (NoMatch):
   - Extrai ID_PCJ do nome
   - Cria título novo (AddNew) para RG/LQ/LC/BX
3. Se achou:
   - RG: IGNORA
   - LQ/LC: ATUALIZA para pago
   - BX: ATUALIZA para cancelado
   - MT: IGNORA
"""

def extrair_id_pcj_do_nome(nome_cliente: str) -> int:
    """
    Extrai ID_PCJ do nome do cliente (primeiros dígitos).
    VBA: Left(Sacado, IdLength) onde IdLength = primeiros dígitos consecutivos
    
    Exemplo: "880 JOSE DA SILVA" -> 880
    """
    if not nome_cliente:
        return None
    
    # VBA: If InStr(1, "0123456789", Left(Sacado, 1)) = 0 Then
    if not nome_cliente[0].isdigit():
        return None
    
    # VBA: For i = 2 To 6... extrai até 6 dígitos
    id_str = ''
    for char in nome_cliente[:6]:
        if char.isdigit():
            id_str += char
        else:
            break
    
    return int(id_str) if id_str else None


# TESTE
if __name__ == '__main__':
    # Testes
    assert extrair_id_pcj_do_nome("880 JOSE DA SILVA") == 880
    assert extrair_id_pcj_do_nome("12345 EMPRESA X") == 12345
    assert extrair_id_pcj_do_nome("NOME SEM ID") is None
    assert extrair_id_pcj_do_nome("") is None
    
    print("✅ Todos os testes passaram!")
    print("\nExemplos:")
    print(f"  '880 JOSE' -> {extrair_id_pcj_do_nome('880 JOSE')}")
    print(f"  '12345 EMPRESA' -> {extrair_id_pcj_do_nome('12345 EMPRESA')}")
    print(f"  'NOME SEM' -> {extrair_id_pcj_do_nome('NOME SEM')}")
