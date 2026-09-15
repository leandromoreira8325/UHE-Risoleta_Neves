import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from src.config import AREA_OFICIAL_HA


def gerar_relatorio_pdf(
    dados_serie,
    mapa_path,
    output_dir
):

    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(
        output_dir,
        "relatorio_monitoramento.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>Relatório de Monitoramento</b>",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    ultimo = dados_serie[-1]

    texto = f"""
    Área do Reservatório: {AREA_OFICIAL_HA:.2f} ha<br/>
    Área de Macrófitas: {ultimo['area_ha']:.2f} ha<br/>
    Percentual de Ocupação: {ultimo['percentual']:.2f}%<br/>
    """

    story.append(
        Paragraph(
            texto,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    if os.path.exists(mapa_path):

        story.append(
            Image(
                mapa_path,
                width=450,
                height=290
            )
        )

    doc.build(story)

    print(
        f"[REPORT] PDF salvo: {pdf_path}"
    )
