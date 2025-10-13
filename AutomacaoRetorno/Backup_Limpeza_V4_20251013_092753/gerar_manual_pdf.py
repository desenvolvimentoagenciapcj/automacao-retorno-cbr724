"""
Gerador de Manual em PDF
Converte a documentação Markdown em PDF profissional
"""

import os
from pathlib import Path
from datetime import datetime

# Verificar se as bibliotecas necessárias estão instaladas
try:
    import markdown
    MARKDOWN_DISPONIVEL = True
except ImportError:
    MARKDOWN_DISPONIVEL = False
    print("⚠️ Biblioteca 'markdown' não instalada. Execute: pip install markdown")

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_DISPONIVEL = True
except ImportError:
    WEASYPRINT_DISPONIVEL = False
    print("⚠️ Biblioteca 'weasyprint' não instalada. Execute: pip install weasyprint")


def criar_html_profissional(conteudo_md, titulo="Manual de Implantação"):
    """Cria HTML estilizado a partir do Markdown"""
    
    # Converter Markdown para HTML
    html_content = markdown.markdown(
        conteudo_md,
        extensions=['tables', 'fenced_code', 'toc', 'codehilite']
    )
    
    # Template HTML com estilos CSS profissionais
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-right {{
                content: "Página " counter(page) " de " counter(pages);
                font-size: 10pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: #0066cc;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 10px;
            margin-top: 30px;
            page-break-before: always;
        }}
        
        h1:first-of-type {{
            page-break-before: avoid;
            font-size: 32pt;
            text-align: center;
            border: none;
            margin-top: 100px;
        }}
        
        h2 {{
            color: #0088cc;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 5px;
            margin-top: 25px;
        }}
        
        h3 {{
            color: #00aacc;
            margin-top: 20px;
        }}
        
        h4 {{
            color: #555;
            margin-top: 15px;
        }}
        
        code {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 90%;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 4px solid #0066cc;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: none;
            border: none;
            padding: 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #0066cc;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        blockquote {{
            border-left: 4px solid #0066cc;
            margin-left: 0;
            padding-left: 20px;
            color: #666;
            font-style: italic;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        .capa {{
            text-align: center;
            page-break-after: always;
            padding-top: 200px;
        }}
        
        .capa h1 {{
            font-size: 36pt;
            color: #0066cc;
            margin-bottom: 20px;
            border: none;
            margin-top: 0;
        }}
        
        .capa p {{
            font-size: 14pt;
            color: #666;
            margin: 10px 0;
        }}
        
        .info-box {{
            background-color: #e8f4fd;
            border-left: 4px solid #0066cc;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .warning-box {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .success-box {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            page-break-after: always;
        }}
        
        .toc h2 {{
            margin-top: 0;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 10pt;
        }}
    </style>
</head>
<body>
    <div class="capa">
        <h1>📘 {titulo}</h1>
        <p><strong>Sistema de Automação de Retornos CBR724</strong></p>
        <p>Fundação Agência das Bacias PCJ</p>
        <p>Versão 1.0 - {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    
    {html_content}
    
    <div class="footer">
        <p>© {datetime.now().year} Fundação Agência das Bacias PCJ - TI</p>
        <p>Este documento é propriedade da Fundação Agência das Bacias PCJ</p>
    </div>
</body>
</html>
"""
    
    return html_template


def gerar_pdf_do_markdown(arquivo_md, arquivo_pdf_saida):
    """Gera PDF a partir de arquivo Markdown"""
    
    if not MARKDOWN_DISPONIVEL or not WEASYPRINT_DISPONIVEL:
        print("\n❌ Bibliotecas necessárias não instaladas!")
        print("\n📦 Execute:")
        print("   pip install markdown weasyprint")
        return False
    
    try:
        # Ler arquivo Markdown
        print(f"\n📖 Lendo arquivo: {arquivo_md}")
        with open(arquivo_md, 'r', encoding='utf-8') as f:
            conteudo_md = f.read()
        
        # Criar HTML
        print("🔄 Convertendo Markdown para HTML...")
        titulo = Path(arquivo_md).stem.replace('_', ' ').title()
        html_content = criar_html_profissional(conteudo_md, titulo)
        
        # Gerar PDF
        print("📄 Gerando PDF...")
        HTML(string=html_content).write_pdf(arquivo_pdf_saida)
        
        print(f"\n✅ PDF gerado com sucesso!")
        print(f"📁 Local: {arquivo_pdf_saida}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao gerar PDF: {e}")
        return False


def gerar_todos_manuais():
    """Gera PDFs de todos os arquivos Markdown de documentação"""
    
    script_dir = Path(__file__).parent
    
    # Lista de arquivos para converter
    arquivos_para_converter = [
        'MANUAL_IMPLANTACAO_COMPLETO.md',
        'GUIA_CONFIG.md',
        'SISTEMA_EM_PRODUCAO.md',
        'NOTIFICACOES_WINDOWS.md',
        'SISTEMA_WATCHDOG.md',
    ]
    
    print("\n" + "="*70)
    print("         📘 GERADOR DE MANUAIS EM PDF")
    print("="*70)
    
    # Criar pasta para PDFs
    pasta_pdfs = script_dir / "Manuais_PDF"
    pasta_pdfs.mkdir(exist_ok=True)
    
    print(f"\n📁 Pasta de saída: {pasta_pdfs}\n")
    
    sucesso = 0
    falhas = 0
    
    for arquivo_md in arquivos_para_converter:
        caminho_md = script_dir / arquivo_md
        
        if not caminho_md.exists():
            print(f"⏭️  Pulando: {arquivo_md} (não encontrado)")
            continue
        
        # Nome do PDF de saída
        nome_pdf = arquivo_md.replace('.md', '.pdf')
        caminho_pdf = pasta_pdfs / nome_pdf
        
        print(f"\n📄 Processando: {arquivo_md}")
        
        if gerar_pdf_do_markdown(caminho_md, caminho_pdf):
            sucesso += 1
        else:
            falhas += 1
    
    # Resumo
    print("\n" + "="*70)
    print(f"✅ Arquivos convertidos: {sucesso}")
    if falhas > 0:
        print(f"❌ Falhas: {falhas}")
    print("="*70 + "\n")


if __name__ == "__main__":
    gerar_todos_manuais()
