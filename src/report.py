import os
from fpdf import FPDF

def gerar_relatorio_pdf(dados_serie, imagens_2026, output_dir, area_oficial_ha):
    """
    Gera o relatório executivo em PDF consolidando os dados de monitoramento de macrófitas
    da UHE Risoleta Neves para o ano de 2026.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho do Relatório
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatorio de Monitoramento de Macrophitas", 0, 1, "C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 8, "UHE Risoleta Neves (Candonga) - Serie Temporal 2026", 0, 1, "C")
    pdf.ln(5)
    
    # Informações gerais do reservatório
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"Area Oficial de Referencia do Reservatorio: {area_oficial_ha} ha", 0, 1, "L")
    pdf.ln(5)
    
    # Tabela de Dados Mensais
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(25, 8, "Periodo", 1, 0, "C", True)
    pdf.cell(35, 8, "Aquisicao S-2", 1, 0, "C", True)
    pdf.cell(30, 8, "Area (ha)", 1, 0, "C", True)
    pdf.cell(30, 8, "Ocupacao", 1, 0, "C", True)
    pdf.cell(70, 8, "Status do Processamento", 1, 1, "C", True)
    
    pdf.set_font("Arial", "", 9)
    for item in dados_serie:
        pdf.cell(25, 8, item["mes"], 1, 0, "C")
        pdf.cell(35, 8, item["data_aquisicao"], 1, 0, "C")
        pdf.cell(30, 8, str(item["area_ha"]), 1, 0, "C")
        pdf.cell(30, 8, f"{item['percentual']}%", 1, 0, "C")
        pdf.cell(70, 8, item["status"], 1, 1, "L")
        
    pdf.ln(10)
    
    # Resumo das Cenas Orbitais Identificadas (Corrigido com .items())
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Cenas Sentinel-2 Mapeadas no Periodo:", 0, 1, "L")
    pdf.set_font("Arial", "", 9)
    
    if imagens_2026:
        for codigo, data_aquisicao in imagens_2026.items():
            pdf.cell(0, 6, f"- Mes {codigo}: Cena catalogada em {data_aquisicao} (Copernicus Data Space)", 0, 1, "L")
    else:
        pdf.cell(0, 6, "- Nenhuma cena satelital catalogada diretamente no intervalo.", 0, 1, "L")
        
    pdf.output(pdf_path)
    print(f"Relatorio PDF completo gerado com sucesso em: {pdf_path}")
    return pdf_path
