"""
report.py
Consolidação do relatório mensal PDF contendo a tabela da série temporal e os mapas gerados.
"""

from __future__ import annotations

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def gerar_relatorio_consolidado(resultados_serie: list[dict], output_dir: str) -> str:
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento_2026.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1f78b4"),
        alignment=1,
    )
    normal_style = styles["Normal"]

    story = []
    story.append(Paragraph("Relatório de Monitoramento de Macrófitas (2026)", title_style))
    story.append(Paragraph("<b>Empreendimento:</b> UHE Risoleta Neves (Candonga)", normal_style))
    story.append(Spacer(1, 12))

    # Tabela com resumo da série temporal Jan-Set 2026
    tabela_dados = [["Mês Ref.", "Data Cena", "Nuvens (%)", "Área (ha)", "Ocupação (%)"]]
    for item in resultados_serie:
        tabela_dados.append([
            item["mes_ref"],
            item["data_cena"],
            f"{item['nuvens']:.1f}%",
            f"{item['area_ha']:.2f}",
            f"{item['percentual']:.2f}%",
        ])

    t = Table(tabela_dados, colWidths=[80, 100, 80, 90, 90])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f78b4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))

    # Anexo dos mapas mensais
    for item in resultados_serie:
        mapa_file = item.get("mapa_path")
        if mapa_file and os.path.exists(mapa_file):
            story.append(Paragraph(f"<b>Mapa de Monitoramento - {item['mes_ref']}</b>", normal_style))
            story.append(Spacer(1, 6))
            story.append(Image(mapa_file, width=480, height=310))
            story.append(Spacer(1, 12))

    doc.build(story)
    print(f"[REPORT] Relatório PDF gerado com sucesso: {pdf_path}")
    return pdf_path
