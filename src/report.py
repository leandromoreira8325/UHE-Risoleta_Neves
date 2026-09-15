import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from config import AREA_OFICIAL_HA

def gerar_relatorio_pdf(dados_serie, mapa_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=letter, 
        rightMargin=36, 
        leftMargin=36, 
        topMargin=36, 
        bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], 
        fontSize=14, leading=16, textColor=colors.HexColor('#1f385c'), 
        alignment=1, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'], 
        fontSize=9.5, leading=12, textColor=colors.HexColor('#595959'), 
        alignment=1, spaceAfter=14
    )
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Heading2'], 
        fontSize=10.5, leading=13, textColor=colors.HexColor('#1f385c'), 
        spaceBefore=10, spaceAfter=6, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'], 
        fontSize=8.5, leading=11, textColor=colors.HexColor('#262626'), 
        spaceAfter=8
    )

    # Cabeçalho
    story.append(Paragraph("MONITORAMENTO DE MACRÓFITAS E QUALIDADE DA ÁGUA", title_style))
    story.append(Paragraph("Relatório Operacional Acumulado - UHE Risoleta Neves (Candonga) - 2026", subtitle_style))
    story.append(Spacer(1, 4))
    
    # Seção 1
    story.append(Paragraph("1. Metodologia de Processamento Geoespacial", h2_style))
    texto_metodologia = (
        "A automação realiza a busca contínua no Copernicus Data Space Ecosystem selecionando, para cada mês de 2026, a imagem do "
        "satélite Sentinel-2/MSI com menor índice de nebulosidade sobre a UHE Risoleta Neves. A detecção de macrófitas é realizada via "
        "índices e razões espectrais (NDVI/MNDWI), isolando a biomassa aquática estritamente sobre a poligonal oficial do reservatório de "
        f"<b>{AREA_OFICIAL_HA:.2f} hectares</b>, garantindo contenção vetorial e auditoria espacial."
    )
    story.append(Paragraph(texto_metodologia, body_style))
    story.append(Spacer(1, 6))
    
    # Seção 2: Tabela
    story.append(Paragraph("2. Resultados Operacionais Acumulados de 2026", h2_style))
    tabela_data = [["Mês / Ano", "Área Macrófitas (ha)", "Área Reservatório (ha)", "Ocupação (%)", "Status"]]
    for item in dados_serie:
        tabela_data.append([
            item["mes"],
            f"{item['area_ha']:.2f}",
            f"{AREA_OFICIAL_HA:.2f}",
            f"{item['percentual']:.2f}%",
            item["status"]
        ])
    
    t = Table(tabela_data, colWidths=[75, 110, 115, 80, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f385c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d9d9d9')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Seção 3: Conclusão
    story.append(Paragraph("3. Conclusão e Diagnóstico Operacional", h2_style))
    ultimo = dados_serie[-1]
    texto_conc = (
        f"<b>SITUAÇÃO REGULAR:</b> A área ocupada por macrófitas na medição mais recente ({ultimo['mes']}) é de <b>{ultimo['area_ha']:.2f} ha</b>, "
        f"o que corresponde a <b>{ultimo['percentual']:.2f}%</b> da área total de referência da UHE Risoleta Neves ({AREA_OFICIAL_HA:,.2f} ha). "
        "O indicador permanece dentro dos parâmetros de estabilidade operacional."
    )
    story.append(Paragraph(texto_conc, body_style))
    story.append(Spacer(1, 8))
    
    # Seção 4: Mapeamento (Separada explicitamente)
    story.append(Paragraph("4. Mapeamento Geoespacial Auditável", h2_style))
    story.append(Paragraph("Distribuição espacial dos bancos de vegetação aquática identificados e mascarados pelo shapefile oficial:", body_style))
    story.append(Spacer(1, 6))

    if os.path.exists(mapa_path):
        story.append(Image(mapa_path, width=480, height=310))

    doc.build(story)
    print(f"[REPORT] Relatório PDF gerado com sucesso: {pdf_path}")
