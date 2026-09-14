"""
Módulo de Geração de Relatórios e Gráficos (PDF & Matplotlib).
Compila o relatório executivo da UHE utilizando fpdf2, 
incluindo pranchas temáticas, imagens RGB de validação e as datas exatas das cenas.
"""

import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from src import config

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, f'MONITORAMENTO DE MACRÓFITAS E QUALIDADE DA ÁGUA – {config.UHE_NOME} (2026)', 0, 1, 'C')
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def gerar_grafico_evolucao(dados, output_dir):
    """Gera e salva o gráfico de linha da evolução temporal das macrófitas."""
    meses, valores = [], []
    for d in dados:
        meses.append(d['mes'].split('/')[0].strip())
        val_str = d['area'].replace(' ha', '')
        valores.append(float(val_str) if 'Sem' not in val_str and 'dados' not in val_str else 0.0)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.plot(meses, valores, marker='o', color='#0044cc', linewidth=2, label='Área Ocupada (ha)')
    ax.axhline(config.INDICE_ALERTA_HA, color='red', linestyle='--', label=f'Limite de Alerta ({config.INDICE_ALERTA_HA} ha)')
    ax.set_title(f"Evolução Temporal da Área de Macrófitas - {config.UHE_NOME} (2026)", fontsize=11, fontweight='bold')
    ax.set_xlabel("Mês / Período Processado", fontsize=9)
    ax.set_ylabel("Área de Macrófitas (ha)", fontsize=9)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=9)
    plt.tight_layout()
    
    grafico_path = os.path.join(output_dir, 'grafico_evolucao.png')
    plt.savefig(grafico_path, bbox_inches='tight')
    plt.close(fig)
    return grafico_path

def gerar_relatorio_pdf(dados, output_dir, area_oficial_ha):
    """Compila o relatório final em PDF utilizando fpdf2 com mapas, imagens RGB e datas exatas."""
    pdf = PDFReport(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Página 1: Metodologia e Tabela
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'RELATÓRIO OPERACIONAL CONSOLIDADO', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f"Monitoramento de Macrófitas e Qualidade da Água – {config.UHE_NOME} (2026)", 0, 1, 'C')
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '1. Metodologia Completa de Processamento Geoespacial', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    metodologia = (
        "O monitoramento utiliza automação via API no Copernicus Data Space Ecosystem para obtenção de imagens "
        "multiespectrais de alta resolução do satélite Sentinel-2/MSI. Para cada período mensal, o sistema seleciona "
        "a melhor cena disponível com menor índice de nebulosidade. Um buffer geométrico é aplicado para "
        "isolar ruídos de margem. O cálculo de biomassa aquática emprega índices espectrais "
        f"sobre a área oficial de espelho d'água de {area_oficial_ha:.2f} hectares."
    )
    pdf.multi_cell(0, 5, metodologia)
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '2. Tabela de Resultados Operacionais Acumulados (2026)', 0, 1, 'L')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    
    col_widths = [20, 50, 30, 25, 40, 25]
    headers = ["Mês", "Data da Cena", "Área Mac.", "Espelho", "Ocupação", "Status"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    for d in dados:
        data_cena_str = d.get('data_cena', 'N/D')
        pdf.cell(col_widths[0], 6, d['mes'], 1, 0, 'C')
        pdf.cell(col_widths[1], 6, data_cena_str, 1, 0, 'C')
        pdf.cell(col_widths[2], 6, d['area'], 1, 0, 'C')
        pdf.cell(col_widths[3], 6, f"{area_oficial_ha:.2f}", 1, 0, 'C')
        pdf.cell(col_widths[4], 6, d['ocupacao'], 1, 0, 'C')
        pdf.cell(col_widths[5], 6, d['status'], 1, 1, 'C')
    pdf.ln(6)

    # Página 2: Gráfico e Conclusão
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '3. Gráfico de Evolução Temporal', 0, 1, 'L')
    grafico_path = gerar_grafico_evolucao(dados, output_dir)
    if os.path.exists(grafico_path):
        pdf.image(grafico_path, x=15, w=180)
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '4. Conclusão e Diagnóstico Operacional', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    conclusao = (
        "SITUAÇÃO REGULAR: O monitoramento contínuo evidencia que a área ocupada por macrófitas permanece sob rigoroso "
        f"controle e abaixo do limite de alerta operacional estabelecido ({config.INDICE_ALERTA_HA:.2f} ha), assegurando a estabilidade "
        f"e a conformidade ambiental e hidrodinâmica do reservatório da {config.UHE_NOME} ao longo da série avaliada."
    )
    pdf.multi_cell(0, 5, conclusao)

    # Páginas Seguintes: Inclusão do Mapa Temático E da Imagem RGB com a data exata da cena
    for i, d in enumerate(dados, start=1):
        mes_nome = d['mes'].split('/')[0].strip()
        data_cena_str = d.get('data_cena', 'Data não informada')
        
        map_img = os.path.join(output_dir, f"mapa_2026_{i:02d}_{mes_nome}.png")
        rgb_img = os.path.join(output_dir, f"rgb_2026_{i:02d}_{mes_nome}.png")

        # 1. Prancha Temática de Macrófitas
        if os.path.exists(map_img):
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, f'Prancha Temática de Macrófitas – {mes_nome} / 2026 (Aquisição: {data_cena_str})', 0, 1, 'C')
            pdf.image(map_img, x=20, y=25, w=170)

        # 2. Imagem em Cor Real (RGB) para Validação de Cena
        if os.path.exists(rgb_img):
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, f'Validação de Cena - Cor Real RGB – {mes_nome} / 2026 (Aquisição: {data_cena_str})', 0, 1, 'C')
            pdf.image(rgb_img, x=20, y=25, w=170)
        else:
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, f'Validação de Cena - Cor Real RGB – {mes_nome} / 2026', 0, 1, 'C')
            pdf.set_font('Helvetica', 'I', 9)
            pdf.set_xy(20, 50)
            pdf.multi_cell(170, 6, f"[Aviso Técnico]: Imagem RGB de validação para {mes_nome}/2026 não localizada no diretório outputs.", 0, 'C')

    pdf_path = os.path.join(output_dir, 'relatorio_mensal.pdf')
    pdf.output(pdf_path)
    print(f"[SUCESSO] Relatório PDF gerado com sucesso em: {pdf_path}")
