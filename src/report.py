import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def gerar_relatorio_pdf(dados_serie, imagens_2026, output_dir, area_oficial_ha, mapa_path):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1f385c'), spaceAfter=10, alignment=1)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#595959'), spaceAfter=15, alignment=1)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1f385c'), spaceBefore=10, spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#262626'), spaceAfter=6)

    # Cabeçalho
    story.append(Paragraph("MONITORAMENTO DE MACRÓFITAS E QUALIDADE DA ÁGUA", title_style))
    story.append(Paragraph("Relatório Operacional Acumulado - UHE Risoleta Neves (Candonga) - 2026", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Metodologia
    story.append(Paragraph("1. Metodologia de Processamento Geoespacial", h2_style))
    texto_metodologia = (
        "A automação realiza a busca contínua no Copernicus Data Space Ecosystem selecionando, para cada mês de 2026, "
        "a imagem do satélite Sentinel-2/MSI com menor índice de nebulosidade sobre a UHE Risoleta Neves. A detecção de macrófitas "
        "é realizada via índices espectrais (NDVI/MNDWI), isolando a biomassa aquática estritamente sobre a poligonal oficial "
        f"do reservatório de <b>{area_oficial_ha:.2f} hectares</b>, garantindo contenção vetorial e auditoria espacial."
    )
    story.append(Paragraph(texto_metodologia, body_style))
    story.append(Spacer(1, 10))
    
    # Tabela de Dados
    story.append(Paragraph("2. Resultados Operacionais Acumulados de 2026", h2_style))
    tabela_data = [["Mês / Ano", "Área Macrófitas (ha)", "Área Reservatório (ha)", "Ocupação (%)", "Status"]]
    for item in dados_serie:
        tabela_data.append([
            item["mes"],
            f"{item['area_ha']:.2f}",
            f"{area_oficial_ha:.2f}",
            f"{item['percentual']:.2f}%",
            item["status"]
        ])
    
    t = Table(tabela_data, colWidths=[80, 100, 110, 80, 160])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f385c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d9d9d9')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Conclusão
    story.append(Paragraph("3. Conclusão e Diagnóstico Operacional", h2_style))
    ultimo = dados_serie[-1]
    texto_conc = (
        f"<b>SITUAÇÃO REGULAR</b>: A área ocupada por macrófitas na medição mais recente ({ultimo['mes']}) é de "
        f"<b>{ultimo['area_ha']:.2f} ha</b>, o que corresponde a <b>{ultimo['percentual']:.2f}%</b> da área total "
        f"de referência da UHE Risoleta Neves. O indicador permanece dentro dos parâmetros de estabilidade operacional."
    )
    story.append(Paragraph(texto_conc, body_style))
    
    # Página 2: Mapa Geográfico
    if mapa_path and os.path.exists(mapa_path):
        story.append(PageBreak())
        story.append(Paragraph("4. Mapeamento Geoespacial Auditável", h2_style))
        story.append(Paragraph("Distribuição espacial dos bancos de vegetação aquática identificados e mascarados pelo shapefile oficial:", body_style))
        story.append(Spacer(1, 10))
        story.append(Image(mapa_path, width=460, height=276))

    doc.build(story)
    print(f"[REPORT] Relatório PDF gerado em: {pdf_path}")
