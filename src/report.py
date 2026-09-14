import os
from fpdf import FPDF

def gerar_relatorio_pdf(dados, output_dir, area_oficial_ha):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Institucional
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 7, "SISTEMA DE MONITORAMENTO AMBIENTAL", 0, 1, "C")
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "UHE Risoleta Neves — Alto/Médio Rio Doce", 0, 1, "C")
    pdf.ln(2)
    
    pdf.set_draw_color(120, 120, 120)
    pdf.line(10, 22, 200, 22)
    pdf.ln(4)
    
    # 1. Metodologia de Cálculo
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "1. Metodologia Utilizada para os Cálculos", 0, 1)
    pdf.set_font("Arial", "", 8.5)
    texto_metodologia = (
        "O monitoramento da cobertura de macrófitas na UHE Risoleta Neves baseia-se no "
        "sensoriamento remoto orbital utilizando imagens multiespectrais da constelação Copernicus "
        "(Sentinel-2, com resolução espacial de 10 metros). O processamento automatizado executa: "
        "(a) Correção atmosférica e conversão radiométricas das bandas B3 (Verde), B4 (Vermelho) e "
        "B8 (Infravermelho Próximo - NIR); (b) Aplicação do Índice Diferencial de Água Normalizado "
        "(NDWI) para delimitação precisa da lâmina d'água do reservatório; (c) Aplicação do Índice "
        "de Vegetação da Diferença Normalizada (NDVI) integrado a limiares espectrais para detecção "
        "de biomassa vegetal flutuante e emersa; (d) Cálculo geoespacial vetorial da área total em "
        "hectares (ha) e percentual relativo à área oficial do reservatório (1.450 ha)."
    )
    pdf.multi_cell(0, 4.2, texto_metodologia)
    pdf.ln(3)
    
    # 2. Mapa Temático
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "2. Mapa Temático de Concentração de Macrófitas", 0, 1)
    mapa_path = os.path.join(output_dir, "mapa_macromas.png")
    if os.path.exists(mapa_path):
        pdf.image(mapa_path, x=40, w=130)
    pdf.ln(3)
    
    # 3. Série Histórica (2023 a 2026)
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "3. Série Histórica Consolidada (2023 – Setembro de 2026)", 0, 1)
    
    # Cabeçalho da Tabela
    pdf.set_fill_color(225, 225, 225)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(50, 6, "Mês / Ano", 1, 0, "C", True)
    pdf.cell(70, 6, "Área Ocupada (ha)", 1, 0, "C", True)
    pdf.cell(70, 6, "% da Área Total", 1, 1, "C", True)
    
    # Linhas de dados (Loop completo 2023-2026)
    pdf.set_font("Arial", "", 8.5)
    for item in dados:
        pdf.cell(50, 5, str(item['data'])[:7], 1, 0, "C")
        pdf.cell(70, 5, f"{item['area_macrofita_ha']:.2f} ha", 1, 0, "C")
        pdf.cell(70, 5, f"{item['percentual']:.2f}%", 1, 1, "C")
        
    pdf.ln(4)
    pdf.set_font("Arial", "I", 8)
    pdf.multi_cell(0, 4, "Nota: Relatório gerado automaticamente por pipeline cloud GIS (Copernicus + Python) para suporte ao gerenciamento ambiental e atendimento às condicionantes da UHE Risoleta Neves.")
    
    pdf.output(pdf_path)
    print(f"Relatório PDF completo gerado com sucesso em: {pdf_path}")
