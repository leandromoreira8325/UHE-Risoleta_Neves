import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas de duas passadas para numeração dinâmica de páginas 'Página X'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawRightString(280 * 2.83465, 10 * 2.83465, f"Página {self._pageNumber} de {page_count}")


def gerar_grafico_evolucao(resultados, output_path, limite_alerta_ha=30.0):
    """Gera o gráfico de linha de evolução temporal da área de macrófitas."""
    meses = [r['mes'].split('/')[0] for r in resultados]
    areas = []
    for r in resultados:
        val_str = r.get('area', '0').replace(' ha', '').strip()
        try:
            areas.append(float(val_str))
        except ValueError:
            areas.append(0.0)

    plt.figure(figsize=(9, 4.5), dpi=300)
    plt.plot(meses, areas, marker='o', color='#1f77b4', linewidth=2, label='Área Ocupada (ha)')
    plt.axhline(y=limite_alerta_ha, color='red', linestyle='--', linewidth=1.5, label=f'Limite de Alerta ({limite_alerta_ha:.2f} ha)')
    
    plt.title("Evolução Temporal da Área de Macrófitas - UHE Risoleta Neves (2026)", fontsize=11, fontweight='bold', pad=12)
    plt.xlabel("Mês / Período Processado", fontsize=9)
    plt.ylabel("Área de Macrófitas (ha)", fontsize=9)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


def gerar_relatorio_consolidado(resultados, pranchas_rgb_png, pranchas_mapa_png, output_dir, area_oficial_ha=270.0, limite_alerta_ha=30.0):
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento_2026.pdf")
    os.makedirs(output_dir, exist_ok=True)

    # Configuração de orientação Landscape A4
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        rightMargin=15, leftMargin=15, topMargin=20, bottomMargin=20
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        alignment=1, textColor=colors.HexColor('#002B49'), spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        alignment=0, textColor=colors.HexColor('#002B49'), spaceBefore=8, spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12,
        alignment=4, textColor=colors.HexColor('#333333'), spaceAfter=8
    )

    cell_style = ParagraphStyle(
        'CellText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10, alignment=1
    )

    cell_style_bold = ParagraphStyle(
        'CellTextBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1, textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------------------
    # PÁGINA 1: RESUMO OPERACIONAL CONSOLIDADO
    # -------------------------------------------------------------------------
    story.append(Paragraph("MONITORAMENTO DE MACRÓFITAS E QUALIDADE DA ÁGUA - UHE RISOLETA NEVES (2026)", title_style))
    story.append(Paragraph("RELATÓRIO OPERACIONAL CONSOLIDADO", ParagraphStyle('Sub', parent=title_style, fontSize=12, leading=14)))
    story.append(Spacer(1, 8))

    # 1. Metodologia
    story.append(Paragraph("1. Metodologia Completa de Processamento Geoespacial", subtitle_style))
    desc_metodo = (
        f"O monitoramento utiliza automação via API no Copernicus Data Space Ecosystem para obtenção de imagens multispectrais "
        f"de alta resolução do satélite Sentinel-2/MSI. Para cada período mensal, o sistema seleciona a melhor cena disponível com menor índice "
        f"de nebulosidade. Um buffer geométrico negativo de 12 metros é aplicado na poligonal do reservatório para eliminar ruídos de margem. "
        f"O cálculo de biomassa aquática emprega os índices NDVI e MNDWI sobre a área oficial de espelho d'água de {area_oficial_ha:.2f} hectares."
    )
    story.append(Paragraph(desc_metodo, body_style))
    story.append(Spacer(1, 6))

    # 2. Tabela Consolidada
    story.append(Paragraph("2. Tabela de Resultados Operacionais Acumulados (2026)", subtitle_style))
    
    headers = [
        Paragraph("Mês", cell_style_bold),
        Paragraph("Data da Cena", cell_style_bold),
        Paragraph("Área Mac.", cell_style_bold),
        Paragraph("Espelho", cell_style_bold),
        Paragraph("Ocupação", cell_style_bold),
        Paragraph("Status", cell_style_bold)
    ]
    
    table_data = [headers]
    for r in resultados:
        row = [
            Paragraph(r.get('mes', ''), cell_style),
            Paragraph(r.get('data_cena', ''), cell_style),
            Paragraph(r.get('area', ''), cell_style),
            Paragraph(f"{area_oficial_ha:.2f} ha", cell_style),
            Paragraph(r.get('ocupacao', ''), cell_style),
            Paragraph(f"<b>{r.get('status', 'REGULAR')}</b>", cell_style)
        ]
        table_data.append(row)

    t = Table(table_data, colWidths=[90, 160, 100, 100, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # 3. Gráfico de Evolução
    grafico_path = os.path.join(output_dir, "grafico_evolucao_temp.png")
    gerar_grafico_evolucao(resultados, grafico_path, limite_alerta_ha=limite_alerta_ha)
    
    story.append(Paragraph("3. Gráfico de Evolução Temporal", subtitle_style))
    story.append(Image(grafico_path, width=500, height=180))
    story.append(Spacer(1, 8))

    # 4. Conclusão
    story.append(Paragraph("4. Conclusão e Diagnóstico Operacional", subtitle_style))
    
    # Avaliação de alerta
    max_area = max([float(r.get('area', '0').replace(' ha', '').strip() or 0) for r in resultados] + [0])
    status_geral = "REGULAR" if max_area <= limite_alerta_ha else "ATENÇÃO"
    
    diagnostico = (
        f"<b>SITUAÇÃO {status_geral}:</b> O monitoramento contínuo elucida que a área ocupada por macrófitas "
        f"permanece monitorada. O limite operacional de alerta estabelecido é de {limite_alerta_ha:.2f} ha, "
        f"assegurando a conformidade ambiental e a estabilidade operacional da UHE Risoleta Neves."
    )
    story.append(Paragraph(diagnostico, body_style))

    # -------------------------------------------------------------------------
    # PRANCHAS CARTOGRÁFICAS E IMAGENS RGB
    # -------------------------------------------------------------------------
    for rgb_img, mapa_img in zip(pranchas_rgb_png, pranchas_mapa_png):
        if os.path.exists(rgb_img) and os.path.exists(mapa_img):
            story.append(PageBreak())
            story.append(Paragraph("MONITORAMENTO DE MACRÓFITAS E QUALIDADE DA ÁGUA - UHE RISOLETA NEVES (2026)", title_style))
            story.append(Spacer(1, 5))
            
            # Coloca a imagem RGB e a Prancha Lado a Lado na página em formato Landscape
            pranchas_table = Table([
                [Image(rgb_img, width=380, height=430), Image(mapa_img, width=380, height=430)]
            ], colWidths=[390, 390])
            
            pranchas_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(pranchas_table)

    # Construção do documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[RELATÓRIO] Relatório PDF padronizado gerado com sucesso em: {pdf_path}")
