"""
Gerador de PDFs Profissionais dos Manuais
Usa reportlab para gerar PDFs com formatação profissional
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Diretório dos manuais
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_PDFS = os.path.join(SCRIPT_DIR, "Manuais_PDF")

# Lista de manuais para converter
MANUAIS = [
    "MANUAL_IMPLANTACAO_COMPLETO.md",
    "GUIA_CONFIG.md",
    "SISTEMA_EM_PRODUCAO.md",
    "NOTIFICACOES_WINDOWS.md",
    "SISTEMA_WATCHDOG.md"
]

class PDFHeader(canvas.Canvas):
    """Classe para adicionar cabeçalho e rodapé"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page_num, page in enumerate(self.pages, start=1):
            self.__dict__.update(page)
            self.draw_page_number(page_num, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        self.drawRightString(
            A4[0] - 2*cm,
            1.5*cm,
            f"Página {page_num} de {page_count}"
        )

def converter_markdown_para_paragrafos(conteudo_md, styles):
    """Converte Markdown simples para elementos PDF"""
    elementos = []
    linhas = conteudo_md.split('\n')
    
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if not linha:
            elementos.append(Spacer(1, 0.3*cm))
            i += 1
            continue
        
        # Título H1
        if linha.startswith('# '):
            texto = linha[2:].strip()
            elementos.append(Spacer(1, 0.5*cm))
            elementos.append(Paragraph(texto, styles['Heading1']))
            elementos.append(Spacer(1, 0.3*cm))
        
        # Título H2
        elif linha.startswith('## '):
            texto = linha[3:].strip()
            elementos.append(Spacer(1, 0.4*cm))
            elementos.append(Paragraph(texto, styles['Heading2']))
            elementos.append(Spacer(1, 0.2*cm))
        
        # Título H3
        elif linha.startswith('### '):
            texto = linha[4:].strip()
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(Paragraph(texto, styles['Heading3']))
            elementos.append(Spacer(1, 0.1*cm))
        
        # Linha horizontal
        elif linha.startswith('---') or linha.startswith('==='):
            elementos.append(Spacer(1, 0.2*cm))
            elementos.append(Table([['']], colWidths=[15*cm], rowHeights=[0.05*cm],
                                 style=[('LINEABOVE', (0,0), (-1,-1), 1, colors.grey)]))
            elementos.append(Spacer(1, 0.2*cm))
        
        # Lista com marcador
        elif linha.startswith('- ') or linha.startswith('* '):
            texto = '• ' + linha[2:].strip()
            elementos.append(Paragraph(texto, styles['BodyText']))
        
        # Lista numerada
        elif linha and linha[0].isdigit() and '. ' in linha:
            elementos.append(Paragraph(linha, styles['BodyText']))
        
        # Bloco de código
        elif linha.startswith('```'):
            codigo = []
            i += 1
            while i < len(linhas) and not linhas[i].strip().startswith('```'):
                codigo.append(linhas[i])
                i += 1
            if codigo:
                texto_codigo = '\n'.join(codigo)
                elementos.append(Spacer(1, 0.2*cm))
                elementos.append(Paragraph(
                    f'<pre><font face="Courier" size="9">{texto_codigo}</font></pre>',
                    styles['CustomCode']
                ))
                elementos.append(Spacer(1, 0.2*cm))
        
        # Parágrafo normal
        else:
            # Escapar caracteres especiais XML
            texto = linha.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Processar markdown bold corretamente
            import re
            texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
            texto = re.sub(r'__(.*?)__', r'<b>\1</b>', texto)
            texto = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texto)
            texto = re.sub(r'_(.*?)_', r'<i>\1</i>', texto)
            elementos.append(Paragraph(texto, styles['BodyText']))
        
        i += 1
    
    return elementos

def gerar_capa(doc, titulo, styles):
    """Gera capa profissional"""
    elementos = []
    
    # Espaço superior
    elementos.append(Spacer(1, 4*cm))
    
    # Título principal
    style_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    elementos.append(Paragraph(titulo, style_titulo))
    
    # Subtítulo
    style_subtitulo = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=50
    )
    elementos.append(Paragraph("Sistema de Automação de Retornos Bancários CBR724", style_subtitulo))
    
    # Informações
    elementos.append(Spacer(1, 3*cm))
    
    info_data = [
        ["Organização:", "Fundação Agência das Bacias PCJ"],
        ["Departamento:", "Tecnologia da Informação"],
        ["Data:", datetime.now().strftime("%d/%m/%Y")],
        ["Versão:", "2.0"]
    ]
    
    table = Table(info_data, colWidths=[4*cm, 10*cm])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(table)
    elementos.append(PageBreak())
    
    return elementos

def gerar_pdf_do_manual(arquivo_md, arquivo_pdf):
    """Gera PDF de um manual Markdown"""
    try:
        print(f"  Processando: {arquivo_md}")
        
        # Ler arquivo Markdown
        caminho_md = os.path.join(SCRIPT_DIR, arquivo_md)
        if not os.path.exists(caminho_md):
            print(f"    AVISO: Arquivo não encontrado - {arquivo_md}")
            return False
        
        with open(caminho_md, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Criar documento PDF
        doc = SimpleDocTemplate(
            arquivo_pdf,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Customizar estilos
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        styles.add(ParagraphStyle(
            name='CustomCode',
            parent=styles['Code'],
            fontSize=9,
            leftIndent=20,
            backgroundColor=colors.HexColor('#f5f5f5')
        ))
        
        # Extrair título do primeiro H1
        titulo = "Manual"
        for linha in conteudo.split('\n'):
            if linha.startswith('# '):
                titulo = linha[2:].strip()
                break
        
        # Construir elementos
        elementos = []
        
        # Adicionar capa
        elementos.extend(gerar_capa(doc, titulo, styles))
        
        # Converter conteúdo
        elementos.extend(converter_markdown_para_paragrafos(conteudo, styles))
        
        # Gerar PDF
        doc.build(elementos, canvasmaker=PDFHeader)
        
        print(f"    ✓ PDF gerado: {os.path.basename(arquivo_pdf)}")
        return True
        
    except Exception as e:
        print(f"    ✗ ERRO ao gerar PDF: {str(e)}")
        return False

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("  GERANDO MANUAIS EM PDF")
    print("="*60 + "\n")
    
    # Criar pasta de PDFs
    if not os.path.exists(PASTA_PDFS):
        os.makedirs(PASTA_PDFS)
        print(f"✓ Pasta criada: {PASTA_PDFS}\n")
    
    sucesso = 0
    falhas = 0
    
    # Gerar cada PDF
    for manual in MANUAIS:
        nome_pdf = manual.replace('.md', '.pdf')
        caminho_pdf = os.path.join(PASTA_PDFS, nome_pdf)
        
        if gerar_pdf_do_manual(manual, caminho_pdf):
            sucesso += 1
        else:
            falhas += 1
    
    # Resumo
    print("\n" + "="*60)
    print(f"  CONCLUÍDO!")
    print("="*60)
    print(f"  ✓ PDFs gerados com sucesso: {sucesso}")
    if falhas > 0:
        print(f"  ✗ Falhas: {falhas}")
    print(f"  📁 Pasta: {PASTA_PDFS}\n")

if __name__ == "__main__":
    main()
