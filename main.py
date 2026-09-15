import os
from src.config import OUTPUT_DIR
from src.processing import processar_dados_2026
from src.mapping import gerar_mapa_macrophitas
from src.report import gerar_relatorio_pdf

if __name__ == "__main__":
    print("=== Pipeline de Monitoramento Patrimonial: UHE Risoleta Neves ===")
    
    # 1. Processamento dos dados da série temporal
    dados_serie, shapefile_path = processar_dados_2026()
    ultimo_dado = dados_serie[-1]
    
    # 2. Geração da prancha cartográfica
    mapa_path = gerar_mapa_macrophitas(shapefile_path, ultimo_dado, OUTPUT_DIR)
    
    # 3. Geração do relatório PDF final
    gerar_relatorio_pdf(dados_serie, mapa_path, OUTPUT_DIR)
    
    print("=== Pipeline concluído com sucesso! ===")
