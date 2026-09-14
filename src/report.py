import os
from fpdf import FPDF

def gerar_relatorio_pdf(dados, output_dir, area_oficial_ha):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_monitoramento.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Relatorio de Monitoramento - UHE Risoleta Neves", 0, 1, "C")
    
    pdf.set_font("Arial", "", 11)
    pdf.ln(10)
    pdf.cell(0, 10, f"Area Oficial de Agua: {area_oficial_ha} ha", 0, 1)
    
    for item in dados:
        pdf.cell(0, 10, f"Data: {item['data']} | Macrofita: {item['area_macrofita_ha']} ha ({item['percentual']}%)", 0, 1)
        
    pdf.output(pdf_path)
    print(f"Relatório PDF gerado com sucesso em: {pdf_path}")
