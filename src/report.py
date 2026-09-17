"""
report.py
Geração do relatório PDF consolidado de monitoramento de macrófitas (UHE Risoleta Neves).
"""

from __future__ import annotations

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def gerar_relatorio_consolidado(dados_mensais: list[dict], output_path: str = "outputs") -> str:
    target = Path(output_path)
    
    # Se o parâmetro for um diretório ou não tiver extensão .pdf, concatena o nome do arquivo
    if target.is_dir() or target.suffix.lower() != ".pdf":
        target.mkdir(parents=True, exist_ok=True)
        pdf_file = target / "relatorio_monitoramento_2026.pdf"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        pdf_file = target

    doc = SimpleDocTemplate(
        str(pdf_file),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=15,
    )
    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=12,
        spaceAfter=8,
    )

    # 1. Cabeçalho Principal
    story.append(Paragraph("Relatório de Monitoramento de Macrófitas (2026)", title_style))
    story.append(Paragraph("Empreendimento: UHE Risoleta Neves (Candonga) | Área de Espelho d'Água: 282 ha", subtitle_style))
    story.append(Spacer(1, 10))

    # 2. Tabela Resumo Consolidada
    story.append(Paragraph("Resumo Executivo do Monitoramento Mensal", section_style))

    tabela_data = [["Mês Ref.", "Data Cena", "Nuvens (%)", "Área (ha)", "Ocupação (%)"]]
    for d in dados_mensais:
        tabela_data.append([
            d.get("mes_ref", "-"),
            d.get("data_cena", "-"),
            f"{d.get('nuvens', 0.0):.1f}%",
            f"{d.get('area_ha', 0.0):.2f}",
            f"{d.get('percentual', 0.0):.2f}%",
        ])

    t = Table(tabela_data, colWidths=[1.1 * inch, 1.3 * inch, 1.2 * inch, 1.2 * inch, 1.4 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    story.append(t)
    story.append(PageBreak())

    # 3. Anexo de Pranchas Cartográficas
    for d in dados_mensais:
        mapa_path = d.get("mapa_path")
        data_cena = d.get("data_cena", "N/A")
        mes_ref = d.get("mes_ref", "N/A")

        story.append(Paragraph(f"Prancha de Monitoramento - {mes_ref} ({data_cena})", section_style))

        if mapa_path and os.path.exists(mapa_path):
            story.append(Image(mapa_path, width=6.2 * inch, height=8.5 * inch))
        else:
            story.append(Paragraph(f"<i>Imagem do mapa não encontrada para {data_cena}.</i>", styles["Normal"]))

        story.append(PageBreak())

    doc.build(story)
    print(f"[REPORT] Relatório PDF gerado com sucesso em: {pdf_file}")
    return str(pdf_file)


# Alias para retrocompatibilidade
gerar_relatorio_pdf = gerar_relatorio_consolidado
