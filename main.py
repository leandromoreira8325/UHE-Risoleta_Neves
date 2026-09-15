from config import OUTPUT_DIR
from processing import processar_dados_2026
from mapping import gerar_mapa_macrophitas
from report import gerar_relatorio_pdf

if __name__ == "__main__":
    print("=== Pipeline de Monitoramento Patrimonial: UHE Risoleta Neves ===")
    
    # 1. Processa dados
    dados_serie, shapefile_path = processar_dados_2026()
    ultimo_dado = dados_serie[-1]
    
    # 2. Gera mapa
    mapa_path = gerar_mapa_macrophitas(shapefile_path, ultimo_dado, OUTPUT_DIR)
    
    # 3. Gera PDF
    gerar_relatorio_pdf(dados_serie, mapa_path, OUTPUT_DIR)
    
    print("=== Pipeline concluído com sucesso! ===")
