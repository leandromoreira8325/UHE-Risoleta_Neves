import os
from fpdf import FPDF

def gerar_relatorio_pdf(dados_serie, imagens_2026, output_dir, area_oficial_ha, mapa_path=None):
    """
    Gera o relatório executivo em PDF consolidando os dados de monitoramento
    e embutindo o mapa geoespacial das macrófitas.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    pdf = FPDF()
    
    # --- PÁGINA 1: Tabela e Dados Numéricos ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatorio de Monitoramento de Macrophitas", 0, 1, "C")
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 7, "UHE Risoleta Neves (Candonga) - Serie Temporal 2026", 0, 1, "C")
    pdf.ln(4)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, f"Area Oficial de Referencia do Reservatorio: {area_oficial_ha} ha", 0, 1, "L")
    pdf.ln(3)
    
    # Tabela
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(22, 7, "Periodo", 1, 0, "C", True)
    pdf.cell(32, 7, "Aquisicao S-2", 1, 0, "C", True)
    pdf.cell(28, 7, "Area (ha)", 1, 0, "C", True)
    pdf.cell(28, 7, "Ocupacao", 1, 0, "C", True)
    pdf.cell(80, 7, "Status do Processamento", 1, 1, "C", True)
    
    pdf.set_font("Arial", "", 9)
    for item in dados_serie:
        pdf.cell(22, 6, item["mes"], 1, 0, "C")
        pdf.cell(32, 6, item["data_aquisicao"], 1, 0, "C")
        pdf.cell(28, 6, str(item["area_ha"]), 1, 0, "C")
        pdf.cell(28, 6, f"{item['percentual']}%", 1, 0, "C")
        pdf.cell(80, 6, item["status"], 1, 1, "L")
        
    pdf.ln(5)
    
    # Cenas Orbitais
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Cenas Sentinel-2 Mapeadas no Periodo:", 0, 1, "L")
    pdf.set_font("Arial", "", 8)
    if imagens_2026:
        for codigo, data_aquisicao in imagens_2026.items():
            pdf.cell(0, 5, f"- Mes {codigo}: Cena catalogada em {data_aquisicao} (Copernicus Data Space)", 0, 1, "L")
            
    # --- PÁGINA 2: Mapa Geoespacial ---
    if mapa_path and os.path.exists(mapa_path):
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Mapeamento Espacial de Macrófitas", 0, 1, "C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, "Distribuicao espacial dos bancos de vegetacao aquatica identificados no reservatorio.", 0, 1, "C")
        pdf.ln(8)
        # Insere a imagem do mapa gerada pelo matplotlib (largura 180mm)
        pdf.image(mapa_path, x=15, y=35, w=180)
        
    pdf.output(pdf_path)
    print(f"Relatorio PDF completo gerado com sucesso em: {pdf_path}")
    return pdf_path
