from processador_cbr724 import ProcessadorCBR724
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

p = ProcessadorCBR724()
registros = p.processar_arquivo(r'D:\Teste_Cobrança_Acess\Retorno\CBR7246250110202521616_id.ret')

print(f"\n✅ Total de registros: {len(registros)}")
if registros:
    print(f"📅 Data extraída do arquivo: {registros[0]['data_ocorrencia'].strftime('%d/%m/%Y')}")
    print(f"🔢 Primeiro título: {registros[0]['nosso_numero']}")
    print(f"💰 Valor: R$ {registros[0]['valor_pago']:,.2f}")
