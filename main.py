from src.processing import processar_serie_temporal
from src.report import gerar_relatorio_pdf

if __name__ == "__main__":
    output_directory = "output"
    shapefile_dummy = "dummy.shp"
    area_oficial = 1450.0  # ha
    
    print("--- Iniciando monitoramento para: UHE Risoleta Neves (Candonga) ---")
    
    # processar_serie_temporal retorna (dados_mensais, imagens_2026)
    dados_serie, imagens_2026 = processar_serie_temporal(shapefile_dummy, output_directory)
    
    # A ordem dos parâmetros em gerar_relatorio_pdf é: (dados, imagens_2026, output_dir, area_oficial_ha)
    gerar_relatorio_pdf(dados_serie, imagens_2026, output_directory, area_oficial)
    
    print("Execucao concluida com sucesso!")
